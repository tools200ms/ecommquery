import os
import re
import ast
import pandas as pd
import configparser
from typing import Dict, List, Set, Optional
from dataclasses import dataclass


@dataclass
class DataSource:
    name: str
    type: str
    location: str
    columns: List[str]
    description: str
    dependencies: Set[str]
    usage_files: List[str]


class DataSourceAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.sources = {}
        self.env_vars = {}
        self.data_sources = {
            'IPEDS': {'description': 'Governmental database with college information',
                      'url': 'https://nces.ed.gov/ipeds/'},
            'Peterson': {'description': 'Database with college admissions and facilities',
                         'url': 'https://petersonsdata.com/'},
            'College_Scorecard': {'description': 'Salary and financial data',
                                  'url': 'https://collegescorecard.ed.gov/data/'},
            'Campus_Safety': {'description': 'Security and crime statistics', 'url': 'https://ope.ed.gov/campussafety'},
            'OpenAlex': {'description': 'Research activity data', 'url': 'https://openalex.org/'}
        }

    def analyze(self):
        self._load_env_vars()
        self._analyze_python_files()
        self._analyze_config_files()
        self._analyze_sql_files()
        return self._generate_report()

    def _load_env_vars(self):
        env_file = os.path.join(self.project_path, 'env.sh')
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('export'):
                            key, value = line.replace('export', '').strip().split('=', 1)
                            self.env_vars[key.strip()] = value.strip().strip("'").strip('"')
            except UnicodeDecodeError:
                with open(env_file, 'r', encoding='latin-1') as f:
                    for line in f:
                        if line.startswith('export'):
                            key, value = line.replace('export', '').strip().split('=', 1)
                            self.env_vars[key.strip()] = value.strip().strip("'").strip('"')

    def _analyze_python_files(self):
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith('.py'):
                    self._analyze_python_file(os.path.join(root, file))

    def _analyze_python_file(self, file_path: str):
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    try:
                        tree = ast.parse(f.read())
                        self._analyze_ast(tree, file_path)
                        break
                    except SyntaxError:
                        continue
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error analyzing {file_path} with {encoding}: {str(e)}")
                continue
        else:
            print(f"Failed to analyze {file_path} with any encoding")

    def _analyze_ast(self, tree, file_path):
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                self._analyze_pandas_read(node, file_path)
                self._analyze_sql_query(node, file_path)
                self._analyze_api_call(node, file_path)

    def _analyze_pandas_read(self, node, file_path):
        if isinstance(node.func, ast.Attribute) and 'read' in node.func.attr:
            if hasattr(node.func.value, 'id') and node.func.value.id == 'pd':
                source_path = self._get_argument_value(node, 'filepath_or_buffer')
                if source_path:
                    self._add_data_source(source_path, 'file', file_path)

    def _analyze_sql_query(self, node, file_path):
        if isinstance(node.func, ast.Attribute) and node.func.attr in ['execute', 'read_sql']:
            query = self._get_argument_value(node, 'sql')
            if query:
                tables = self._extract_tables_from_sql(query)
                for table in tables:
                    self._add_data_source(table, 'database', file_path)

    def _analyze_api_call(self, node, file_path):
        if isinstance(node.func, ast.Attribute) and node.func.attr in ['get', 'post']:
            url = self._get_argument_value(node, 'url')
            if url:
                self._add_data_source(url, 'api', file_path)

    def _analyze_config_files(self):
        config_dirs = [self.env_vars.get('CONFIG_DIR', 'config'), '.']
        for config_dir in config_dirs:
            dir_path = os.path.join(self.project_path, config_dir)
            if os.path.exists(dir_path):
                for file in os.listdir(dir_path):
                    if file.endswith('.ini'):
                        self._analyze_ini_file(os.path.join(dir_path, file))

    def _analyze_ini_file(self, file_path):
        config = configparser.ConfigParser()
        try:
            config.read(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                config.read(file_path, encoding='latin-1')
            except Exception as e:
                print(f"Failed to read config file {file_path}: {str(e)}")
                return

        for section in config.sections():
            if 'database' in section.lower():
                for key, value in config[section].items():
                    if 'connection' in key or 'url' in key:
                        self._add_data_source(value, 'database', file_path)

    def _analyze_sql_files(self):
        for known_source in ['IPEDS', 'PETERSON', 'SCORECARD', 'CRIMES']:
            dump_file = self.env_vars.get(f'{known_source}_DUMP_FILE')
            if dump_file:
                self._analyze_sql_dump(dump_file, known_source)

    def _analyze_sql_dump(self, dump_file, source_type):
        dump_path = os.path.join(
            self.project_path,
            self.env_vars.get('DATABASE_DIR', 'databases'),
            dump_file
        )
        if os.path.exists(dump_path):
            self._add_data_source(
                dump_path,
                'database',
                source_type,
                description=self.data_sources.get(source_type, {}).get('description', '')
            )

    def _add_data_source(self, location, source_type, usage_file, description='', columns=None):
        if not location or not isinstance(location, str):
            return

        try:
            source_name = os.path.basename(location)
            if source_name not in self.sources:
                self.sources[source_name] = DataSource(
                    name=source_name,
                    type=source_type,
                    location=location,
                    columns=columns or [],
                    description=description,
                    dependencies=set(),
                    usage_files=[usage_file]
                )
            else:
                if usage_file not in self.sources[source_name].usage_files:
                    self.sources[source_name].usage_files.append(usage_file)
                if columns:
                    self.sources[source_name].columns.extend(
                        col for col in columns if col not in self.sources[source_name].columns
                    )
        except Exception as e:
            print(f"Error adding data source {location}: {str(e)}")

    def _get_argument_value(self, node, arg_name):
        for keyword in node.keywords:
            if keyword.arg == arg_name and isinstance(keyword.value, ast.Str):
                return keyword.value.s
        return None

    def _extract_tables_from_sql(self, query):
        tables = []
        matches = re.findall(r'FROM\s+(\w+)|JOIN\s+(\w+)', query, re.IGNORECASE)
        for match in matches:
            table = match[0] or match[1]
            if table:
                tables.append(table)
        return tables

    def _generate_report(self):
        report = ["# Data Source Analysis Report\n"]
        for source_name, details in self.data_sources.items():
            report.append(f"\n## {source_name}")
            report.append(f"- Description: {details['description']}")
            report.append(f"- URL: {details['url']}")
            if f"{source_name}_DUMP_FILE" in self.env_vars:
                report.append(f"- Data file: {self.env_vars[f'{source_name}_DUMP_FILE']}")
            if f"{source_name}_VERSION" in self.env_vars:
                report.append(f"- Version: {self.env_vars[f'{source_name}_VERSION']}")

        report.append("\n## Data Directory Structure")
        for dir_var in ['RESULT_DIR', 'CONFIG_DIR', 'DATABASE_DIR']:
            if dir_var in self.env_vars:
                report.append(f"- {dir_var}: {self.env_vars[dir_var]}")

        report.append("\n## Detailed Source Analysis")
        for source_name, source in self.sources.items():
            report.append(f"\n### {source_name}")
            report.append(f"- Type: {source.type}")
            report.append(f"- Location: {source.location}")
            if source.columns:
                report.append("- Columns:")
                for col in source.columns:
                    report.append(f"  - {col}")
            if source.usage_files:
                report.append("- Used in:")
                for usage in source.usage_files:
                    report.append(f"  - {usage}")

        return "\n".join(report)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze project data sources")
    parser.add_argument("project_path", help="Path to project directory")
    parser.add_argument("--output", default="data_sources_report.md", help="Output report file")
    args = parser.parse_args()

    analyzer = DataSourceAnalyzer(args.project_path)
    report = analyzer.analyze()

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)


if __name__ == "__main__":
    main()
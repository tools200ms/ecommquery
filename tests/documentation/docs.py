import os
import ast
import json
from typing import Dict, List, Optional
import anthropic
from pathlib import Path


class CodeDocumenter:
    def __init__(self, api_key: str, project_root: str):
        """Initialize the documentation generator.

        Args:
            api_key: Anthropic API key
            project_root: Root directory of the Python project
        """
        self.client = anthropic.Client(api_key=api_key)
        self.project_root = Path(project_root)

    def collect_python_files(self) -> List[Path]:
        """Recursively collect all Python files in the project."""
        python_files = []
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        return python_files

    def parse_file(self, file_path: Path) -> Dict:
        """Parse a Python file and extract its structure.

        Returns dictionary containing:
            - imports
            - classes (with methods)
            - functions
            - module docstring
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)
        structure = {
            'imports': [],
            'classes': [],
            'functions': [],
            'module_docstring': ast.get_docstring(tree)
        }

        # Process imports and module-level items
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    structure['imports'].append(name.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for name in node.names:
                    structure['imports'].append(f"{module}.{name.name}")
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'docstring': ast.get_docstring(node),
                    'methods': []
                }
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        class_info['methods'].append({
                            'name': child.name,
                            'docstring': ast.get_docstring(child)
                        })
                structure['classes'].append(class_info)
            elif isinstance(node, ast.FunctionDef):
                # This will only process top-level functions since we're using iter_child_nodes
                structure['functions'].append({
                    'name': node.name,
                    'docstring': ast.get_docstring(node)
                })

        return structure

    def generate_documentation(self, file_structure: Dict, relative_path: str) -> str:
        """Generate documentation for a single file using Claude."""
        prompt = f"""As an expert Python developer, analyze this code structure and create comprehensive documentation.
        File path: {relative_path}

        Structure:
        {json.dumps(file_structure, indent=2)}

        Please provide:
        1. A high-level overview of the file's purpose
        2. Detailed documentation for each class and method
        3. Usage examples where appropriate
        4. Any notable design patterns or architectural decisions
        5. Dependencies and requirements

        Format the response in Markdown."""

        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content

    def document_project(self) -> Dict[str, str]:
        """Document the entire project.

        Returns:
            Dictionary mapping file paths to their documentation
        """
        documentation = {}
        python_files = self.collect_python_files()

        for file_path in python_files:
            relative_path = file_path.relative_to(self.project_root)
            structure = self.parse_file(file_path)
            doc = self.generate_documentation(structure, str(relative_path))
            documentation[str(relative_path)] = doc

        return documentation

    def save_documentation(self, documentation: Dict[str, str], output_dir: str):
        """Save the generated documentation to files.

        Args:
            documentation: Dictionary mapping file paths to documentation
            output_dir: Directory to save the documentation files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Create main index.md
        index_content = "# Project Documentation\n\n## Files\n\n"
        for file_path in documentation.keys():
            clean_path = file_path.replace('\\', '/')
            index_content += f"- [{clean_path}]({clean_path}.md)\n"

        with open(output_path / 'index.md', 'w', encoding='utf-8') as f:
            f.write(index_content)

        # Save individual file documentation
        for file_path, doc_content in documentation.items():
            clean_path = file_path.replace('\\', '/')
            file_doc_path = output_path / f"{clean_path}.md"
            file_doc_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_doc_path, 'w', encoding='utf-8') as f:
                f.write(doc_content)

# Usage example:
if __name__ == "__main__":
    api_key = ""
    project_root = "C:/Users/Hp/Documents/GitHub/colleges-ranking/"
    output_dir = "docs"

    documenter = CodeDocumenter(api_key, project_root)
    documentation = documenter.document_project()
    documenter.save_documentation(documentation, output_dir)
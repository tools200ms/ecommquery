import os
from pathlib import Path

from ecommquery.exceptions import LocalResourceAccessError, DataformatError


class QueryLoader:
    __LINE_LEN_LIMIT = 1024
    __LINE_NO_LIMIT = 16392
    def __init__(self, query_path: str):
        if not os.path.exists(query_path):
            raise LocalResourceAccessError(f"Path ('{query_path}') does not exists")

        if os.path.isdir(query_path):
            q_file_list = Path(query_path).glob('**/*.query.txt')
        elif os.path.isfile(query_path):
            q_file_list = [query_path]
        else:
            raise LocalResourceAccessError(f"Provided path ('{query_path}') is not a file nor directory name")

        for q_file in q_file_list:
            if not os.path.isfile(q_file):
                continue

            if not os.path.exists(q_file):
                raise Exception(f"Missing file: {q_file}")

            print(f"Loading: {q_file}")
            self.__load(q_file)

    def __load(self, file):
        with open(file) as f:
            line_no = 0

            while ++line_no < QueryLoader.__LINE_NO_LIMIT:
                line = f.readline(QueryLoader.__LINE_LEN_LIMIT)
                if not line:
                    break;

                if len(line) == QueryLoader.__LINE_LEN_LIMIT:
                    raise DataformatError(f"Line no. {file} of file '' exceeded maximum length")

                line = line.strip()
                if len(line) == 0:
                    continue

                print(line)

            if line_no == QueryLoader.__LINE_NO_LIMIT:
                raise DataformatError(f"Too long file: {file}")

import os
from enum import Enum
from pathlib import Path

from ecommquery.assistant.lib.query import Query
from ecommquery.exceptions import LocalResourceAccessError, DataformatError


class QueryLoader:
    __LINE_LEN_LIMIT = 1024
    __LINE_NO_LIMIT = 16392

    class State(Enum):
        SPACE   = 0
        COMMENT = 1
        QUERY   = 2

    def __init__(self, query_path: str):
        if not os.path.exists(query_path):
            raise LocalResourceAccessError(f"Path ('{query_path}') does not exists")

        if os.path.isdir(query_path):
            q_file_list = Path(query_path).glob('**/*.mp.txt')
        elif os.path.isfile(query_path):
            q_file_list = [query_path]
        else:
            raise LocalResourceAccessError(f"Provided path ('{query_path}') is not a file nor directory name")

        self.__queries = {}
        for q_file in q_file_list:
            if not os.path.isfile(q_file):
                continue

            if not os.path.exists(q_file):
                raise Exception(f"Missing file: {q_file}")

            print(f"Loading: {q_file}")
            self.__load(q_file)

    def __load(self, file):
        state = QueryLoader.State.SPACE
        query = None
        query_text = ''

        f = open(file)
        try:
            line_no = 0

            while True:
                line_no += 1
                if ++line_no == QueryLoader.__LINE_NO_LIMIT:
                    raise DataformatError(f"Too long file")

                line = f.readline(QueryLoader.__LINE_LEN_LIMIT)
                if not line:
                    break;

                if len(line) == QueryLoader.__LINE_LEN_LIMIT:
                    raise DataformatError(f"Exceeded maximum line length")

                if state == QueryLoader.State.QUERY:

                    if line.rstrip() == '@end':
                        line = line.rstrip()[: -4]
                        if len(line) != 0:
                            query_text += line

                        if len(query_text) != 0:
                            query.addQuery(query_text)
                            query.ready(self.__queries)
                        else:
                            print(f"Warning: empty query {query.getName()}, line: {line_no}")

                        query = None
                        query_text = None
                        state = QueryLoader.State.SPACE
                    else:
                        query_text += line
                elif state == QueryLoader.State.COMMENT:
                    if line.rstrip().endswith('*/'): # multi line comment closed
                        state = QueryLoader.State.SPACE
                else: # Space
                    line = line.strip()

                    if len(line) == 0:
                        continue

                    if line.startswith('#'): # one line comment
                        pass # just continue reading next lines
                    elif line.startswith('/*'): # multi
                                                # line comment start, switch to comment state
                        state = QueryLoader.State.COMMENT
                    elif line.startswith('@'): # parse for instruction

                        query = Query.factory(self.__queries, line)
                        query_text = ''
                        state = QueryLoader.State.QUERY
                    else:
                        raise DataformatError(f"Unexpected syntax")

            if query != None:
                raise DataformatError(f"Query '{query.getName()}' has not been closed")

        except SyntaxError as sn_ex:
            raise SyntaxError(str(sn_ex) + f"\nError in {file}:{line_no}")
        except DataformatError as df_ex:
            raise DataformatError(str(df_ex) + f"\nError in {file}:{line_no}")
        finally:
            f.close()

    def getQueries(self):
        return self.__queries

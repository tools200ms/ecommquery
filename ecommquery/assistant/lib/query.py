import importlib
import re
import types

from ecommquery.exceptions import CallError


class Query:
    def __init__(self, name: str):
        if not re.match(r'^\w{1,256}$', name):
            raise SyntaxError(f"Incorrect query name: {name}\nexpected '@<alphanumeric name>'")

        self._name = name
        self._params = []

    @staticmethod
    def factory(q_list, line):
        instr = line.split()

        q_name = instr[0][1:]
        query = Query(q_name)

        if q_name in q_list:
            raise SyntaxError(f"Duplicated query '{q_name}'")

        for param_name in instr[1:]:
            query.addParam(param_name)

        return query

    def addParam(self, param_name: str) -> bool:
        if not param_name.isalpha() and len(param_name) < 64:
            raise SyntaxError("Illegal parameter name")

        if param_name == 'simplenamespace':
            p_class = types.SimpleNamespace
        else:
            # get ecommquery.lib. module to find class:
            module = importlib.import_module('ecommquery.lib.' + param_name)

            p_class = getattr(module, param_name.capitalize(), None)
            if not p_class:
                return False

        self._params.append(p_class)

    def ready(self, q_list):
        q_list[self._name] = self
    def addQuery(self, q_text: str) -> str:
        if len(q_text.strip()) == 0:
            raise SyntaxError("Empty Text")

        self._text = q_text

    def getName(self):
        return self._name

    def getQueryText(self) -> str:
        return self._text

    def compileQueryText(self, values: []) -> str:
        args = {}
        if len(self._params) != len(values):
            raise CallError(f"Incorrect argument number, expecting {len(self._params)}")

        for idx, param in enumerate(self._params):
            val = values[idx]
            if not isinstance(val, param):
                raise CallError(f"Expecting {param.__name__}, got {val.__name__}")

            p_name = param.__name__.lower()

            args[p_name] = val

        return self._text.format(**args)

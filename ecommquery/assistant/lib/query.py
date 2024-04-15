import importlib


class Query:
    def __init__(self, name: str):
        if not name.isalnum():
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

    def getQueryText(self):
        return self._text

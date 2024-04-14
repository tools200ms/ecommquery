import os.path
from pathlib import Path
from abc import abstractmethod

from ecommquery.exceptions import LocalResourceAccessError


class AnalyticalService:
    def query(self, scopes: [], function):
        pass

    def assignCetegories(self):
        pass

    def assignProperties(self):
        pass

    def generateSummary(self):
        pass

    def validateTexts(self):
        pass

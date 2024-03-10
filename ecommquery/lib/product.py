from abc import abstractmethod


class Product:
    def __init__(self):
        self._item_no = None
        self._name = None
        self._short_description = None
        self._description = None
        self.variant = None


from pathlib import Path

from ecommquery.core.service_management import ManagementService
from ecommquery.ext.filesystem.lib.file import FSFile


class ServiceFS(ManagementService):
    def __init__(self, path, verbose: bool, debug: bool, pretend: bool):
        super().__init__()
        self._path = Path(path)

    def establish(self):
        if not self._path.exists():
            raise(f"Path does not exist: {self._path}")

            # Check if the path is a directory
        if not self._path.is_dir():
            raise(f"Path is not a directory: {self._path}")

    def get_file(self, name: str) -> FSFile:
        """
        Merges the given file name with the base path and returns the file content.

        Args:
            name (str): The name of the file to retrieve.

        Returns:
            str: The content of the file as a string.

        Raises:
            FileNotFoundError: If the file does not exist.
            Exception: For other file-related errors.
        """
        file_path = self._path / name

        if not file_path.exists():
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        try:
            return FSFile(file_path.open('r', encoding='utf-8'))
        except Exception as e:
            raise Exception(f"An error occurred while reading the file '{file_path}': {e}")




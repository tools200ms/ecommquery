from pathlib import Path

from ecommquery.core.service_management import ManagementService


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



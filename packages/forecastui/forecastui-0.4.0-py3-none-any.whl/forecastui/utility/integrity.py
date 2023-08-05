from flask import current_app
import pathlib
from .settings_manager import SettingsManager

class Doctor:

    def __init__(self):
        self.__paths = {}
        manager = SettingsManager()
        dirs = manager.getAll("Directories")
        for key, value in dirs.items():
            self.__paths[key] = pathlib.Path(value)

    def is_first_start(self):
        path = pathlib.Path.home() / ".config" / "forecastui" / "forecastui.conf"
        return not self.exists(path)

    def create_folders(self):
        for path in self.__paths.values():
            path.mkdir(parents=True, exist_ok=True)

    def exists(self, path):
        assert isinstance(path, pathlib.Path)
        return path.exists()

import os
import typing
import inspect
import pickle
import warnings
import portalocker
import pathlib

Exportable = type(typing.Any)(
    "Exportable",
    doc="""Special type indicating an exportable type for the offshore package.
    This type behaves like Any for all practical purposes.
    """,
)


class Offshore:
    def __init__(self, filename=".offshore", autosave=False, autoload=False):
        self.__dict__["_path"] = pathlib.Path(os.getcwd()) / filename
        self.__dict__["_autosave"] = bool(autosave)
        self.__dict__["_autoload"] = bool(autoload)
        self.__dict__["_store"] = {}

        try:
            self._load()
        except FileNotFoundError:
            self.dump()

    def __getattr__(self, item):
        if self._autoload:
            self.load()

        try:
            return self._store[item]
        except KeyError as e:
            raise AttributeError(str(e))

    def __setattr__(self, key, value):
        self._store[key] = value

        if self._autosave:
            self.dump()

    def __getitem__(self, item):
        if self._autoload:
            self.load()

        return self._store[item]

    def __setitem__(self, key, value):
        self._store[key] = value

        if self._autosave:
            self.dump()

    def _load(self):
        with portalocker.Lock(str(self._path), "rb", timeout=60) as file:
            self.__dict__["_store"] = pickle.load(file)

    @staticmethod
    def _parse_stack(stack):
        frame = stack[1][0]
        global_vars = frame.f_globals
        module = inspect.getmodule(frame)

        if module is None:
            return [], global_vars

        annotations = [key for key, value in typing.get_type_hints(module).items() if value is Exportable]
        return annotations, global_vars

    def snapshot(self):
        stack = inspect.stack()
        annotations, global_vars = self._parse_stack(stack)

        if not annotations:
            warnings.warn(f"No exportable variables found")

        for key in annotations:
            self._store[key] = global_vars[key]

        self.dump()

    def restore(self):
        stack = inspect.stack()
        annotations, global_vars = self._parse_stack(stack)

        if not annotations:
            warnings.warn(f"No exportable variables found")

        self.load()

        for key in annotations:
            if key not in self._store:
                warnings.warn(f"Key '{key}' was not found in the state store and has not been restored")
                continue

            global_vars[key] = self._store[key]

    def dump(self):
        with portalocker.Lock(str(self._path), "wb", timeout=60) as file:
            pickle.dump(self._store, file)

            file.flush()
            os.fsync(file.fileno())

    def load(self):
        try:
            self._load()
        except FileNotFoundError:
            warnings.warn(f"State store not found in '{str(self._path)}'")

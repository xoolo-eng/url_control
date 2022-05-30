from collections import namedtuple
from importlib import import_module
from traceback import format_exc
from typing import TypeVar


View = TypeVar("View")

__all__ = ("Controller", "ControllerError")


class ControllerError(Exception):
    ...


class Controller:
    __slots__ = ()

    _urlpatterns = set()
    _sub_path = ""
    _route = namedtuple("Route", "path, handler, name")

    @classmethod
    def entry_point(cls, module: str) -> None:
        try:
            import_module(module)
        except Exception:
            raise ControllerError("Import root urls:\n{}".format(format_exc()))

    @classmethod
    def add(cls, path: str, handler: View, name: str) -> None:
        cls._urlpatterns.add(cls._route("".join([cls._sub_path, path]), handler, name))

    @classmethod
    def include(cls, path: str, module: str):
        old_sub_path = cls._sub_path
        cls._sub_path += path
        try:
            import_module(module)
        except Exception:
            raise ControllerError("Import root urls:\n{}".format(format_exc()))
        finally:
            cls._sub_path = old_sub_path

    @classmethod
    def urls(cls):
        for url in cls._urlpatterns:
            yield url

    @classmethod
    def get(cls, name):
        for url in cls._urlpatterns:
            if url.name == name:
                return url

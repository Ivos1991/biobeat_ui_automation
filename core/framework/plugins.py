"""Plugin discovery and registration for optional framework capabilities."""

import importlib
import pkgutil
from dataclasses import dataclass
from typing import Any, Protocol

from core.framework.types import PluginName


class FrameworkPlugin(Protocol):
    """Contract for optional framework extensions."""

    name: str
    description: str

    def register(self, runtime: Any) -> None: ...


class EvidenceCollectorPlugin(FrameworkPlugin, Protocol):
    """Optional plugin category for evidence and reporting integrations."""


class EnvironmentInitializerPlugin(FrameworkPlugin, Protocol):
    """Optional plugin category for environment bootstrapping hooks."""


_PLUGIN_REGISTRY: dict[str, type[FrameworkPlugin]] = {}


def plugin(name: str) -> Any:
    """Decorator used by plugins to self-register at import time."""

    def decorator(plugin_type: type[FrameworkPlugin]) -> type[FrameworkPlugin]:
        _PLUGIN_REGISTRY[name] = plugin_type
        return plugin_type

    return decorator


@dataclass(slots=True)
class LoadedPlugin:
    name: PluginName
    instance: FrameworkPlugin


class PluginManager:
    """Discovers and activates configured framework plugins."""

    def __init__(self, logger: Any) -> None:
        self._logger = logger
        self._loaded: dict[str, LoadedPlugin] = {}

    @property
    def loaded_plugins(self) -> tuple[LoadedPlugin, ...]:
        return tuple(self._loaded.values())

    def discover(self, package_name: str = "core.plugins.builtin") -> None:
        package = importlib.import_module(package_name)
        for module in pkgutil.iter_modules(package.__path__, f"{package_name}."):
            importlib.import_module(module.name)

    def activate(self, runtime: Any, enabled_plugins: tuple[str, ...]) -> None:
        self.discover()
        for plugin_name in enabled_plugins:
            plugin_type = _PLUGIN_REGISTRY.get(plugin_name)
            if plugin_type is None:
                self._logger.warning("Configured plugin '%s' was not discovered", plugin_name)
                continue
            instance = plugin_type()
            instance.register(runtime)
            self._loaded[plugin_name] = LoadedPlugin(name=PluginName(plugin_name), instance=instance)
            self._logger.info("Activated plugin '%s'", plugin_name)

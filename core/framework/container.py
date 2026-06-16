"""Explicit dependency injection container used by the test framework."""

from collections.abc import Callable
from dataclasses import dataclass, field
from threading import RLock
from typing import Generic, TypeVar

T = TypeVar("T")


class ContainerError(RuntimeError):
    """Raised when the service container cannot resolve a dependency."""


class Provider(Generic[T]):
    """Base provider contract."""

    def resolve(self, container: "ServiceContainer") -> T:
        """Return an instance from the container according to the provider strategy."""
        raise NotImplementedError


@dataclass(slots=True)
class SingletonProvider(Provider[T]):
    """Provider that creates a dependency once and reuses it for future resolutions."""
    factory: Callable[["ServiceContainer"], T]
    _instance: T | None = None
    _lock: RLock = field(default_factory=RLock)

    def resolve(self, container: "ServiceContainer") -> T:
        """Lazily create the singleton instance in a thread-safe way."""
        if self._instance is not None:
            return self._instance
        with self._lock:
            if self._instance is None:
                self._instance = self.factory(container)
        return self._instance


@dataclass(slots=True)
class FactoryProvider(Provider[T]):
    """Provider that creates a fresh dependency instance on every resolution."""
    factory: Callable[["ServiceContainer"], T]

    def resolve(self, container: "ServiceContainer") -> T:
        """Build and return a new instance from the registered factory."""
        return self.factory(container)


class ServiceContainer:
    """Lightweight registry for singleton and factory dependencies."""

    def __init__(self) -> None:
        """Initialize the internal provider registry."""
        self._providers: dict[object, Provider[object]] = {}

    def register_singleton(
        self, key: object, factory: Callable[["ServiceContainer"], T] | None = None, *, instance: T | None = None
    ) -> None:
        """Register a singleton dependency by instance or lazy factory."""
        if instance is not None:
            self._providers[key] = SingletonProvider(lambda _container: instance)
            return
        if factory is None:
            raise ContainerError(f"Singleton registration for {key!r} requires a factory or an instance")
        self._providers[key] = SingletonProvider(factory)

    def register_factory(self, key: object, factory: Callable[["ServiceContainer"], T]) -> None:
        """Register a dependency that should be rebuilt on each resolution."""
        self._providers[key] = FactoryProvider(factory)

    def resolve(self, key: object) -> object:
        """Resolve a dependency by key or raise a container error when it is missing."""
        try:
            provider = self._providers[key]
        except KeyError as error:
            raise ContainerError(f"No provider registered for {key!r}") from error
        return provider.resolve(self)

    def typed_resolve(self, key: object, expected_type: type[T]) -> T:
        """Resolve a dependency and validate that it matches the expected runtime type."""
        instance = self.resolve(key)
        if not isinstance(instance, expected_type):
            raise ContainerError(f"Resolved service {key!r} is not of expected type {expected_type!r}")
        return instance

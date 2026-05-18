"""Cross-cutting decorators used by services and infrastructure."""

from functools import wraps
from time import perf_counter
from typing import Any, Callable, ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


def logged_call(message: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Log method entry and exit using the bound object's ``logger`` attribute."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            logger = getattr(args[0], "logger", None) if args else None
            if logger is not None:
                logger.info("%s", message)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def timed_call(metric_name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Record execution time using the bound object's ``logger`` attribute."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            started = perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                logger = getattr(args[0], "logger", None) if args else None
                if logger is not None:
                    logger.info("%s completed in %.2fms", metric_name, (perf_counter() - started) * 1000)

        return wrapper

    return decorator


def retryable(attempts: int, exceptions: tuple[type[BaseException], ...], *, delay_seconds: float = 0.0) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry a callable for expected exceptions."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            import time

            last_error: BaseException | None = None
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    last_error = error
                    logger = getattr(args[0], "logger", None) if args else None
                    if logger is not None:
                        logger.warning("Retry %s/%s for %s after %s", attempt, attempts, func.__name__, error)
                    if attempt == attempts:
                        raise
                    if delay_seconds > 0:
                        time.sleep(delay_seconds)
            assert last_error is not None
            raise last_error

        return wrapper

    return decorator


def capture_evidence(action: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Notify the runtime hook system when an action fails."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except Exception as error:
                runtime = getattr(args[0], "runtime", None) if args else None
                if runtime is not None:
                    runtime.logger.exception("Failure while executing %s", action)
                raise error

        return wrapper

    return decorator

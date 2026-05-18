# Plugin System

## Purpose

Plugins allow optional framework capabilities to be added without modifying core runtime code.

## Core Contracts

- `FrameworkPlugin`
- `EvidenceCollectorPlugin`
- `EnvironmentInitializerPlugin`

These contracts live in `core/framework/plugins.py`.

## Discovery Model

- Built-in plugins live under `core/plugins/builtin`.
- Each plugin uses `@plugin("plugin_name")`.
- `PluginManager.discover()` imports every module in the built-in package.
- `PluginManager.activate()` instantiates only plugins listed in `Settings.plugins.enabled`.

## Current Plugins

- `session_logger`
  - Logs session and test lifecycle transitions.
- `allure_evidence`
  - Attaches failure and API evidence through the hook bus.

## Adding a Plugin

```python
from core.framework.plugins import plugin


@plugin("notifications")
class NotificationPlugin:
    name = "notifications"
    description = "Send run notifications"

    def register(self, runtime) -> None:
        runtime.hooks.register("after_session", self.send_summary, owner=self.name)

    def send_summary(self, context) -> None:
        ...
```

Then enable it through:

```env
ENABLED_PLUGINS=session_logger,allure_evidence,notifications
```

## Design Tradeoff

The framework uses import discovery instead of Python entry points because it keeps local development friction low and remains easy to explain in a code review.

from core.framework.runtime import FrameworkRuntime, build_runtime
from core.framework.hooks import HookManager
from core.framework.plugins import PluginManager


def test_runtime_build_expects_plugins_hooks_and_container_wired(monkeypatch):
    monkeypatch.setenv("ENABLED_PLUGINS", "session_logger,allure_evidence")
    runtime = build_runtime()

    try:
        assert isinstance(runtime, FrameworkRuntime)
        assert isinstance(runtime.hooks, HookManager)
        assert isinstance(runtime.plugins, PluginManager)
        assert {plugin.name for plugin in runtime.plugins.loaded_plugins} == {"session_logger", "allure_evidence"}
        assert runtime.container.resolve(FrameworkRuntime) is runtime
    finally:
        runtime.hooks.emit("after_session", runtime.session_context)

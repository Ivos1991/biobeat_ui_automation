from config.settings import Settings


def test_settings_environment_loading_expects_nested_typed_configuration(monkeypatch):
    monkeypatch.setenv("WEB_BASE_URL", "http://example.test")
    monkeypatch.setenv("API_BASE_URL", "http://api.example.test")
    monkeypatch.setenv("BROWSER_EVIDENCE_MODE", "always")
    monkeypatch.setenv("ENABLED_PLUGINS", "session_logger,allure_evidence")
    monkeypatch.setenv("FRAMEWORK_ENV", "ci")

    settings = Settings.from_env()

    assert settings.urls.web_base_url == "http://example.test"
    assert settings.urls.api_base_url == "http://api.example.test"
    assert settings.reporting.evidence_mode == "full_evidence"
    assert settings.plugins.enabled == ("session_logger", "allure_evidence")
    assert settings.runtime.environment.value == "ci"

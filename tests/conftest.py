import pytest


@pytest.fixture(autouse=True)
def set_up_test_environment(monkeypatch):
    monkeypatch.setenv("config_loader.config_loader.config.BASE_AZAIR_URL", "https://test-url.com/")

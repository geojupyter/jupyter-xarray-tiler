import pytest

pytest_plugins = ("pytest_jupyter.jupyter_server",)


@pytest.fixture
def jp_server_config(jp_server_config) -> dict:
    return {"ServerApp": {"jpserver_extensions": {"jupyter_server_titiler": True}}}

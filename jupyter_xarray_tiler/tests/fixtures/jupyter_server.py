import pytest


@pytest.fixture
def jp_server_config(jp_server_config) -> dict:
    return {
        "ServerApp": {
            "jpserver_extensions": {
                "jupyter_xarray_tiler": True,
            },
        },
    }

import pytest

pytest_plugins = (
    "pytest_jupyter.jupyter_server",
    "jupyter_xarray_tiler.tests.fixtures.server",
    "jupyter_xarray_tiler.tests.fixtures.data",
)


@pytest.fixture
def jp_server_config(jp_server_config) -> dict:
    return {
        "ServerApp": {
            "jpserver_extensions": {
                "jupyter_xarray_tiler": True,
            },
        },
    }

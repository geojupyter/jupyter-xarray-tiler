from pathlib import Path

import pytest

# Discover all modules in the tests.fixtures subpackage
FIXTURES_MODULE = ["jupyter_xarray_tiler", "tests", "fixtures"]
fixtures_dir = Path(__file__).parent.joinpath(*FIXTURES_MODULE)
fixture_plugins = [
    f"{'.'.join(FIXTURES_MODULE)}.{path.stem}"
    for path in fixtures_dir.glob("*.py")
    if not path.stem.startswith("_")
]

pytest_plugins = (
    "pytest_jupyter.jupyter_server",
    *fixture_plugins,
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

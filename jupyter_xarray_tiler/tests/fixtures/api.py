from collections.abc import AsyncGenerator

import pytest_asyncio

from jupyter_xarray_tiler.titiler import _get_server


async def _reset_titiler_api_for_testing() -> None:
    # Shutdown the previous server
    server = _get_server()
    await server.stop_tile_server()
    # Clear the cache so next time we'll get a fresh one
    _get_server.cache_clear()


@pytest_asyncio.fixture
async def clean_titiler_api() -> AsyncGenerator[None]:
    """Ensure a test's usage of the titiler API is not influenced by other tests.

    I.e., the test will receive a fresh TiTiler server.
    """
    await _reset_titiler_api_for_testing()
    yield
    await _reset_titiler_api_for_testing()

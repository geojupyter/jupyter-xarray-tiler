from collections.abc import AsyncGenerator

import pytest_asyncio

from jupyter_xarray_tiler.titiler._server import TiTilerServer


@pytest_asyncio.fixture
async def titiler_server() -> AsyncGenerator[TiTilerServer]:
    server = TiTilerServer()
    await server.start_tile_server()
    yield server

    await server.stop_tile_server()
    if server._tile_server_task:
        await server._tile_server_task
    del server

import pytest
from xarray import DataArray

from jupyter_xarray_tiler.xpublish._server import XpublishServer

from .helpers import check_tile
from .params import params_for_backend


class TestXpublishServer:
    @pytest.mark.asyncio
    async def test_server_is_not_singleton(self) -> None:
        """Test that XpublishServer is not a singleton.

        Previously, we used a singleton pattern for Xpublish server, but not anymore.
        Now, tests depend on being able to create a fresh instance and the end-user is
        protected from starting multiple instances in the public API.
        """
        assert id(XpublishServer()) != id(XpublishServer())
        assert XpublishServer() is not XpublishServer()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("z", "y", "x", "mock_data_array"),
        params_for_backend("xpublish"),
        indirect=["mock_data_array"],
    )
    async def test_add_data_array_works(
        self,
        z: int,
        y: int,
        x: int,
        clean_xpublish_server: XpublishServer,
        mock_data_array: DataArray,
    ) -> None:
        """Test that tiles can be accessed after a data array is added to the server."""
        proxy_url = await clean_xpublish_server.add_data_array(
            data_array=mock_data_array,
            rescale=(0, 1),
        )

        await check_tile(proxy_url=proxy_url.format(z=z, y=y, x=x))

    @pytest.mark.asyncio
    async def test_add_data_array_returns_valid_tile_url(
        self,
        clean_xpublish_server: XpublishServer,
        mock_data_array: DataArray,
    ) -> None:
        """Test that adding a DataArray returns a properly formatted tile URL."""
        tile_url = await clean_xpublish_server.add_data_array(
            data_array=mock_data_array,
        )

        assert tile_url is not None
        assert "/proxy/" in tile_url
        assert f"/{clean_xpublish_server._port}/" in tile_url
        assert "/tiles/WebMercatorQuad/{z}/{y}/{x}" in tile_url


class TestXpublishServerRestart:
    @pytest.mark.asyncio
    async def test_server_started_event_is_cleared_after_stop(
        self,
        clean_titiler_server: XpublishServer,
    ) -> None:
        """Test that _tile_server_started is cleared so the server can be restarted."""
        assert clean_titiler_server._tile_server_started.is_set()

        await clean_titiler_server.stop_tile_server()
        if clean_titiler_server._tile_server_task:
            await clean_titiler_server._tile_server_task

        assert not clean_titiler_server._tile_server_started.is_set()

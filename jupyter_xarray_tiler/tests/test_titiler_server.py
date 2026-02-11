import pytest
from xarray import DataArray

from jupyter_xarray_tiler.titiler._server import TiTilerServer


@pytest.mark.asyncio
async def test_server_is_not_singleton() -> None:
    """Test that TiTilerServer is not a singleton.

    Previously, we used a singleton pattern for TiTiler server, but not anymore.
    Now, tests depend on being able to create a fresh instance and the end-user is
    protected from starting multiple instances in the public API.
    """
    assert TiTilerServer() is not TiTilerServer()


@pytest.mark.asyncio
async def test_add_data_array_creates_api_routes(
    titiler_server: TiTilerServer,
    random_data_array: DataArray,
) -> None:
    """Test that FastAPI routes are created when a data array is added to the server."""
    assert len(titiler_server.routes) == 0

    await titiler_server.add_data_array(
        data_array=random_data_array,
        colormap_name="viridis",
    )

    assert len(titiler_server.routes) > 1


@pytest.mark.asyncio
async def test_add_data_array_returns_valid_tile_url(
    titiler_server: TiTilerServer,
    random_data_array: DataArray,
) -> None:
    """Test that adding a DataArray returns a properly formatted tile URL."""
    tile_url = await titiler_server.add_data_array(
        data_array=random_data_array,
        colormap_name="viridis",
    )

    assert tile_url is not None
    assert "/proxy/" in tile_url
    assert f"/{titiler_server._port}/" in tile_url
    assert "/tiles/WebMercatorQuad/{z}/{x}/{y}.png" in tile_url
    assert "colormap_name=viridis" in tile_url
    assert "scale=1" in tile_url

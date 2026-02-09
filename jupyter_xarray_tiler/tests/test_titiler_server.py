import numpy as np
import pytest
import pytest_asyncio
import xarray as xr

from jupyter_xarray_tiler.titiler import TiTilerServer


@pytest_asyncio.fixture
async def titiler_server():
    server = TiTilerServer()
    await server.start_tile_server()
    yield server

    await TiTilerServer._reset()


@pytest.fixture
def random_data_array():
    data = np.random.default_rng().random((100, 100))

    return xr.DataArray(
        data,
        dims=["y", "x"],
        coords={
            "y": np.linspace(-90, 90, 100),
            "x": np.linspace(-180, 180, 100),
        },
        attrs={"crs": "EPSG:4326"},
    )


@pytest.mark.asyncio
async def test_server_is_singleton():
    """Test that TiTilerServer is a singleton."""
    assert TiTilerServer() is TiTilerServer()
    await TiTilerServer._reset()


@pytest.mark.asyncio
async def test_server_singleton_cleanup():
    a = TiTilerServer()
    id_a = id(a)
    await TiTilerServer._reset()

    b = TiTilerServer()
    id_b = id(b)

    assert id_a != id_b


@pytest.mark.asyncio
async def test_add_data_array_creates_api_routes(titiler_server, random_data_array):
    """Test that FastAPI routes are created when a data array is added to the server."""
    assert len(titiler_server.routes) == 0

    await titiler_server.add_data_array(
        data_array=random_data_array,
        name="test_layer",
        colormap_name="viridis",
    )

    assert len(titiler_server.routes) > 1


@pytest.mark.asyncio
async def test_add_data_array_returns_valid_tile_url(titiler_server, random_data_array):
    """Test that adding a DataArray returns a properly formatted tile URL."""
    tile_url = await titiler_server.add_data_array(
        data_array=random_data_array,
        name="test_layer",
        colormap_name="viridis",
    )

    assert tile_url is not None
    assert "/proxy/" in tile_url
    assert f"/{titiler_server._port}/" in tile_url
    assert "/tiles/WebMercatorQuad/{z}/{x}/{y}.png" in tile_url
    assert "colormap_name=viridis" in tile_url
    assert "scale=1" in tile_url

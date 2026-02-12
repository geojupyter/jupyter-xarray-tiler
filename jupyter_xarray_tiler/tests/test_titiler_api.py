import pytest
from xarray import DataArray

from jupyter_xarray_tiler.titiler import (
    _get_server,
    add_data_array,
    get_routes,
)


def test_singleton_ish() -> None:
    """Test that the API only uses one TiTiler server instance."""
    assert id(_get_server()) == id(_get_server())
    assert _get_server() is _get_server()


@pytest.mark.usefixtures("clean_titiler_api")
def test_get_routes_raises_before_server_started() -> None:
    """Test that get_routes raises an error if called before initialization."""
    with pytest.raises(RuntimeError):
        get_routes()


@pytest.mark.usefixtures("clean_titiler_api")
async def test_add_data_array_creates_routes(
    random_data_array: DataArray,
) -> None:
    await add_data_array(
        data_array=random_data_array,
        colormap_name="viridis",
    )
    assert len(get_routes()) > 0

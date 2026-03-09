import pytest
from xarray import DataArray

from jupyter_xarray_tiler.xpublish import (
    _get_server,
    add_data_array,
    get_routes,
)

from .helpers import check_tile, proxy_url_to_localhost_url


def test_singleton_ish() -> None:
    """Test that the API only uses one Xpublish server instance."""
    assert id(_get_server()) == id(_get_server())
    assert _get_server() is _get_server()


@pytest.mark.usefixtures("clean_xpublish_api")
def test_get_routes_raises_before_server_started() -> None:
    """Test that get_routes raises an error if called before initialization."""
    with pytest.raises(RuntimeError):
        get_routes()


@pytest.mark.usefixtures("clean_xpublish_api")
@pytest.mark.parametrize(
    ("z", "y", "x"),
    [
        (4, 9, 4),
        pytest.param(
            1,
            1,
            1,
            marks=pytest.mark.xfail(
                reason="500. See <https://github.com/earth-mover/xpublish-tiles/issues/206#issuecomment-4015544811>"
            ),
        ),
        pytest.param(
            8,
            69,
            169,
            marks=pytest.mark.xfail(
                reason="Transparent. See <https://github.com/earth-mover/xpublish-tiles/issues/206#issuecomment-4015544811>"
            ),
        ),
    ],
)
async def test_add_data_array_works(
    z: int,
    y: int,
    x: int,
    mock_data_array: DataArray,
) -> None:
    """Test that tiles can be accessed after a data array is added to the server."""
    proxy_url = await add_data_array(data_array=mock_data_array, rescale=(0, 1))

    await check_tile(url=proxy_url_to_localhost_url(proxy_url).format(z=z, y=y, x=x))

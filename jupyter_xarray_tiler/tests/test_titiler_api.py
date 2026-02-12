import pytest

from jupyter_xarray_tiler.titiler import _get_server, get_routes


def test_get_routes_raises_before_server_started() -> None:
    """Test that get_routes raises an error if called before initialization."""
    with pytest.raises(RuntimeError):
        get_routes()


def test_singleton_ish() -> None:
    """Test that the API only uses one TiTiler server instance."""
    assert id(_get_server()) == id(_get_server())
    assert _get_server() is _get_server()

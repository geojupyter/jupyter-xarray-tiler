from jupyter_xarray_tiler.titiler import _get_server


def test_singleton_ish() -> None:
    """Test that the API only uses one TiTiler server instance."""
    assert id(_get_server()) == id(_get_server())

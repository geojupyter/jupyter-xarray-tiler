class TileIsTransparentError(Exception):
    """A tile served during testing is fully transparent."""

    reason = (
        "Transparent tile received."
        " See <https://github.com/earth-mover/xpublish-tiles/issues/206#issuecomment-4015544811>"
    )


class TileRequestReturnCodeNot200Error(Exception):
    """A request for a tile during testing returned a non-200 response code."""

    reason = (
        "Non-200 HTTP response code received."
        " See <https://github.com/earth-mover/xpublish-tiles/issues/206#issuecomment-4015544811>"
    )

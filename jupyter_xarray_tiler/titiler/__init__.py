from functools import cache
from typing import Any

from titiler.core.algorithm.base import BaseAlgorithm
from xarray import DataArray

from jupyter_xarray_tiler.titiler._singleton import TiTilerServer


@cache
def _get_server() -> TiTilerServer:
    return TiTilerServer()


async def add_data_array(
    data_array: DataArray,
    *,
    colormap_name: str = "viridis",
    rescale: tuple[float, float] | None = None,
    scale: int = 1,
    algorithm: BaseAlgorithm | None = None,
    **kwargs: str | int,
) -> str:
    """Adds a DataArray to the TiTiler server and returns a URL template.

    The TiTiler server is lazily started when the first DataArray is added.
    """
    return await _get_server().add_data_array(
        data_array,
        colormap_name=colormap_name,
        rescale=rescale,
        scale=scale,
        algorithm=algorithm,
        **kwargs,
    )


def get_routes() -> list[dict[str, Any]]:
    return _get_server().routes

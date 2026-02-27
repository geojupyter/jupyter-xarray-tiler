import uuid

import xpublish
from fastapi import FastAPI
from xarray import DataArray, Dataset
from xpublish.utils.api import DATASET_ID_ATTR_KEY
from xpublish_tiles.xpublish.tiles.plugin import TilesPlugin

from jupyter_xarray_tiler._base_server import _FastApiTileServer
from jupyter_xarray_tiler.constants._messages import (
    _found_bug_message,
    _not_initialized_message,
)


class XpublishServer(_FastApiTileServer):
    """Manage an xpublish-tiles FastAPI server instance.

    In practice, there should only ever be a single instance of this class.
    But this class is not a singleton: the public API handles this under the hood via a
    private function which holds a single instance in its cache.
    """

    def __init__(self) -> None:
        super().__init__()
        self._rest: xpublish.Rest | None = None

    def _init_fastapi_app(self) -> FastAPI:
        self._rest = xpublish.Rest(
            plugins={"tiles": TilesPlugin()},
        )
        return self._rest.app

    async def add_data_array(
        self,
        data_array: DataArray,
        # *,
        # ...
    ) -> str:
        await self.start_tile_server()

        if self._port is None:
            raise RuntimeError(f"{_not_initialized_message} {_found_bug_message}")

        # Create route on server for this data array
        source_id = str(uuid.uuid4())
        self._add_data_array_route(
            source_id=source_id,
            data_array=data_array,
        )

        # Construct URL
        # TODO: CAll self._build_url() instead of hardcoding this
        _params = ...  # ?
        return (
            f"/proxy/{self._port}/datasets/{source_id}/.../"
            "{z}/{x}/{y}.png?"  # + urlencode(_params)
        )

    def _add_data_array_route(
        self,
        *,
        source_id: str,
        data_array: DataArray,
    ) -> None:
        # TODO
        if self._app is None:
            raise RuntimeError(f"{_not_initialized_message} {_found_bug_message}")

        dataset: Dataset = data_array.to_dataset(name=data_array.name or "data")
        dataset.assign_attrs({DATASET_ID_ATTR_KEY: source_id}, inplace=True)

        # Add dataset to xpublish server
        self._rest._datasets[source_id] = dataset

import uuid
from urllib.parse import urlencode

from fastapi import FastAPI
from xarray import DataArray

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

    def _init_fastapi_app(self) -> FastAPI: ...

    async def add_data_array(
        self,
        data_array: DataArray,
        # *,
        # ...
    ) -> str:
        await self.start_tile_server()

        if self._port is None:
            raise RuntimeError(f"{_not_initialized_message} {_found_bug_message}")

        _params = ...  # ?

        source_id = str(uuid.uuid4())
        self._add_data_array_route(
            source_id=source_id,
            data_array=data_array,
            algorithm=algorithm,
        )

        return (
            f"/proxy/{self._port}/{source_id}/.../"
            "{z}/{x}/{y}.png?" + urlencode(_params)
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

        tiler = TilerFactory(
            router_prefix=f"/{source_id}",
            reader=XarrayReader,
            path_dependency=lambda: data_array,
            reader_dependency=DefaultDependency,
            process_dependency=algorithms.dependency,
        )
        self._app.include_router(tiler.router, prefix=f"/{source_id}")

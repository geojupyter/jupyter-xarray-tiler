import uuid
from asyncio import Event, Lock, Task, create_task
from functools import partial
from urllib.parse import urlencode

import rioxarray
from anycorn import Config, serve
from anyio import connect_tcp, create_task_group
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from xarray import DataArray, Dataset
from geopandas import GeoDataFrame
from rio_tiler.io.xarray import XarrayReader
from titiler.core.factory import TilerFactory
from titiler.core.algorithm import algorithms as default_algorithms
from titiler.core.algorithm import Algorithms, BaseAlgorithm
from titiler.core.dependencies import DefaultDependency

from jupyter_server_titiler.constants import ENDPOINT_BASE


# def _setup_app() -> FastAPI:
#     app = FastAPI()
# 
#     # Add CORS middleware
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],  # Allows all origins (for development - be more specific in production)
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
# 
#     return app
# 
# 
# def _create_xarray_id_lookup(*args: list[DataArray | Dataset]):
#     return {uuid.uuid4(): ds for ds in args}


class TiTilerServer:
    """Shamelessly stolen from jupytergis-tiler.

    https://github.com/geojupyter/jupytergis-tiler/blob/main/src/jupytergis/tiler/gis_document.py
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._tile_server_task: Task | None = None
        self._tile_server_started = Event()
        self._tile_server_shutdown = Event()
        self._tile_server_lock = Lock()

    async def start_tile_server(self):
        async with self._tile_server_lock:
            if not self._tile_server_started.is_set():
                self._tile_server_task = create_task(self._start_tile_server())
                await self._tile_server_started.wait()

    async def add_data_array(
        self,
        data_array: DataArray,
        name: str,
        colormap_name: str = "viridis",
        rescale: tuple[float, float] | None = None,
        scale: int = 1,
        opacity: float = 1,
        algorithm: BaseAlgorithm | None = None,
        **params,
    ):
        await self.start_tile_server()

        _params = {
            "server_url": self._tile_server_url,
            "scale": str(scale),
            "colormap_name": colormap_name,
            "reproject": "max",
            **params,
        }
        if rescale is not None:
            _params["rescale"] = f"{rescale[0]},{rescale[1]}"
        if algorithm is not None:
            _params["algorithm"] = "algorithm"
        source_id = str(uuid.uuid4())
        url = (
            f"/{ENDPOINT_BASE}/{source_id}/tiles/WebMercatorQuad/"
            + "{z}/{x}/{y}.png?"
            + urlencode(_params)
        )
        return url

    async def stop_tile_server(self):
        async with self._tile_server_lock:
            if self._tile_server_started.is_set():
                self._tile_server_shutdown.set()

    async def _start_tile_server(self):
        self._app = FastAPI()

        config = Config()
        config.bind = "127.0.0.1:0"

        async with create_task_group() as tg:
            binds = await tg.start(
                partial(
                    serve,
                    self._app,
                    config,
                    shutdown_trigger=self._tile_server_shutdown.wait,
                    mode="asgi",
                )
            )

            self._tile_server_url = binds[0]

            host, _port = binds[0][len("http://") :].split(":")
            port = int(_port)
            while True:
                try:
                    await connect_tcp(host, port)
                except OSError:
                    pass
                else:
                    self._tile_server_started.set()
                    break

    def _include_tile_server_router(
        self,
        source_id: str,
        data_array: DataArray,
        algorithm: BaseAlgorithm | None = None,
    ):
        algorithms = default_algorithms
        if algorithm is not None:
            algorithms = default_algorithms.register({"algorithm": algorithm})

        tiler = TilerFactory(
            router_prefix=f"/{source_id}",
            reader=XarrayReader,
            path_dependency=lambda:data_array,
            reader_dependency=DefaultDependency,
            process_dependency=algorithms.dependency,
        )
        self._app.include_router(tiler.router, prefix=f"/{source_id}")


# def explore(*args: list[DataArray | Dataset | GeoDataFrame]):
    # app = _setup_app()

    # xarray_objs = tuple(arg for arg in args if isinstance(arg, (DataArray, Dataset)))
    # if xarray_objs:
    #     xarray_id_lookup = _create_xarray_id_lookup(xarray_objs)

    #     tiler_factory = TilerFactory(
    #         path_dependency=xarray_id_lookup.get,
    #         reader=XarrayReader,
    #         reader_dependency=DefaultDependency,
    #     )
    #     app.include_router(tiler_factory.router)
    #     
    #     import uvicorn
    #     uvicorn.run(app=app, host="127.0.0.1", port=8080, log_level="info")
    #     # return app, xarray_id_lookup

    # # Display a widget
    # # TODO: What if there are multiple widgets?
    # # TODO: Clean up when widgets clean up
    # raise NotImplementedError("Only xarray.Dataset and xarray.DataArray are supported for now.")


# def test() -> Dataset | DataArray:
#     ds = rioxarray.open_rasterio(
#         "https://s2downloads.eox.at/demo/EOxCloudless/2020/rgbnir/s2cloudless2020-16bits_sinlge-file_z0-4.tif"
#     )
#     return explore(ds)

import uuid
from asyncio import Event, Lock, Task, create_task
from functools import partial
from typing import Any, Self
from urllib.parse import urlencode

import httpx
from anycorn import Config, serve
from anyio import connect_tcp, create_task_group
from fastapi import FastAPI
from fastapi.routing import APIRoute
from jupyter_server.serverapp import list_running_servers
from rio_tiler.io.xarray import XarrayReader
from titiler.core.algorithm import BaseAlgorithm
from titiler.core.algorithm import algorithms as default_algorithms
from titiler.core.dependencies import DefaultDependency
from titiler.core.factory import TilerFactory
from xarray import DataArray

from jupyter_server_titiler.constants import ENDPOINT_BASE
from jupyter_server_titiler.kernel import get_kernel_id


class TiTilerServer:
    """A singleton class to manage a TiTiler FastAPI server instance.

    Shamelessly stolen from jupytergis-tiler.

    https://github.com/geojupyter/jupytergis-tiler/blob/main/src/jupytergis/tiler/gis_document.py
    """

    _instance: Self | None = None
    _kernel_id: str
    _app: FastAPI

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs) -> None:
        if hasattr(self, "_tile_server_task"):
            return

        super().__init__(*args, **kwargs)
        self._tile_server_task: Task | None = None
        self._tile_server_started = Event()
        self._tile_server_shutdown = Event()
        self._tile_server_lock = Lock()
        self._kernel_id = get_kernel_id()

    @classmethod
    async def reset(cls) -> None:
        if not cls._instance:
            raise RuntimeError(f"{cls.__name__} not initialized")

        await cls._instance.stop_tile_server()
        if cls._instance._tile_server_task:  # noqa: SLF001
            await cls._instance._tile_server_task  # noqa: SLF001

        del cls._instance
        cls._instance = None

    @property
    def routes(self) -> list[dict[str, Any]]:
        return [
            {"path": route.path, "name": route.name}
            for route in self._app.router.routes
            if isinstance(route, APIRoute)
        ]

    async def start_tile_server(self) -> None:
        async with self._tile_server_lock:
            if self._tile_server_started.is_set():
                return
            self._tile_server_task = create_task(self._start_tile_server())
            await self._tile_server_started.wait()

    async def add_data_array(
        self,
        data_array: DataArray,
        colormap_name: str = "viridis",
        rescale: tuple[float, float] | None = None,
        scale: int = 1,
        algorithm: BaseAlgorithm | None = None,
        **params,
    ) -> str:
        await self.start_tile_server()

        _params = {
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

        self._include_tile_server_router(source_id, data_array, algorithm)

        return (
            f"/{ENDPOINT_BASE}/{source_id}/tiles/WebMercatorQuad/"
            "{z}/{x}/{y}.png?" + urlencode(_params)
        )

    async def stop_tile_server(self) -> None:
        async with self._tile_server_lock:
            if self._tile_server_started.is_set():
                self._tile_server_shutdown.set()

    async def _start_tile_server(self) -> None:
        self._app = FastAPI(
            openapi_url="/",
            docs_url=None,
            redoc_url=None,
        )

        config = Config()
        config.bind = "127.0.0.1:0"

        async with create_task_group() as tg:
            binds = await tg.start(
                partial(
                    serve,
                    self._app,  # type: ignore[arg-type]
                    config,
                    shutdown_trigger=self._tile_server_shutdown.wait,  # type: ignore[arg-type]
                    mode="asgi",
                ),
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

            await self._register_server()

    async def _register_server(self) -> None:
        async with httpx.AsyncClient() as client:
            # FIXME: I know this is wrong. There may be multiple running servers. I'm
            # asking for help.
            server_info = next(list_running_servers())
            url = f"{server_info['url']}{ENDPOINT_BASE}"
            payload = {
                "kernel_id": self._kernel_id,
                "server_url": self._tile_server_url,
            }
            response = await client.post(url, json=payload)
            response.raise_for_status()

    def _include_tile_server_router(
        self,
        source_id: str,
        data_array: DataArray,
        algorithm: BaseAlgorithm | None = None,
    ) -> None:
        algorithms = default_algorithms
        if algorithm is not None:
            algorithms = default_algorithms.register({"algorithm": algorithm})

        tiler = TilerFactory(
            router_prefix=f"/{source_id}",
            reader=XarrayReader,
            path_dependency=lambda: data_array,
            reader_dependency=DefaultDependency,
            process_dependency=algorithms.dependency,
        )
        self._app.include_router(tiler.router, prefix=f"/{source_id}")

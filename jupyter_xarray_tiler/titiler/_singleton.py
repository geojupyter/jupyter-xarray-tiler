import uuid
from asyncio import Event, Lock, Task, create_task
from functools import partial
from typing import Any, ClassVar, Self
from urllib.parse import urlencode

from anycorn import Config, serve
from anyio import connect_tcp, create_task_group
from fastapi import FastAPI
from fastapi.routing import APIRoute
from rio_tiler.io.xarray import XarrayReader
from titiler.core.algorithm import algorithms as default_algorithms
from titiler.core.algorithm.base import BaseAlgorithm
from titiler.core.dependencies import DefaultDependency
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from titiler.core.factory import TilerFactory
from xarray import DataArray

_incorrect_usage_message = (
    "If you're seeing this, you're probably 'holding it wrong'. Check out the docs!"
)


class TiTilerServer:
    """A singleton class to manage a TiTiler FastAPI server instance."""

    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_tile_server_task"):
            return

        self._app: FastAPI | None = None
        self._port: int | None = None
        self._tile_server_task: Task[None] | None = None
        self._tile_server_started = Event()
        self._tile_server_shutdown = Event()
        self._tile_server_lock = Lock()

    @classmethod
    async def _reset(cls) -> None:
        """Destroy the singleton instance -- for testing only."""
        if not cls._instance:
            raise RuntimeError(f"{cls.__name__} not initialized")

        await cls._instance.stop_tile_server()
        if cls._instance._tile_server_task:  # noqa: SLF001
            await cls._instance._tile_server_task  # noqa: SLF001

        del cls._instance
        cls._instance = None

    @property
    def routes(self) -> list[dict[str, Any]]:
        if self._app is None:
            raise RuntimeError(
                f"Server not correctly initialized. {_incorrect_usage_message}"
            )

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
        *,
        colormap_name: str = "viridis",
        rescale: tuple[float, float] | None = None,
        scale: int = 1,
        algorithm: BaseAlgorithm | None = None,
        **kwargs: str | int,
    ) -> str:
        await self.start_tile_server()

        _params = {
            "scale": str(scale),
            "colormap_name": colormap_name,
            "reproject": "max",
            **kwargs,
        }
        if rescale is not None:
            _params["rescale"] = f"{rescale[0]},{rescale[1]}"
        if algorithm is not None:
            _params["algorithm"] = "algorithm"
        source_id = str(uuid.uuid4())

        self._include_tile_server_router(
            source_id=source_id,
            data_array=data_array,
            algorithm=algorithm,
        )

        return (
            f"/proxy/{self._port}/{source_id}/tiles/WebMercatorQuad/"
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
        add_exception_handlers(self._app, DEFAULT_STATUS_CODES)

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

            host, port = binds[0][len("http://") :].split(":")
            self._port = int(port)
            while True:
                try:
                    await connect_tcp(host, self._port)
                except OSError:
                    pass
                else:
                    self._tile_server_started.set()
                    break

    def _include_tile_server_router(
        self,
        *,
        source_id: str,
        data_array: DataArray,
        algorithm: BaseAlgorithm | None = None,
    ) -> None:
        if self._app is None:
            raise RuntimeError(
                f"Server not correctly initialized. {_incorrect_usage_message}"
            )

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

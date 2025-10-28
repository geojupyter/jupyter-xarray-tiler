import uuid

import rioxarray
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from xarray import DataArray, Dataset
from geopandas import GeoDataFrame
from rio_tiler.io.xarray import XarrayReader
from titiler.core.factory import TilerFactory
from titiler.core.dependencies import DefaultDependency

def _setup_app() -> FastAPI:
    app = FastAPI()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins (for development - be more specific in production)
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def _create_xarray_id_lookup(*args: list[DataArray | Dataset]):
    return {uuid.uuid4(): ds for ds in args}


def explore(*args: list[DataArray | Dataset | GeoDataFrame]):
    app = _setup_app()

    xarray_objs = tuple(arg for arg in args if isinstance(arg, (DataArray, Dataset)))
    if xarray_objs:
        xarray_id_lookup = _create_xarray_id_lookup(xarray_objs)

        tiler_factory = TilerFactory(
            path_dependency=xarray_id_lookup.get,
            reader=XarrayReader,
            reader_dependency=DefaultDependency,
        )
        app.include_router(tiler_factory.router)
        
        import uvicorn
        uvicorn.run(app=app, host="127.0.0.1", port=8080, log_level="info")
        # return app, xarray_id_lookup

    # Display a widget
    # TODO: What if there are multiple widgets?
    # TODO: Clean up when widgets clean up
    raise NotImplementedError("Only xarray.Dataset and xarray.DataArray are supported for now.")


def test() -> Dataset | DataArray:
    ds = rioxarray.open_rasterio(
        "https://s2downloads.eox.at/demo/EOxCloudless/2020/rgbnir/s2cloudless2020-16bits_sinlge-file_z0-4.tif"
    )
    return explore(ds)

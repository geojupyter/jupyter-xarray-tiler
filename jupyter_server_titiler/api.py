from xarray import DataArray

from jupyter_server_titiler.titiler import TiTilerServer


# async def explore(*args: list[DataArray | Dataset]):
async def explore(da: DataArray) -> str:
    """Explore xarray DataArrays and Datasets in a map widget.

    This function must be called with await in a Jupyter notebook:
        await explore(data_array)

    TODO: Support any number of Xarray objects
    """
    titiler_server = TiTilerServer()
    return await titiler_server.add_data_array(da, name="my_da")

    # TODO: Display a widget
    # TODO: What if there are multiple widgets?
    # TODO: Clean up when widgets clean up

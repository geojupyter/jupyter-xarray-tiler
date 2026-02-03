# Quickstart

As an author of a an interactive map library for Jupyter, you might use
`jupyter-xarray-tiler` to provide the ability to dynamically visualize data in Xarray
DataArrays without writing to a file like so:

```python
from jupyter_xarray_tiler import TiTilerServer


class MyMapLibrary:
  # ...

  def add_xarray_layer(self, da: xr.DataArray):
    # Get a server object (will always reference the same server);
    # server will be started if necessary:
    tileserver = TiTilerServer()

    # Add the layer to the tile server.
    # A URL that passes through the Jupyter server proxy will be returned:
    url = tileserver.add_data_array(da)

    # Add the layer to your map!
    self._add_tile_layer(url)
```

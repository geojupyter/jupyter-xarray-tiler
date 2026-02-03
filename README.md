# Jupyter Xarray Tiler

[![Github Actions Status - Build](https://github.com/geojupyter/jupyter-xarray-tiler/workflows/Build/badge.svg)](https://github.com/geojupyter/jupyter-xarray-tiler/actions/workflows/build.yml)

> [!IMPORTANT]
> This repository is experimental and in the prototype stage.
> Expect nothing to work.
> Expect the name to change in the future.

A Jupyter server extension which provides an API to launch a server to dynamically tile
[Xarray DataArray](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.html)s
for interactive visualization.

### :rocket: Powered by...

[TiTiler (Development Seed)](https://developmentseed.org/titiler/)

Other backends (e.g.
[xpublish-tiles (earthmover)](https://github.com/earth-mover/xpublish-tiles)) may be
supported in the future!

### :sparkles: Inspired by...

[jupytergis-tiler](https://github.com/geojupyter/jupytergis-tiler) by
[David Brochart](https://github.com/davidbrochart)

## Who is this for?

Intended to be consumed by interactive map libraries for Jupyter, **not end-users**,
e.g.:

* [Leafmap](https://leafmap.org/)
* [ipyleaflet](https://ipyleaflet.readthedocs.io)
* [ipyopenlayers](https://ipyopenlayers.readthedocs.io/)
* More?

## What problem does this solve?

For authors of interactive map libraries for Jupyter, providing a dynamic HTTP tile
server presents a unique problem: **they don't know where Jupyter is running**.
It could be, for example, running on:

* users' local machines
* a shared JupyterLab instance on an intranet
* an authenticated JupyterHub in a public cloud

The first case is the simplest; when the tile server is running on `localhost`, the map
viewer running in JavaScript in the user's browser can connect to it.

In the other cases, the map viewer needs a public URL to connect to.
The URL of the current JupyterHub instance may not be known.
Additionally, a map server running in a Jupyter kernel isn't exposed to the public
internet in many cases (for example, when it's running in a Kubernetes pod as part of a
JupyterHub).
This extension provides [dynamic proxying](https://jupyter-server-proxy.readthedocs.io/)
to map servers running in the kernel.

## Usage

As a Jupyter interactive map library author, you may implement a method like:

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

## Install

> [!WARNING]
> This method of installation doesn't work yet.
> Install from source or see the [contributing instuctions](CONTRIBUTING.md) for now.

Recommended:

```bash
uv add jupyter-xarray-tiler
```

Or:

```bash
pixi add jupyter-xarray-tiler
```

For other methods of installation, including pip, conda, mamba, and micromamba, see the
[installation instructions in the documentation](https://jupyter-xarray-tiler.readthedocs.io/user-guide/install/).

### From source

```bash
uv add git+https://github.com/geojupyter/jupyter-xarray-tiler.git#egg=jupyter-xarray-tiler
```

If you prefer to install from a local clone of the source, view the
[Contributor Guide in our documentation](https://jupyter-xarray-tiler.readthedocs.io/contributor-guide)!

## Contributing

See the
[Contributor Guide in our documentation](https://jupyter-xarray-tiler.readthedocs.io/contributor-guide)!

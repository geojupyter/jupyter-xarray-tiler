# Backends

## [TiTiler](https://developmentseed.org/titiler/)

TiTiler, by [Development Seed](https://developmentseed.org/), is "a modern dynamic tile
server built on top of FastAPI and Rasterio/GDAL".


## [xpublish-tiles](https://github.com/earth-mover/xpublish-tiles)

[Xpublish](https://xpublish.readthedocs.io/), by [earthmover](https://earthmover.io/), is a tool to "publish Xarray datasets
to the web".
xpublish-tiles is a plugin to serve time images with the OGC Tiles API.

Like TiTiler, it's a dynamic tile server using FastAPI.

Unlike TiTiler, xpublish-tiles uses a GDAL-free rendering pipeline under the hood.
Additionally, the Xpublish API is built around DataArrays, not Datasets.

xpublish-tiles claims to be faster, but lacks some features like support for rendering
algorithms that TiTiler supports, e.g. hillshade rendering.

[Read more about xpublish-tiles and how it compares to TiTiler on the earthmover blog](https://earthmover.io/blog/dynamic-map-tile-rendering-icechunk-zarr-data-xpublish-tiles/)!

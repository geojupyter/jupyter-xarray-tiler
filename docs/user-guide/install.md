# Install

:::{important}
This extension doesn't directly depend on JupyterLab, as it is intended to support other
front-ends.

If you're using it with JupyterLab, it requires JupyterLab >= 4.0.0
:::

## From PyPI

:::{warning}
This method of installation doesn't work yet.
Install from source or see the [contributing instuctions](/contributor-guide/index.md) for now.
:::

`````````{tabs}
``````{group-tab} uv (recommended)
```bash
uv add jupyter-xarray-tiler
```
``````

``````{group-tab} pip
```bash
pip install jupyter-xarray-tiler
```
``````
`````````

## From Conda Forge

:::{warning}
This method of installation doesn't work yet.
Install from source or see the [contributing instuctions](/contributor-guide/index.md) for now.
:::

`````````{tabs}
``````{group-tab} Pixi (recommended)
```bash
pixi add jupyter-xarray-tiler
```
``````

``````{group-tab} conda/mamba/micromamba
```bash
conda install jupyter-xarray-tiler
```

You can substitute `conda` in this command for `mamba` or `micromamba` as appropriate.
``````
`````````

## From source

:::{hint}
If you prefer to install from a local clone, view the
[contributing instuctions](/contributor-guide/index.md).
:::

`````````{tabs}
``````{group-tab} uv (recommended)
```bash
uv add git+https://github.com/geojupyter/jupyter-xarray-tiler.git#egg=jupyter-xarray-tiler
```
``````

``````{group-tab} pip
```bash
pip install git+https://github.com/geojupyter/jupyter-xarray-tiler.git#egg=jupyter-xarray-tiler
```
``````
`````````

## Uninstall

Depending on how you installed:

`````````{tabs}
``````{group-tab} uv (recommended)
```bash
uv remove jupyter-xarray-tiler
```
``````

``````{group-tab} pip
```bash
pip uninstall jupyter-xarray-tiler
```
``````

``````{group-tab} Pixi (recommended)
```bash
pixi remove jupyter-xarray-tiler
```
``````

``````{group-tab} conda/mamba/micromamba
```bash
conda uninstall jupyter-xarray-tiler
```

You can substitute `conda` in this command for `mamba` or `micromamba` as appropriate.
``````

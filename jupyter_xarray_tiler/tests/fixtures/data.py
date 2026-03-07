import numpy as np
import pytest
import xarray as xra
from affine import Affine


@pytest.fixture
def mock_data_array() -> xra.DataArray:
    npixels_y = 100
    npixels_x = 100
    min_x = -180
    max_x = 180
    min_y = -90
    max_y = 90

    y_coords = np.linspace(max_y, min_y, npixels_y, endpoint=False)
    x_coords = np.linspace(min_x, max_x, npixels_x, endpoint=False)
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)

    data = ((x_grid - x_grid.min()) + (y_grid - y_grid.min())) / 2  # Diagonal gradient
    data = data / data.max()  # Normalize to 0-1

    da = xra.DataArray(
        data,
        dims=["y", "x"],
        coords={
            "y": y_coords,
            "x": x_coords,
        },
    )
    da.rio.write_crs("EPSG:4326", inplace=True)

    # Calculate pixel size
    x_res = (max_x - min_x) / npixels_x
    y_res = (max_y - min_y) / npixels_y

    transform = Affine.translation(min_x, max_y) * Affine.scale(x_res, -y_res)

    da.rio.write_transform(transform, inplace=True)
    return da

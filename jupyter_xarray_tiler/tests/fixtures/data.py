import numpy as np
import pytest
from xarray import DataArray


@pytest.fixture
def random_data_array() -> DataArray:
    data = np.random.default_rng().random((100, 100))

    da = DataArray(
        data,
        dims=["y", "x"],
        coords={
            "y": np.linspace(-90, 90, 100),
            "x": np.linspace(-180, 180, 100),
        },
    )
    return da.rio.write_crs("EPSG:4326")

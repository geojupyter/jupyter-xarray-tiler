from jupyter_server.serverapp import ServerApp

from jupyter_server_titiler._routes import setup_routes
from jupyter_server_titiler._routes.registry import unregister_server
from jupyter_server_titiler.api import explore
from jupyter_server_titiler.constants import (
    LAB_EXTENSION_NAME,
    SERVER_EXTENSION_NAME,
)
from jupyter_server_titiler.titiler import TiTilerServer

__all__ = ["TiTilerServer", "explore"]

try:
    from jupyter_server_titiler._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip:
    # <https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs>
    import warnings

    warnings.warn(
        f"Importing '{SERVER_EXTENSION_NAME}' outside a proper installation."
        " It's highly recommended to install the package from a stable release or"
        " in editable mode.",
        stacklevel=2,
    )
    __version__ = "dev"


def _jupyter_labextension_paths() -> list[dict[str, str]]:
    return [
        {
            "src": "labextension",
            "dest": LAB_EXTENSION_NAME,
        },
    ]


def _jupyter_server_extension_points() -> list[dict[str, str]]:
    return [
        {
            "module": SERVER_EXTENSION_NAME,
        },
    ]


def _load_jupyter_server_extension(server_app: ServerApp) -> None:
    """Registers the API routes to receive HTTP requests from the frontend extension.

    Parameters
    ----------
    server_app: Jupyter server application instance

    """
    setup_routes(server_app.web_app)

    # When a kernel shuts down, remove entry from registry of running TiTiler servers
    shutdown_kernel = server_app.kernel_manager.shutdown_kernel

    async def unregister_and_shutdown_kernel(kernel_id: str, *args, **kwargs) -> None:
        unregister_server(kernel_id)
        server_app.log.debug(f"Unregistered {kernel_id} TiTiler server")
        await shutdown_kernel(kernel_id, *args, **kwargs)

    server_app.kernel_manager.shutdown_kernel = unregister_and_shutdown_kernel  # type: ignore[method-assign]

    server_app.log.info(f"Registered '{SERVER_EXTENSION_NAME}' server extension")

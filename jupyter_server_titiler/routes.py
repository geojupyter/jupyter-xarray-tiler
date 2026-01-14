import httpx

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

from jupyter_server_titiler.constants import (
    ENDPOINT_BASE,
    SERVER_EXTENSION_NAME,
)


class TiTilerRouteHandler(APIHandler):
    """How does this handler work?"""

    @tornado.web.authenticated
    async def get(self, path: str):
        if not path:
            self.finish(
                f"This is the root endpoint of the '{SERVER_EXTENSION_NAME}'"
                " server extension"
            )
            return

        params = {key: val[0].decode() for key, val in self.request.arguments.items()}
        server_url = params.pop("server_url")
        print(path)
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{server_url}/{path}", params=params)
            self.write(r.content)


def setup_routes(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]

    titiler_route_pattern = url_path_join(base_url, ENDPOINT_BASE, "(.*)")

    routes = [(titiler_route_pattern, TiTilerRouteHandler)]
    web_app.add_handlers(host_pattern, routes)

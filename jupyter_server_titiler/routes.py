import httpx

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

from jupyter_server_titiler.constants import ENDPOINT_BASE
from jupyter_server_titiler.api import TiTilerServer


class TiTilerRouteHandler(APIHandler):
    """How does this handler work?"""

    @tornado.web.authenticated
    async def get(self, path: str):
        params = {key: val[0].decode() for key, val in self.request.arguments.items()}

        server = TiTilerServer()
        await server.start_tile_server()
        get_url = f"{server._tile_server_url}/{path}"

        # Proxy the request to FastAPI service
        async with httpx.AsyncClient() as client:
            r = await client.get(get_url, params=params)

            content_type = r.headers.get("content-type")
            if content_type:
                self.set_header("Content-Type", content_type)

            self.set_status(r.status_code)
            self.write(r.content)
            await self.flush()


def setup_routes(web_app):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]

    titiler_route_pattern = url_path_join(base_url, ENDPOINT_BASE, "(.*)")
    routes = [(titiler_route_pattern, TiTilerRouteHandler)]

    web_app.add_handlers(host_pattern, routes)

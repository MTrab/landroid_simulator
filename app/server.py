"""Web server classes."""

import base64
import logging
import ssl

from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet
import jinja2

from .tools.database import Database
from .urlhandlers import *


class HttpRequestHandler:
    """HTTP handler."""

    def __init__(
        self,
        config: dict,
        keep_alive: int = 75,
        **kwargs,
    ) -> None:
        """Initialize the web server."""

        self._config = config
        self._port = config["port"]
        self._ip = config["ip"]
        self._dir = config["template_path"]
        self._logger = logging.getLogger(__name__)
        self._runner: web.AppRunner

    async def handle_root(self, request):
        """Handle an incoming request."""
        return web.Response(text="Nothing here yet!")

    # async def handle_proxy(self, request):
    #     """Forward incoming requests."""
    #     url = f"https://api.worxlandroid.com{request.path_qs}"
    #     print(url)
    #     async with ClientSession() as client:
    #         async with client.request(
    #             method=request.method,
    #             url=url,
    #             verify_ssl=False,
    #             headers=request.headers,
    #         ) as resp:
    #             assert resp.status == 200
    #         data = await resp.text()

    #     return web.Response(text=data)

    async def start(self):
        """Start the service."""
        app = web.Application()

        app["database"] = Database(self._config["database_path"])

        fernet_key = fernet.Fernet.generate_key()
        secret_key = base64.urlsafe_b64decode(fernet_key)
        setup_session(app, EncryptedCookieStorage(secret_key))

        app.add_routes([web.route("*", "", self.handle_root)])
        app.add_routes([web.route("*", "/", self.handle_root)])

        app.add_subapp("/sim", app_sim)
        app.add_subapp("/api/v2", app_api)

        # app.add_routes([web.route("*", "/{tail:.*}", self.handle_proxy)])

        aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(self._dir))

        self._runner = web.AppRunner(app)
        await self._runner.setup()

        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(
            "/workspaces/landroid_simulator/certs/server.crt",
            "/workspaces/landroid_simulator/certs/server.key",
        )

        site = web.TCPSite(self._runner, self._ip, self._port, ssl_context=ssl_context)

        await site.start()
        self._logger.info(
            "Listening for web requests on https://%s:%s", self._ip, self._port
        )

    async def stop(self):
        """Stop the service."""
        self._logger.info("Closing listener")
        await self._runner.cleanup()

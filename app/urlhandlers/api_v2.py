"""Generic API-v2 handler."""

import logging
from aiohttp import web
from aiohttp_session import get_session

from ..datasets import Dataset, DatasetDescription

app = web.Application()
routes = web.RouteTableDef()

_LOGGER = logging.getLogger(__name__)


@routes.view("/product-items")
class productitems(web.View):
    """Handling users products."""

    async def get(self) -> str:
        """Return a test string."""
        return "User data"


@routes.view("/products")
class products(web.View):
    """Handling all products information."""

    async def get(self) -> str:
        """Return products info."""
        session = await get_session(self.request)
        if not "vendor" in session:
            raise web.HTTPFound("/sim/authenticate")

        vendor = DatasetDescription.from_json(session["vendor"])
        dataset = Dataset(vendor)

        return web.Response(text=dataset.load(vendor.products_file))


@routes.view("/boards")
class boards(web.View):
    """Handling all boards information."""

    async def get(self) -> str:
        """Return boards info."""
        session = await get_session(self.request)
        if not "vendor" in session:
            raise web.HTTPFound("/sim/authenticate")

        vendor = DatasetDescription.from_json(session["vendor"])
        dataset = Dataset(vendor)

        return web.Response(text=dataset.load(vendor.boards_file))


@routes.view("/product-items/(.*)/status")
class productstatus(web.View):
    """Handling device status information."""

    async def get(self, serial) -> str:
        """Return a test string."""
        return f"This is device status for {serial}"


@routes.view("/oauth/token")
class token(web.View):
    """Return token."""

    async def post(self) -> str:
        """Receive data."""
        token_data = {
            "access_token": "TestToken",
            "token_type": "Test",
            "mqtt_endpoint": "omv.trab.dk:1234",
        }
        return web.json_response(token_data)


@routes.view("/me")
class me(web.View):
    """Handling user info."""

    async def get(self) -> str:
        """Return a test string."""
        return "User data"


@routes.view("/certificate")
class certificate(web.View):
    """Handling user certificate."""

    async def get(self) -> str:
        """Return a test string."""
        return "Certificate data"


app.add_routes(routes)

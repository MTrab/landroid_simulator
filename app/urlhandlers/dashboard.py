"""Authenticate user logins."""
import logging
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session

_LOGGER = logging.getLogger(__name__)


@web.middleware
async def check_session(request, handler):
    """Check for valid session."""
    session = await get_session(request)
    if (not "loggedin" in session) or not session["loggedin"]:
        raise web.HTTPFound("/sim")

    response = await handler(request)
    return response


app = web.Application(middlewares=[check_session])
routes = web.RouteTableDef()


@routes.view("")
@routes.view("/")
class Authenticate(web.View):
    """Authentication class."""

    @aiohttp_jinja2.template("sim/dashboard/index.html")
    async def get(self):
        """Show basic dashboard."""
        session = await get_session(self.request)

        return {"email": session["email"]}


app.add_routes(routes)

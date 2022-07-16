"""Authenticate user logins."""
import logging
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session

from app.tools.database import Database, UserInfo

_LOGGER = logging.getLogger(__name__)


@web.middleware
async def check_session(request, handler):
    """Check for valid session."""
    session = await get_session(request)
    if (not "loggedin" in session) or not session["loggedin"]:
        raise web.HTTPFound("/sim")

    db: Database = request.config_dict["database"]
    session["userdata"] = db.get_userinfo(session["email"])

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
        # userdata = UserInfo.from_json(session["userdata"])
        return UserInfo.from_json(session["userdata"]).to_dict()


app.add_routes(routes)

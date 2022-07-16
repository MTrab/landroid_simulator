"""Authenticate user logins."""
import hashlib
import logging
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session

from app.tools.database import DatabaseTypes

from .dashboard import app as app_dashboard

_LOGGER = logging.getLogger(__name__)

app = web.Application()
app.add_subapp("/dashboard", app_dashboard)

routes = web.RouteTableDef()


@routes.view("/authenticate")
class Authenticate(web.View):
    """Authentication class."""

    # async def get(self):
    #     """For testing purposes only."""
    #     session = await get_session(self.request)
    #     # if not "vendor" in session:
    #     session["vendor"] = Vendor.WORX.to_json()
    #     return web.Response(text="Testing authenticate get")

    async def post(self):
        """Data from client."""
        indata = await self.request.post()

        db = self.request.config_dict["database"]
        authdb = db.connect(DatabaseTypes.USERS)
        if isinstance(authdb, type(None)):
            _LOGGER.error(
                "Could not authorize user, as there was an error opening the database!"
            )
            return web.Response(
                status=500,
                text="500: Server error - Error opening database connection!",
            )

        pwdhash = hashlib.md5(indata["password"].encode("utf-8")).hexdigest()
        cursor = authdb.cursor()
        cursor.execute(
            "select count(*) from users where email=? and password=?",
            (indata["email"], pwdhash),
        )
        data = cursor.fetchone()[0]
        authdb.close()

        if data == 0:
            return web.Response(status=403, text="403: Unauthorized")
        else:
            session = await get_session(self.request)
            session["loggedin"] = True
            session["email"] = indata["email"]
            session.max_age = 5 * 60
            raise web.HTTPFound("/sim")


@routes.view("/")
@routes.view("")
class Root(web.View):
    """Root simulator page."""

    @aiohttp_jinja2.template("sim/index.html")
    async def get(self):
        """Return some test data."""
        session = await get_session(self.request)
        if ("loggedin" in session) and session["loggedin"]:
            raise web.HTTPFound("/sim/dashboard")

        return {}


@routes.view("/lostpass")
class ForgotPassword(web.View):
    """Class for handling forgotten passwords."""

    async def get(self):
        """Return some test data."""
        return web.Response(text="Lost password")


@routes.view("/create")
class CreateUser(web.View):
    """Class for creating users."""

    async def get(self):
        """Return some test data."""
        return web.Response(text="Create user")


app.add_routes(routes)

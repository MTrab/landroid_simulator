"""Authenticate user logins."""
import hashlib
import logging
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session

from app.tools.database import Database, DatabaseTypes

from .dashboard import app as app_dashboard

_LOGGER = logging.getLogger(__name__)

app = web.Application()
app.add_subapp("/dashboard", app_dashboard)

routes = web.RouteTableDef()


@routes.post("/authenticate")
async def Authenticate(request):
    """Authentication."""
    indata = await request.post()

    db: Database = request.config_dict["database"]
    authdb = db.connect(DatabaseTypes.USERS)
    if isinstance(authdb, type(None)):
        _LOGGER.error(
            "Could not authorize user, as there was an error opening the database!"
        )
        return web.Response(
            status=500,
            text="500: Server error - Error opening database connection!",
        )

    pwdhash = db.hash_password(indata["password"])
    cursor = authdb.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE email=? AND password=?",
        (indata["email"], pwdhash),
    )
    data = cursor.fetchone()[0]
    authdb.close()

    if data == 0:
        return web.Response(status=403, text="403: Unauthorized")
    else:
        session = await get_session(request)
        session["loggedin"] = True
        session["email"] = indata["email"]
        session.max_age = 5 * 60
        raise web.HTTPFound("/sim")


@routes.get("/")
@routes.get("")
@aiohttp_jinja2.template("sim/index.html")
async def Root(request):
    """Root simulator page."""
    session = await get_session(request)
    if ("loggedin" in session) and session["loggedin"]:
        raise web.HTTPFound("/sim/dashboard")

    return {}


@routes.view("/create")
class CreateUser(web.View):
    """Class for creating users."""

    @aiohttp_jinja2.template("sim/create.html")
    async def get(self):
        """Return create form."""
        return {}

    async def post(self):
        """Save the user."""
        indata = await self.request.post()

        db: Database = self.request.config_dict["database"]
        if db.user_exist(indata["email"]):
            return aiohttp_jinja2.render_template(
                "sim/create_user_exist.html", request=self.request, context=indata
            )

        if not db.save_user(indata):
            return aiohttp_jinja2.render_template(
                "sim/create_error_save.html", request=self.request, context=indata
            )

        # return web.HTTPTemporaryRedirect(
        #     "/sim/authenticate",
        # )
        return await Authenticate(self.request)


app.add_routes(routes)

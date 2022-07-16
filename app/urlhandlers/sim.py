"""Authenticate user logins."""
import hashlib
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session

from app.datasets import Vendor

# from app.datasets import Vendor

app = web.Application()
routes = web.RouteTableDef()
# aiohttp_jinja2.setup(app,    loader=jinja2.FileSystemLoader('static/sim'))


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

        authdb
        pwdhash = hashlib.md5(indata["password"].encode("utf-8")).hexdigest()
        check = authdb.execute(
            "select * from users where email=? and password=?",
            (indata["email"], pwdhash),
        )
        if check:
            # web.ctx.session.loggedin = True
            # web.ctx.session.username = indata.username
            raise web.HTTPFound("/sim")
        else:
            return "Those login details don't work!"


@routes.view("/")
@routes.view("")
class Root(web.View):
    """Root simulator page."""

    @aiohttp_jinja2.template("sim/index.html")
    async def get(self):
        """Return some test data."""
        return {}

    #     return web.Response(text="Test")  # render.index()


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

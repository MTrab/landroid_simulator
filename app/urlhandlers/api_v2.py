"""Generic API-v2 handler."""
import web

from ..datasets import Dataset

web.config.debug = False
app = web.auto_application()


class productitems(app.page):
    """Handling users products."""

    path = "/product_items"

    def GET(self) -> str:
        """Return a test string."""
        return "User data"


class products(app.page):
    """Handling all products information."""

    path = "/products"

    def GET(self) -> str:
        """Return products info."""
        if not "vendor" in web.ctx.session:
            raise web.seeother("/sim/authenticate", True)

        dataset = Dataset(web.ctx.session.vendor)

        return dataset.load(dataset.vendor.products_file)


class boards(app.page):
    """Handling all boards information."""

    path = "/boards"

    def GET(self) -> str:
        """Return boards info."""
        if not "vendor" in web.ctx.session:
            raise web.seeother("/sim/authenticate", True)

        dataset = Dataset(web.ctx.session.vendor)

        return dataset.load(dataset.vendor.boards_file)


class productstatus(app.page):
    """Handling device status information."""

    path = "/product-items/(.*)/status"

    def GET(self, serial) -> str:
        """Return a test string."""
        return f"This is device status for {serial}"

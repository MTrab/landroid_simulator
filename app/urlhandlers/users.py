"""Landroid user handler."""
import web

app = web.auto_application()


class me(app.page):
    """Handling user info."""

    path = "/me"

    def GET(self) -> str:
        """Return a test string."""
        return "User data"


class certificate(app.page):
    """Handling user certificate."""

    path = "/certificate"

    def GET(self) -> str:
        """Return a test string."""
        return "Certificate data"

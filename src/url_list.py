"""URL list."""

import json
from .datasets import VendorName, Dataset, DatasetType

urls = (
    "/",
    "root",
    "/api/v2/oauth/token",
    "token",
    "/api/v2/users/me",
    "me",
    "/api/v2/users/certificate",
    "certificate",
    "/api/v2/product-items",
    "productitems",
    "/api/v2/products",
    "products",
    "/api/v2/boards",
    "boards",
    "/api/v2/product-items/(.*)/status",
    "productstatus",
)


class root:
    """Basic web-root for the service"""

    def GET(self) -> str:
        """HTTP GET handler for the web root.

        Returns:
            str: HTTP response
        """
        return (
            "<h1 align='center'><b>This is the web-root. "
            "Nothing to see here, move along!</b></h1>"
        )


class token:
    """Return token."""

    def POST(self) -> str:
        """Receive data."""
        token_data = {
            "access_token": "TestToken",
            "token_type": "Test",
            "mqtt_endpoint": "omv.trab.dk:1234",
        }
        return json.dumps(token_data)


class me:
    """Handling user info."""

    def GET(self) -> str:
        """Return a test string."""
        return "User data"


class certificate:
    """Handling user certificate."""

    def GET(self) -> str:
        """Return a test string."""
        return "User data"


class productitems:
    """Handling users products."""

    def GET(self) -> str:
        """Return a test string."""
        return "User data"


class products:
    """Handling all products information."""

    def GET(self) -> str:
        """Return products info."""
        dataset = Dataset(VendorName.WORX)

        return dataset.load(DatasetType.PRODUCTS)


class boards:
    """Handling all boards information."""

    def GET(self) -> str:
        """Return boards info."""
        dataset = Dataset(VendorName.WORX)

        return dataset.load(DatasetType.BOARDS)


class productstatus:
    """Handling device status information."""

    def GET(self, serial) -> str:
        """Return a test string."""
        return f"This is device status for {serial}"

"""oAuth handler."""
import json
import web

app = web.auto_application()


class token(app.page):
    """Return token."""

    path = "/token"

    def POST(self) -> str:
        """Receive data."""
        token_data = {
            "access_token": "TestToken",
            "token_type": "Test",
            "mqtt_endpoint": "omv.trab.dk:1234",
        }
        return json.dumps(token_data)

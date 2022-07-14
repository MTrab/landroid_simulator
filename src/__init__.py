"""Main program file."""

import sys
from typing import Any

import web
from cheroot.server import HTTPServer
from cheroot.ssl.builtin import BuiltinSSLAdapter

from .datasets import VendorName
from .url_list import *

# __all__ = ["ServerBase"]

THIS_VENDOR = None


class ServerBase:
    """Base server class."""

    __service: Any

    def __init__(self, port: str = "88", vendor: VendorName = VendorName.WORX) -> Any:
        """Init base server object."""
        sys.argv.append(port)
        THIS_VENDOR = vendor
        self.__service = web.application(urls, globals())
        self.__session = web.session.Session(
            self.__service, web.session.DiskStore(".sessions")
        )

    def start(self) -> None:
        """Starts the web service"""
        HTTPServer.ssl_adapter = BuiltinSSLAdapter(
            certificate="certs/server.crt", private_key="certs/server.key"
        )
        self.__service.run()

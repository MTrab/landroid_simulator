"""App version."""

import logging


class VersionManager:
    """Version manager."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.version = "0.0.1-dev"
        self.author = "Malene Trab (https://github.com/mtrab)"
        self.license = "GPL-3.0"

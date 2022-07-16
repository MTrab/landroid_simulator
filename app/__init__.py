"""Main program file."""

import asyncio
import logging
import os

from .__version__ import VersionManager
from .server import HttpRequestHandler
from .tools.logger import init_logger


def main(config: dict):
    """Main process"""
    logfile = os.path.join(config["log_path"], "landroid_simulator.log")
    if config["log_level"].lower() == "debug":
        loglevel = logging.DEBUG
    elif config["log_level"].lower() == "info":
        loglevel = logging.INFO
    elif config["log_level"].lower() == "warning":
        loglevel = logging.WARNING
    elif config["log_level"].lower() == "error":
        loglevel = logging.ERROR
    elif config["log_level"].lower() == "critical":
        loglevel = logging.CRITICAL
    else:
        loglevel = logging.NOTSET

    init_logger(logfile, loglevel=loglevel)

    _LOGGER = logging.getLogger(__name__)

    ver = VersionManager()
    _LOGGER.info(
        r"""
    __                  __            _      __
   / /  ___ _  ___  ___/ /____ __    (_) ___/ /
  / /__/ _ `/ / _ \/ _  // __// _ \ / / / _  /
 /_______,__ /_//_/\_,_//_/__ \___//_/_ \_,_/
   / __/ (_) __ _  __ __  / / ___ _ / /_ ___   ____
  _\ \  / / /  ' \/ // / / / / _ `// __// _ \ / __/
 /___/ /_/ /_/_/_/\_,_/ /_/  \_,_/ \__/ \___//_/
    """
    )
    _LOGGER.info("Version: %s", ver.version)
    _LOGGER.info("Author: %s", ver.author)
    _LOGGER.info("License: %s", ver.license)
    _LOGGER.debug("Saving log files in %s", config["log_path"])
    _LOGGER.debug("Serving templates from %s", config["template_path"])
    _LOGGER.info(
        "Listening for MQTT connections on tcp://%s:%s",
        config["ip"],
        config["mqtt_port"],
    )

    app = HttpRequestHandler(config)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(app.start())
        loop.run_forever()
    except (KeyboardInterrupt, TypeError):
        loop.run_until_complete(app.stop())

    loop.close()

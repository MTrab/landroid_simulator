"""
Landroid Simulator

Used for testing and developing pyWorxcloud and Landroid_Cloud modules.
"""

import os
from app.__version__ import app_author, app_license, app_version
from app.tools.logger import Logger

if __name__ == "__main__":
    base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "log")
    print(
        r"""
    __                  __              _      __
   / /  ___ _  ___  ___/ /  ____ ___   (_) ___/ /
  / /__/ _ `/ / _ \/ _  /  / __// _ \ / / / _  /
 /_______,__ /_//_/\_,_/  /_/__ \___//___ \_,_/
   / __/  (_)  __ _  __ __  / / ___ _ / /_ ___   ____
  _\ \   / /  /  ' \/ // / / / / _ `// __// _ \ / __/
 /___/  /_/  /_/_/_/\_,_/ /_/  \_,_/ \__/ \___//_/
    """
    )
    print("Version: " + str(app_version))
    print("Author: " + str(app_author))
    print("License: " + str(app_license))

    log_debug = os.path.join(base_path, "landroid_simulator.log")
    log_err = os.path.join(base_path, "landroid_simulator.log")
    Logger.create_logger(log_debug, log_err, __package__)

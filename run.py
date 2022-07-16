"""
Landroid Simulator

Used for testing and developing pyWorxcloud and Landroid_Cloud modules.
"""

import argparse
import os
import app

if __name__ == "__main__":
    run_path = os.path.abspath(os.path.dirname(__file__))
    parser = argparse.ArgumentParser(
        description="Landroid Simulator commandline arguments",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Set port number to be used for web interface",
        default="88",
        type=str,
    )
    parser.add_argument(
        "-l",
        "--log_level",
        help="Set lowest loglevel",
        default="info",
        choices=["critical", "error", "warning", "info", "debug"],
        type=str,
    )
    parser.add_argument(
        "-b", "--log_backup", help="Number of log backups to keep", type=int
    )
    parser.add_argument(
        "--log_path",
        help="Path where log files will be saved",
        type=str,
        default=os.path.join(run_path, "log"),
    )
    parser.add_argument(
        "--ip",
        help="IP address to listen for requests",
        type=str,
        default="0.0.0.0",
    )

    config = vars(parser.parse_args())
    config.update({"template_path": os.path.join(run_path, "app/templates")})

    app.main(config)

"""
Prometheus exporter for package version
"""
import argparse
import logging
from pathlib import Path

from prometheus_client import start_http_server, Info

from version_exporter.config import read_config
from version_exporter.rpm_query import get_versions

PORT = 9998


def main():
    """
    Main entrypoint
    """
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
    args = parse_args()
    config = read_config(Path(args.config))

    # Set metrics and start exporter http server
    i = Info(
        "version_exporter_packages_version", "Versions of locally installed packages"
    )
    i.info(get_versions(config["rpm"]))

    start_http_server(PORT)
    logging.info("http server started on port %d", PORT)

    try:
        while True:
            continue
    except KeyboardInterrupt:
        logging.info("Shutting down...")


def parse_args() -> argparse.Namespace:
    """
    Parse CLI args

    Return:
        argpase.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Exporter version of locally installed packages"
    )
    parser.add_argument(
        "--config", help="configuration file path", default="/opt/config.yaml"
    )

    return parser.parse_args()

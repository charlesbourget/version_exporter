"""
Prometheus exporter for package version
"""
import argparse
from pathlib import Path

from prometheus_client import start_http_server, Info

from version_exporter.config import read_config
from version_exporter.rpm_query import get_versions


def main():
    """
    Main entrypoint
    """
    args = parse_args()
    config = read_config(Path(args.config))

    # Set metrics and start exporter http server
    i = Info("packages_version", "Versions of locally installed packages")
    i.info(get_versions(config["rpm"]))
    start_http_server(9998)

    try:
        while True:
            continue
    except KeyboardInterrupt:
        print("Shutting down...")


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

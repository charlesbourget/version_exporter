"""
Wrapper around RPM database
"""
import logging

try:
    import rpm
except ModuleNotFoundError:
    logging.error(
        (
            "You must install the following package:\n"
            "sudo dnf install -y python3-rpm\n"
            "'rpm' doesn't come as a pip but as a system dependency.\n"
        )
    )
    raise


def get_versions(rpm_packages: list) -> dict:
    """
    Get version number from list of packages

    Args:
        rpm_packages (list): List of packages to fetch

    Returns:
        dict: packages with their versions
    """
    versions = {}
    for rpm_package in rpm_packages:
        logging.info("Fetching version for package: %s", rpm_package)
        with QueryHelper(limit=1, name=rpm_package) as rpm_query:
            for result in rpm_query:
                versions[result["name"]] = result["version"]

    return versions


class QueryHelper:
    """
    Wrapper around the rpm db

    Yields:
        dict: rpm package info
    """

    MAX_NUMBER_OF_RESULTS = 10_000

    def __init__(self, *, limit: int = MAX_NUMBER_OF_RESULTS, name: str):
        """
        :param limit: How many results to return
        :param name: Filter by package name
        """
        self.transaction_set = rpm.TransactionSet()
        self.name = name
        self.limit = limit

    def __enter__(self):
        """
        Returns list of items on the RPM database
        """

        dataset = self.transaction_set.dbMatch("name", self.name)

        count = 0
        for rpm_package in dataset:
            if count >= self.limit:
                break
            yield rpm_package
            count += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transaction_set.closeDB()

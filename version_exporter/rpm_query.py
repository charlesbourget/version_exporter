"""
Wrapper around RPM database
"""
import sys

try:
    import rpm
except ModuleNotFoundError:
    print(
        (
            "You must install the following package:\n"
            "sudo dnf install -y python3-rpm\n"
            "'rpm' doesn't come as a pip but as a system dependency.\n"
        ),
        file=sys.stderr,
    )
    raise


def get_versions(rpm_packages: list):
    """_summary_

    Args:
        packages (list): _description_

    Returns:
        _type_: _description_
    """
    versions = {}
    for rpm_package in rpm_packages:
        with QueryHelper(limit=5, name=rpm_package) as rpm_query:
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

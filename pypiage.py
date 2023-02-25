from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib import request, error
import json
import logging
import sys
import os

PYTHON_LOGLEVEL = os.getenv("PYTHON_LOGLEVEL", "INFO")
PACKAGE_FETCH_TIMEOUT = int(os.getenv("PACKAGE_FETCH_TIMEOUT", 5))
BASE_URL = "https://pypi.org/pypi/{}/json"

logging.basicConfig(level=PYTHON_LOGLEVEL)
logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            packages = [line.strip().split("==")[0] for line in f if line.strip()]
    else:
        packages = [line.strip().split("==")[0] for line in sys.stdin if line.strip()]

    def get_package_info(package):
        logger.info(f"Getting package info for {package}")
        try:
            with request.urlopen(
                BASE_URL.format(package), timeout=PACKAGE_FETCH_TIMEOUT
            ) as response:
                if response.status == 200:
                    package_info = json.loads(response.read())
                    upload_time = package_info["urls"][-1]["upload_time"]
                    return package, upload_time
        except error.URLError as e:
            logger.error(f"Failed to fetch package info for {package}: {e}")

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_package_info, package) for package in packages]
        package_years = {
            package: year
            for package, year in (f.result() for f in as_completed(futures))
            if year
        }

    sorted_packages = sorted(
        [
            (pkg, datetime.strptime(year, "%Y-%m-%dT%H:%M:%S"))
            for pkg, year in package_years.items()
        ],
        key=lambda x: x[1],
    )

    for package, upload_time in sorted_packages:
        print(f"{package}|{upload_time}")


if __name__ == "__main__":
    main()

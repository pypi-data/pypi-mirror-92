import os
import sys

sys.path.insert(0, os.path.abspath("."))

from ingots.utils.packages_versions import build_package_full_version  # noqa
from ingots.utils.packages_versions import create_package_version_file  # noqa

from ingot_tcp import VERSION  # noqa


if __name__ == "__main__":
    create_package_version_file(
        full_package_version=build_package_full_version(
            base_package_version=VERSION,
            version_suffix_env_name="INGOT_TCP_VERSION_SUFFIX",
        )
    )

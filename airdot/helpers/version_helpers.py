import os, sys
from typing import Optional

supported_python_versions = ["3", "4", "5", "6", "7", "8", "9"]


def get_python_default_version(python_version: Optional[str] = None):
    if python_version is None:
        # add getting environment python version here
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        return verify_version(python_version)
    else:
        return verify_version(python_version)


def verify_version(python_version):
    if python_version.split(".")[-1][0] in supported_python_versions:
        return python_version
    else:
        raise Exception(
            f"Unsupported python version passed {python_version}. current supported version {supported_python_versions}"
        )

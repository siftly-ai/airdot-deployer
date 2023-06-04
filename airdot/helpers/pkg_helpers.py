import os, sys
from typing import Optional, List, Dict
import pkg_resources
import types
from importlib.metadata import version
import json
import requests
import warnings


pkg_mapping = {"sklearn": "scikit-learn"}

base_pkg = []


def get_environment_pkgs(
    python_packages: Optional[List[str]] = None, func_globals=None
):
    if python_packages is None:
        return verify_packages(
            get_pip_list().split("\n"), func_globals
        )  # get_pip_list().split("\n")
    elif isinstance(python_packages, list):
        return python_packages + base_pkg


# only explicit install ?
def get_pip_list() -> List[Dict[str, str]]:
    return os.popen("python -m pip freeze | grep == ").read().strip()


def imports(func_globals):
    module_list = []
    for name, val in func_globals.items():
        if isinstance(val, types.ModuleType):
            module_list.append(val.__name__)
    return module_list


def get_locally_installed_packages(encoding=None):
    packages = []
    ignore = ["tests", "_tests", "egg", "EGG", "info"]
    for path in sys.path:
        for root, dirs, files in os.walk(path):
            for item in files:
                if "top_level" in item:
                    item = os.path.join(root, item)
                    with open(item, "r", encoding=encoding) as f:
                        package = root.split(os.sep)[-1].split("-")
                        try:
                            package_import = f.read().strip().split("\n")
                        except:  # NOQA
                            # TODO: What errors do we intend to suppress here?
                            continue
                        for i_item in package_import:
                            if (i_item not in ignore) and (package[0] not in ignore):
                                version = None
                                if len(package) > 1:
                                    version = (
                                        package[1]
                                        .replace(".dist", "")
                                        .replace(".egg", "")
                                    )
                                packages.append(f"{package[0]}=={version}")
    return list(set(packages))


def get_root_pkgs(pkg_list):
    root_pkg = []
    for pkg in pkg_list:
        if len(pkg.split(".")) > 1 and pkg.split(".")[0] in pkg_mapping:
            root_pkg.append(pkg_mapping[pkg.split(".")[0]])
        else:
            root_pkg.append(pkg)
    return root_pkg


def verify_packages(pkg_list, func_globals):
    # get only used modules
    used_pkg_list = []
    used_imports = get_root_pkgs(imports(func_globals))
    for item in pkg_list:
        pkg_name, pkg_version = item.split("==")
        if pkg_name in used_imports:
            used_pkg_list.append(f"{pkg_name}=={pkg_version}")
    pypi_url = "https://pypi.org/pypi/{}/{}/json"
    final_pkg_list = []
    for item in used_pkg_list:
        pkg_name, pkg_version = item.split("==")
        status_code = requests.get(pypi_url.format(pkg_name, pkg_version)).status_code
        if status_code == 200:
            final_pkg_list.append(item)
        else:
            warnings.warn(f"Not a valid Pypi package {pkg_name}. ignoring the package")
    final_pkg_list = final_pkg_list + base_pkg
    return final_pkg_list

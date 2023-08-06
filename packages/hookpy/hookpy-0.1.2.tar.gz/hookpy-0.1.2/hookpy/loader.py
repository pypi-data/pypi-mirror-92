import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Optional

from hookpy import compat
from hookpy.compat import VALID_PYTHON_MODULE_NAME_PATTERN

CUSTOM_LOADED_MODULES = {}


def locate_package(package_name, cwd_check=False) -> Optional[Path]:
    """locale package by find_spec, perfered method.
    """
    assert package_name != "__init__"
    if not VALID_PYTHON_MODULE_NAME_PATTERN.match(package_name):
        return None
    try:
        spec = importlib.util.find_spec(package_name)
    except ValueError:
        # this usually happens when the module is overrided by a custom ModuleType.
        return None 
    if spec is None:
        return None
    if spec.origin is None:
        return None

    origin = Path(spec.origin)
    cwd = Path.cwd()
    if origin.name == "__init__.py":
        # has submodule
        if origin.parent.parent == cwd and cwd_check:
            msg = (
                "find a package in cwd, you must use locate_package_subproc"
                " or run program in a directory that dont contain a package.")
            raise ValueError(msg)
        return origin.parent
    return origin


def locate_top_package(file_path, cwd_check=False):
    """you need to provide a setup.py in your project and
    install it with pip install -e . or regular approach.
    if a package is located via cwd, a warn is produced and cwd package
    is returned.
    """
    file_path = Path(file_path).resolve()
    res = None
    cwd = Path.cwd()
    for path in file_path.parents:
        package_root = locate_package(path.stem)
        if package_root is not None:
            if package_root != path:
                continue
            res = path
            if path.parent == cwd and cwd_check:
                msg = (
                    "find a package in cwd, you must use locate_top_package_subproc"
                    " or run program in a directory that dont inside a package."
                )
                raise ValueError(msg)
            break
    return res


def _get_mod_name_from_path(path):
    path = Path(path)
    return path.name.split(".")[0]


def try_capture_import_parts(source_path, package_name=None):
    """
    if your function path is project/mod0/func_mod.py,
    then the import_parts is [project, mod0, func_mod]
    """
    source_path = Path(source_path).resolve()
    if package_name is None:
        # find outer module name
        path = locate_top_package(source_path)
        if path is None:
            return None
        path_candidates = [path]
        found_modules = []
        for path in path_candidates:
            module_name = _get_mod_name_from_path(path)
            module_loader = importlib.util.find_spec(module_name)
            if module_loader is not None:
                found_modules.append(module_name)
        assert len(
            path_candidates
        ) == 1, "can't determine unique project in {}. you should provide name by yourself.".format(
            found_modules)
        package_name = found_modules[0]
    relative_path = source_path.relative_to(path_candidates[0])
    relative_path = relative_path.parent / _get_mod_name_from_path(
        relative_path)
    return [package_name, *relative_path.parts]


def is_path_in_package(path):
    return locate_top_package(path) is not None


def import_from_path(path, mod_name=None):
    path = Path(path)
    if mod_name is None:
        mod_name = path.name.split(".")[0]
    spec = importlib.util.spec_from_file_location(mod_name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module

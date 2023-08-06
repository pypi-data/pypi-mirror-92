"""register ast hooks for top-level functions and class member functions, 
make function can be modified during runtime.
"""

import abc
import atexit
import functools
import importlib
import inspect
import json
import os
import ast 
import re
import threading
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple, Type, Union
import yaml 
from hookpy import compat, funcid, loader
from hookpy.constants import HOOKPY_CONFIG_PATH, HOOKPY_ENABLE
from hookpy.funcid import try_remove_decorator

_FUNC_ID_TO_HOOKS = {}  # type: Dict[str, List["Hook"]]

_LOCK = threading.Lock()


def read_config(config_path: str):
    config_path = Path(config_path)
    with config_path.open("r") as f:
        data = yaml.safe_load(f)
    return data


class HookConfig:
    def __init__(self, config_path: Union[Path, str], config: Dict[str, Any]):
        self.hook_folders = config.get("folders", [])  # type: List[str]
        self.hook_projects = config.get("projects", [])  # type: List[str]
        self.func_excludes = [
            re.compile(s) for s in config.get("func_excludes", [])
        ]
        self.folder_excludes = [
            re.compile(s) for s in config.get("folder_excludes", [])
        ]
        self.module_excludes = [
            re.compile(s) for s in config.get("module_excludes", [])
        ]
        self.config_path = Path(config_path)

        self.disable_class_decorator = config.get("disable_class_decorator", False)
        self.disable_function_decorator = config.get("disable_function_decorator", False)
        funcid_root = config.get("funcid_root", None)
        if "root" in config:
            self.root = Path(config["root"])
            if not self.root.is_absolute():
                self.root = self.config_path.parent / self.root
        else:
            self.root = self.config_path.parent
        if funcid_root is None:
            funcid_root = self.root 
        else:
            funcid_root = Path(funcid_root)
            if not funcid_root.is_absolute():
                funcid_root = self.config_path.parent / funcid_root
        self.funcid_root = funcid_root

        self.hooks_config = config["hooks"]
        # if dir in hook_folders is relative, use config_path to convert it
        # to absolute
        for i, folder in enumerate(self.hook_folders):
            folder_p = Path(folder)
            if not folder_p.is_absolute():
                folder_p = self.config_path.parent / folder_p
            self.hook_folders[i] = str(folder_p)

        for proj in self.hook_projects:
            path = Path(loader.locate_package(proj))
            if path.is_file():
                self.hook_folders.append(str(path.parent))
            else:
                self.hook_folders.append(str(path))

        for proj in self.module_excludes:
            path = Path(loader.locate_package(proj))
            if path.is_file():
                self.folder_excludes.append(str(path.parent))
            else:
                self.folder_excludes.append(str(path))

    def get_hook_classes(
            self
    ) -> Generator[Tuple[Type["Hook"], Dict[str, Any]], None, None]:
        for hook_cfg in self.hooks_config:
            name = hook_cfg["type"]
            config = hook_cfg.get("config", None)  # type: Dict[str, Any]
            if not config:
                config = {}

            hook_cls = funcid.get_module_object_by_imp_id(name)
            yield (hook_cls, config)


HOOK_CONFIG = None  # type: Optional[HookConfig]


def init_hook_config():
    global HOOK_CONFIG
    if HOOKPY_ENABLE:
        HOOK_CONFIG = HookConfig(HOOKPY_CONFIG_PATH,
                                 read_config(HOOKPY_CONFIG_PATH))

def get_hook_config():
    return HOOK_CONFIG

def enable_hook():
    global HOOKPY_ENABLE
    HOOKPY_ENABLE = True


def disable_hook():
    global HOOKPY_ENABLE
    HOOKPY_ENABLE = False


def set_config_path(path: str):
    global HOOKPY_CONFIG_PATH
    HOOKPY_CONFIG_PATH = path


def find_enable_hook(func_id):
    if not HOOKPY_ENABLE:
        return None
    if func_id not in _FUNC_ID_TO_HOOKS:
        return None
    hooks = _FUNC_ID_TO_HOOKS[func_id]
    impl = None
    if len(hooks) == 1:
        hook = hooks[0]
        if hook.enabled():
            hook.is_enabled(True)
            impl = hook.get_impl()
        else:
            hook.is_enabled(False)
        return impl
    found = False
    for i in range(len(hooks)):
        hook = hooks[i]
        if hook.enabled() and not found:
            impl = hook.get_impl()
            found = True
            hook.is_enabled(True)
        else:
            hook.is_enabled(False)
    # reorder hooks, ensure every hook can be called.
    with _LOCK:
        hooks.insert(0, hooks.pop())
    return impl


def register_hook(func=None):
    def wrapper(func):
        # TODO try to disable hook execution before import finished
        if not HOOKPY_ENABLE:
            return func
        if compat.Python3_6AndLater:
            if inspect.isasyncgenfunction(func):
                return func

        # we need to know the function type, regular/generator/async/async generator
        # with/async with isn't supported.
        func_without_deco = try_remove_decorator(func)
        func_meta = funcid.get_func_metadata(func)
        node = func_meta.node 
        for p in func_meta.parents[::-1]:
            if isinstance(p, ast.ClassDef):
                if HOOK_CONFIG.disable_class_decorator and p.decorator_list:
                    return func
        if HOOK_CONFIG.disable_function_decorator and node.decorator_list:
            return func 
        if func_meta is None:
            return func
        path = func_meta.path
        # print("{}:{}".format(path, func_meta.lineno))
        func_id = func_meta.get_func_id()
        func_name = ""
        if func_id is None:
            # get full path
            func_id = func_meta.get_func_id(root=HOOK_CONFIG.funcid_root)
            # func_id = str(path) + "-" + local_parts
            _, _, local_parts = funcid.split_func_id(func_id)
            func_name = local_parts[-1]
        else:
            _, _, local_parts = funcid.split_func_id(func_id)
            func_name = local_parts[-1]
        # print("!!!", func_id, path, func_meta.lineno)

        func_meta.func_id = func_id  # TODO remove this
        if func_name == "__getattr__":
            # __getattr__ may cause inf recursive call
            return func
        if func_name == "__setattr__":
            return func

        for pattern in HOOK_CONFIG.func_excludes:
            if pattern.match(func_name):
                return func
        with _LOCK:
            if func_id in _FUNC_ID_TO_HOOKS:
                return func
            hooks = []
            for hook_cls, config in HOOK_CONFIG.get_hook_classes():
                hook = hook_cls(**config)
                if hook.create_impl(func_meta, func):
                    hooks.append(hook)
            if hooks:
                _FUNC_ID_TO_HOOKS[func_id] = hooks
            else:
                return func
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapped(*args, **kw):
                impl = find_enable_hook(func_id)
                if not impl:
                    impl = func
                return await impl(*args, **kw)

            return async_wrapped
        if inspect.isgeneratorfunction(func):

            @functools.wraps(func)
            def generator_wrapped(*args, **kw):
                impl = find_enable_hook(func_id)
                if not impl:
                    impl = func
                yield from impl(*args, **kw)

            return generator_wrapped
        else:

            @functools.wraps(func)
            def regular_wrapped(*args, **kw):
                impl = find_enable_hook(func_id)
                if not impl:
                    impl = func
                return impl(*args, **kw)

            return regular_wrapped

    if func is None:
        return wrapper
    else:
        return wrapper(func)


class Hook(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def create_impl(self, func_meta: funcid.FuncMetadata, func) -> bool:
        """hook init impl. if failed, return a False,
        this hook won't be added to collection.
        """

    @abc.abstractmethod
    def get_impl(self):
        """get a impl.
        """

    @abc.abstractmethod
    def enabled(self) -> bool:
        """this hook may not be used even if it return True. 
        keep in mind that to minimize running overhead, the hook impl
        shouldn't be used for all time.
        """

    @abc.abstractmethod
    def is_enabled(self, enabled: bool):
        """reset your state here.
        """

    def handle_exit(self):
        return


def _hook_exit():
    for _, hooks in _FUNC_ID_TO_HOOKS.items():
        for h in hooks:
            h.handle_exit()


atexit.register(_hook_exit)

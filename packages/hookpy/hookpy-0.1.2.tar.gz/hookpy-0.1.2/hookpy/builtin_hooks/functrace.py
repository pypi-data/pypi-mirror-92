import functools
import inspect
from typing import Optional

from hookpy import Hook, compat, funcid


class FuncTracePrint(Hook):
    def __init__(self):
        self.impl = None
        self.meta = None  # type: Optional[funcid.FuncMetadata]

    def create_impl(self, func_meta: funcid.FuncMetadata, func) -> bool:
        isasyncgen = False or (compat.Python3_6AndLater
                               and inspect.isasyncgenfunction(func))
        self.meta = func_meta
        if not inspect.iscoroutinefunction(func) and not isasyncgen:
            func_id = func_meta.func_id

            @functools.wraps(func)
            def wrapped(*args, **kw):
                print(func_id)
                return func(*args, **kw)

            self.impl = wrapped
            return True
        return False

    def get_impl(self):
        return self.impl

    def enabled(self) -> bool:
        return True

    def is_enabled(self, enabled: bool):
        return

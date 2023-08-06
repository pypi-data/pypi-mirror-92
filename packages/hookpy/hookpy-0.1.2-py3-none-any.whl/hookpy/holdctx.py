"""

we must call hookpy.hold() in a function. the function must not be nested.
never use hookpy.hold() in multi-thread context, we can't determine which thread should execute code.
when call hookpy.hold(), 
1. origin code will stop, origin globals/locals will be captured
2. a loop will start to watch code change in this function id and below the hookpy.hold context.
3. if code changed in this file, new globals will be generated.
4. if code changed in this hold context, code will be executed with globals and captured locals.
TODO how to deal with module reload?
hookpy.hold(mods_reload=["codeai", ...])

Watch logic
1. start to analysis file if file changed
2. if change happens inside this function id, determine is inside hookpy.hold() context.
3. if change happens in other global space, we reload globals.

Stop logic
only one hookpy.hold() is allowed in a function id.
if hookpy.hold() is disappear, the origin program will resume.
TODO hold_async

"""

import ast
from pathlib import Path 
import inspect
from hookpy import loader 
from typing import Optional, List, Dict, Union, Any
import contextlib 
import time 
from hookpy import funcid 
import traceback


@contextlib.contextmanager
def hold(mods_reload: Optional[List[str]] = None, duration=0.2, reload_file=True, verbose=False):
    # TODO mods_reload
    # capture prev locals
    frame = inspect.currentframe().f_back.f_back
    # get unique function id
    prev_lineno = frame.f_lineno
    file_name = Path(frame.f_code.co_filename)
    if not file_name.exists():
        print("your file not exist", file_name)
        yield 
        return
    first_lineno = frame.f_code.co_firstlineno
    _locals = frame.f_locals
    _globals = frame.f_globals
    del frame
    prev_hold_source = None
    with open(str(file_name), "r") as f:
        file_source = f.read()
    prev_source = file_source 
    prev_source_except_hold = ""
    func_node = None 
    namespaces = None 
    local_fid = ""
    while True:
        if prev_hold_source is None:
            file_source = prev_source
        else:
            if not file_name.exists():
                break
            with open(str(file_name), "r") as f:
                file_source = f.read()
            if file_source == prev_source:
                time.sleep(duration)
                continue
        prev_source = file_source
        source_lines = file_source.split("\n")
        try:
            tree = ast.parse(file_source)
        except SyntaxError:
            traceback.print_exc()
            continue
        func_node = None 
        if prev_hold_source is None:
            # first time
            func_node_ns = funcid.find_toplevel_func_node_by_lineno(tree, first_lineno)
            # find with xxx.hold()
            if func_node_ns is None:
                break
            func_node, namespaces = func_node_ns
            local_fid = ".".join([n.name for n in namespaces] + [func_node.name])
        else:
            toplevels = funcid.get_toplevel_func_node(tree)
            for func_node_can, ns in toplevels:
                local_fid_can = ".".join([n.name for n in ns] + [func_node_can.name])
                if local_fid_can == local_fid:
                    func_node = func_node_can
                    break 
        if func_node is None:
            # that function is disappear. return
            raise RuntimeError("function disappear. exit")
        func_first_lineno = func_node.lineno
        deco_list = func_node.decorator_list
        # fix lineno to match inspect
        if len(deco_list) > 0:
            func_first_lineno = min([d.lineno for d in deco_list])
        func_end_lineno = func_node.body[-1].lineno 
        for n in ast.walk(func_node.body[-1]):
            if hasattr(n, "lineno"):
                func_end_lineno = max(func_end_lineno, n.lineno)
        hold_context_node = None 
        # TODO better way to find hold context.
        for node in ast.walk(func_node):
            if isinstance(node, ast.With):
                for with_item in node.items:
                    for name_node in ast.walk(with_item):
                        if isinstance(name_node, ast.Attribute):
                            if name_node.attr == hold.__name__:
                                # we found the hold stmt.
                                hold_context_node = node
                                break 
                        elif isinstance(name_node, ast.Name):
                            if name_node.id == hold.__name__:
                                # we found the hold stmt.
                                hold_context_node = node
                                break 
                    if hold_context_node is not None:
                        break 
            if hold_context_node is not None:
                break
        if hold_context_node is None:
            print("hold_context_node not found. break")
            break
        with_end_lineno = hold_context_node.body[-1].lineno 
        for n in ast.walk(hold_context_node.body[-1]):
            if hasattr(n, "lineno"):
                with_end_lineno = max(with_end_lineno, n.lineno)

        with_body_first_lineno = hold_context_node.body[0].lineno
        with_body_first_col_offset = hold_context_node.body[0].col_offset
        # extract body code
        lines = source_lines[with_body_first_lineno-1:with_end_lineno].copy()
        lines = [l[with_body_first_col_offset:].rstrip() for l in lines]
        lines = funcid.clean_source_code(lines)
        source = "\n".join(lines)
        # TODO clean comments
        lines_except_hold = source_lines[:func_first_lineno-1].copy()
        lines_except_hold += source_lines[func_end_lineno:].copy()
        lines_except_hold = funcid.clean_source_code(lines_except_hold)
        source_except_hold = "\n".join(lines_except_hold)

        if prev_hold_source is None:
            time.sleep(duration)
            prev_hold_source = source
            prev_source_except_hold = source_except_hold
            continue 
        code_block_equal = source == prev_hold_source
        code_except_hold_equal = prev_source_except_hold == source_except_hold
        if not code_except_hold_equal and reload_file:
            if verbose:
                print("module reload")
            mod = loader.import_from_path(file_name)
            _globals = mod.__dict__
            # mod = runpy.run_path()
        prev_source_except_hold = source_except_hold
        if code_block_equal:
            time.sleep(duration)
            continue 
        prev_hold_source = source
        print("-----Exec {}-----".format(local_fid))
        try:
            exec(source, _globals, _locals)
        except Exception as e:
            traceback.print_exc()
        time.sleep(duration)
    yield 
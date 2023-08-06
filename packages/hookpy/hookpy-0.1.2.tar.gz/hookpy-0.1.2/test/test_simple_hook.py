import contextlib
import importlib
import io
from pathlib import Path

import hookpy
from hookpy import hookimport
from hookpy.testtools import fake_project


def test_simple_hook():
    with fake_project(Path(__file__).parent / "fake_project") as (proj_name,
                                                                  proj_path):
        config_path = proj_path / proj_name / "hook-config.json"
        hookpy.core.set_config_path(config_path)
        hookpy.core.enable_hook()
        hookpy.core.init_hook_config()

        hookimport.install_register_hook(hookpy.core.HOOK_CONFIG.hook_folders)

        mod = importlib.import_module(proj_name)
        ss = io.StringIO("")
        with contextlib.redirect_stdout(ss):
            mod.add.add2(1, 2)
        values = ss.getvalue().strip().split("\n")
        assert len(values) == 2

        assert values[0] == proj_name + ".add-add2"
        assert values[1] == proj_name + ".add-add"

import hookpy 
import threading 
import tempfile 
import subprocess
import time 
import shutil 
from pathlib import Path 
import contextlib 
_GLOBAL_FUNC = """
def wtf():
    print("??")
    pass
"""

_SOURCE = """
import hookpy 
{global_func}
def main():
    print(5)
    a = 5
    b = 3 
    {hold}
{context}

if __name__ == "__main__":
    main()

"""

_HOLD_CONTEXT1 = """
        print(b)
        
"""

_HOLD_CONTEXT2 = """
        wtf( )
"""

@contextlib.contextmanager
def tempdir(delete=True):
    try:
        dirpath = tempfile.mkdtemp()
        dirpath = Path(dirpath)
        yield dirpath
    finally:
        if delete:
            shutil.rmtree(str(dirpath))


def test_hold():
    hold_stmt = "with hookpy.hold(verbose=True):"
    with tempdir() as folder:
        name = str(folder / "test.py")
        with Path(name).open("w") as f:
            source = _SOURCE.format(global_func="", context=_HOLD_CONTEXT1, hold=hold_stmt)
            f.write(source)
        proc = subprocess.Popen(["python", name], stdout=subprocess.PIPE)
        time.sleep(0.5)
        with Path(name).open("w") as f:
            f.write(_SOURCE.format(global_func=_GLOBAL_FUNC, context=_HOLD_CONTEXT1, hold=hold_stmt))
        time.sleep(0.5)
        with Path(name).open("w") as f:
            f.write(_SOURCE.format(global_func=_GLOBAL_FUNC, context=_HOLD_CONTEXT2, hold=hold_stmt))
        time.sleep(0.5)

        with Path(name).open("w") as f:
            f.write(_SOURCE.format(global_func=_GLOBAL_FUNC, context="", hold=""))
        stdout, _ = proc.communicate(timeout=0.5)
        stdouts = stdout.decode("utf-8").strip().split("\n")
        stdouts = [l.strip() for l in stdouts]
        assert stdouts == ['5', 'module reload', '-----Exec main-----', '??', 'hold_context_node not found. break', '3']

if __name__ == "__main__":
    test_hold()
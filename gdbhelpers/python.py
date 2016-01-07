# $_python function.

import gdb
import sys

## If python > 3.4??
if sys.version_info[0] > 2:
        import importlib
        from importlib import reload

class Python(gdb.Function):
    """$_python - evaluate a Python expression

Usage:
    $_python(STR)

This function evaluates a Python expression and returns
the result to gdb.  STR is a string which is parsed and evalled."""

    def __init__(self):
        gdb.write("init python helper: \n")
        super(Python, self).__init__('_python')

    def invoke(self, expr):
        return eval(expr.string())

Python()

class PyReload(gdb.Command):
    """$reload python modules
"""

    def __init__(self):
        gdb.write("init python reload helper: \n")
        super(PyReload, self).__init__("reload", gdb.COMMAND_DATA)

    def invoke(self, arg, from_tty):
        argv = gdb.string_to_argv(arg)
        if len(argv) == 0:
            for mod in sys.modules.values():
                gdb.write("reload(" + mod + ")")
                reload(mod)
        else:
            for mod in argv:
                gdb.write (mod)
            gdb.write("\n");

        return

PyReload()

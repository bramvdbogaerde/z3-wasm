"""
This script reads from $ROOT/bindings/export_list.txt and returns a comma seperated list for use with EXPORTED_FUNCTIONS in emscripten
"""

import os

ROOT = os.environ.get("ROOT", os.getcwd())
BINDINGS = ROOT+"/bindings/"
EXPORT_LIST = BINDINGS+"/export_list.txt"
DEFAULT_EXPORTED = [ "_init_context", "_destroy_context", "_eval_smt2"]

with open(EXPORT_LIST, "r") as f:
    lines = [ line.strip() for line in f.readlines() ] + DEFAULT_EXPORTED
    fns = ",".join([ f"\"{line}\"" for line in lines ])
    print(f"[ {fns} ]")

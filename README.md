Z3 WASM
=========

This repository contains scripts that makes interaction
with the Z3 solver from a browser using WASM easier.

* `build.sh` contains commands to fetch and compile Z3 using emscripten.
* `api/` contains a C API which exposes the Z3 API to Javascript, and 
  the `api.js` file contains some glue code that enables easier interaction
  with the C API.
* `example/` contains an example of how to use the `api.c` module using a dynamically linked native version of the Z3 library, this cannot be used from the browser.
* `index.html` contains an example on how to load and use the Z3 Javascript glue code.

Both the location of the Z3 repository and the Z3 version can be controlled
using environment variables. `Z3_BASE_DIR` controls the location of the 
cloned Z3 repository, while `Z3_VERSION` alters the version that is 
fetched from Github.

## Binding Generator

The `bindgen` directory contains some Python scripts to automate generating Javascript bindings for the Z3 C Api.

Currently, all functions declared in `z3/src/api/z3.h` of the original Z3 source are used for the Javascript bindings, all `Z3_*`
types are treated as opaque pointers (i.e., just numbers from Javascript's point of view) except for `Z3_string` which is treated as a string.

As of yet, the bindings remains untested, so it might be possible that an incorrect type is assigned to a particular parameter which might
lead to undefined behaviour.

## Related repositories

Clément Pit-Claudel has performed similar steps as I have taken here. 
However, its scripts are meant to be used on Ubuntu or Debian derivates, 
and do not work nicely on other distributions of Linux. Furthermore, its
Z3 version is outdated, and numerous users have reported either compilation
issues or issues while using the library.



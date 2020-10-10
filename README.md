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

## Related repositories

Clément Pit-Claudel has performed similar steps as I have taken here. 
However, its scripts are meant to be used on Ubuntu or Debian derivates, 
and do not work nicely on other distributions of Linux. Furthermore, its
Z3 version is outdated, and numerous users have reported either compilation
issues or issues while using the library.



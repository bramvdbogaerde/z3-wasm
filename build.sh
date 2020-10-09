#!/bin/bash

if [ -z $Z3_BASE_DIR ]; then
   export Z3_BASE_DIR="$HOME/data/sources/z3/"
fi

function available() {
   echo "Checking if $1 is available"
   if ! [ -x $(command -v $1) ]; then
      echo "Error $1 is not installed" >&2
      exit 1
   fi
}

available emcc
available emconfigure

mkdir -p out

emcc api/api.c $Z3_BASE_DIR/build/libz3.a -s EXPORTED_FUNCTIONS='["_init_context", "_destroy_context", "_eval_smt2"]' -s DISABLE_EXCEPTION_CATCHING=0 -s EXCEPTION_DEBUG=1 -I $Z3_BASE_DIR/src/api/ --post-js api/api.js -o out/z3.js

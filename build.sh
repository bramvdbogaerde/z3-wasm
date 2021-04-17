#!/usr/bin/env bash

if [ -z $Z3_BASE_DIR ]; then
   export Z3_BASE_DIR="$PWD/z3"
fi

if [ -z $Z3_VERSION ]; then
   export Z3_VERSION="z3-4.8.10"
fi

export ROOT=$PWD

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
mkdir -p $Z3_BASE_DIR

cd $Z3_BASE_DIR
git clone https://github.com/Z3Prover/z3 .
git fetch --all --tags
git checkout $Z3_VERSION 

emconfigure python scripts/mk_make.py --staticlib
cd build
emmake make -j$(nproc)

cd $ROOT

export EM_CACHE=$HOME/.emscripten/
emcc api/api.c $Z3_BASE_DIR/build/libz3.a -s EXPORTED_FUNCTIONS='["_init_context", "_destroy_context", "_eval_smt2"]' -s DISABLE_EXCEPTION_CATCHING=0 -s EXCEPTION_DEBUG=1 -I $Z3_BASE_DIR/src/api/ --post-js api/api.js -o out/z3.js

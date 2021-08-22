#!/usr/bin/env bash


# TODO: check whether libclang is available and try to regenerate bindings

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

mkdir -p out/cache
mkdir -p $Z3_BASE_DIR

cd $Z3_BASE_DIR
git clone https://github.com/Z3Prover/z3 .
git fetch --all --tags
git checkout $Z3_VERSION 

export CXXFLAGS="-pthread -s DISABLE_EXCEPTION_CATCHING=0 -s USE_PTHREADS=1"
export LDFLAGS="-s USE_PTHREADS=1"
emconfigure python scripts/mk_make.py --staticlib 
cd build
emmake make -j$(nproc)

cd $ROOT

export EM_CACHE=$HOME/.emscripten/
emcc api/api.c $Z3_BASE_DIR/build/libz3.a -fexceptions -pthread -s EXPORTED_FUNCTIONS=$(python3 bindgen/export_list.py) -s DISABLE_EXCEPTION_CATCHING=0 -s EXCEPTION_DEBUG=1 -s USE_PTHREADS=1 -s PTHREAD_POOL_SIZE=4 -s TOTAL_MEMORY=1GB -I $Z3_BASE_DIR/src/api/ --post-js api/api.js -o out/z3.js

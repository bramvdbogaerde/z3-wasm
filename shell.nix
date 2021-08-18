{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs ; [ clang emscripten ];
  EM_CACHE = "./cache";
}

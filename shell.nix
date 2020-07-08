{ pkgs ? import <nixpkgs> {} }:
with pkgs;
mkShell {
  VENV = "env";
  buildInputs = [
    git
    python36Full
    zlib
    docker
  ];
  shellHook = ''
    export PYTHONPATH=`pwd`/$VENV/${python.sitePackages}:$PYTHONPATH
    export LD_LIBRARY_PATH=${lib.makeLibraryPath [stdenv.cc.cc]}
  '';
}

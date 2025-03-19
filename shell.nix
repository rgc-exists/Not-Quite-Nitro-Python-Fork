{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  venvDir = ".venv";
  buildInputs = with pkgs; [
    python312
    python312Packages.venvShellHook
  ];

  postVenvCreation = ''
    pip install -r requirements.txt
  '';
}

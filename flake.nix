{
  description = "PowerMate control development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          evdev
          pygobject3  # For GLib/Gio
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            pamixer
            gobject-introspection  # For GI typelib files
            glib
            
            # Development tools
            git
            nixpkgs-fmt
          ];

          shellHook = ''
            echo "PowerMate development environment activated!"
            echo "Python version: $(python --version)"
          '';
        };
      }
    );
}
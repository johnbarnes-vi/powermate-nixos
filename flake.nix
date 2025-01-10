{
  description = "Griffin PowerMate Volume Controller for NixOS";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      nixosModules.default = import ./module.nix;
      
      packages = forAllSystems (system: {
        default = nixpkgs.legacyPackages.${system}.python3.pkgs.buildPythonApplication {
          pname = "powermate-controller";
          version = "0.1.0";
          format = "setuptools";  # Explicitly set the format
          src = ./src;
          propagatedBuildInputs = with nixpkgs.legacyPackages.${system}.python3.pkgs; [
            evdev
          ];
          # Add these checks to help debug any import issues
          pythonImportsCheck = [ "powermate_controller" ];
          doCheck = false;  # Skip tests for now
        };
      });
    };
}
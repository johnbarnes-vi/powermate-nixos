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
          src = ./src;
          propagatedBuildInputs = with nixpkgs.legacyPackages.${system}.python3.pkgs; [
            evdev
          ];
        };
      });
    };
}
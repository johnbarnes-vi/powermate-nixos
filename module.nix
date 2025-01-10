{ config, lib, pkgs, ... }:

with lib;

let
  cfg = config.services.powermate-controller;
in {
  options.services.powermate-controller = {
    enable = mkEnableOption "Griffin PowerMate Volume Controller";
    
    package = mkOption {
      type = types.package;
      description = "The PowerMate controller package";
      default = pkgs.python3.pkgs.buildPythonApplication {
        pname = "powermate-controller";
        version = "0.1.0";
        format = "setuptools";
        src = ./src;
        propagatedBuildInputs = with pkgs.python3.pkgs; [
          evdev
        ];
        pythonImportsCheck = [ "powermate_controller" ];
        doCheck = false;
      };
    };
  };

  config = mkIf cfg.enable {
    systemd.user.services.powermate-controller = {
      description = "Griffin PowerMate Volume Controller";
      wantedBy = [ "graphical-session.target" ];
      after = [ "graphical-session.target" ];
      
      serviceConfig = {
        ExecStart = "${cfg.package}/bin/powermate_controller";
        Restart = "always";
        RestartSec = 3;
      };
    };

    services.udev.extraRules = ''
      SUBSYSTEM=="input", ATTRS{idVendor}=="077d", ATTRS{idProduct}=="0410", MODE="0666", GROUP="input"
    '';

    users.groups.input = {};
  };
}
{ config, pkgs, inputs, ... }:

{
  env = {
    PROJECTNAME = "pystdlib";
    GREEN = "\\033[0;32m";
    NC = "\\033[0m"; # No Color
  };

  scripts.hello.exec = ''echo -e "''${GREEN}welcome to $PROJECTNAME''${NC}"'';

  imports = [ inputs.nur.nixosModules.nur ];

  packages = with pkgs; with config.nur.repos; with inputs.nixpkgs-future.legacyPackages."x86_64-linux"; [
    cloc
    gitFull
    gitAndTools.git-crypt
    just
    tagref
    vim
    python311Packages.papis-python-rofi
    python311Packages.xlib
    python311Packages.pygit2
    python311Packages.dmenu-python
    python311Packages.pyfzf
    python311Packages.notify2
  ];

  enterShell = ''
    hello
  '';

  difftastic.enable = true;

  languages.python = {
    enable = true;
    package = pkgs.python311;
  };

  pre-commit.hooks = {
    shfmt.enable = true;
    typos.enable = true;
  };
}

#!/usr/bin/python
# -*- coding: utf-8 -*-

# arguments.py file is part of slpkg.

# Copyright 2014-2015 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Slpkg is a user-friendly package manager for Slackware installations

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from repolist import RepoList
from __metadata__ import MetaData as _m


def options():
    """Slpkg is a user-friendly package manager for Slackware installations
                                                 _       _
                                             ___| |_ __ | | ____ _
                                            / __| | '_ \| |/ / _` |
                                            \__ \ | |_) |   < (_| |
                                            |___/_| .__/|_|\_\__, |
                                                  |_|        |___/

Commands:
   update                                   Run this command to update all
                                            the packages list.
   upgrade                                  Delete and recreate all packages
                                            lists.
   repo-add [repository name] [URL]         Add custom repository.
   repo-remove [repository]                 Remove custom repository.
   repo-list                                Print a list of all the
                                            repositories.
   repo-info [repository]                   Get information about a
                                            repository.
   update slpkg                             Upgrade the program directly from
                                            repository.

Optional arguments:
  -h, --help                                Print this help message and exit
  -v, --version                             Print program version and exit.
  -a, [script.tar.gz] [source...]           Auto build SBo packages.
                                            If you already have downloaded the
                                            script and the source code you can
                                            build a new package with this
                                            command.
  -b, [package...] --add, --remove          Manage packages in the blacklist.
      list                                  Add or remove packages and print
                                            the list. Each package is added
                                            here will not be accessible by the
                                            program.
  -q, [package...] --add, --remove          Manage SBo packages in the queue.
      list, build, install, build-install   Add or remove and print the list
                                            of packages. Build and then install
                                            the packages from the queue.
  -g, config, config=[editor]               Configuration file management.
                                            Print the configuration file or
                                            edit.
  -l, [repository], --index, --installed    Print a list of all available
                                            packages repository, index or print
                                            only packages installed on the
                                            system.
  -c, [repository] --upgrade, --skip=[]     Check the install upgraded packages
                                            from repositories.
  -s, [repository] [package...]             Sync packages. Install packages
                                            directly from remote repositories
                                            with all dependencies.
  -t, [repository] [package]                Track package dependencies and
                                            print package dependenies tree with
                                            highlight if packages is installed.
  -p, [repository] [package], --color=[]    Print description of a package
                                            directly from the repository and
                                            change color text.
  -n, [package]                             View a standard of SBo page in
                                            terminal and manage multiple options
                                            like reading, downloading, building
                                            installation, etc.
  -F, [package...]                          Find packages from repositories and
                                            search at each enabled repository
                                            and prints results.
  -f, [package...]                          Find and print installed packages
                                            reporting the size and the sum.
  -i, [package...]                          Installs single or multiple
                                            Slackware binary packages (*.t?z).
  -u, [package...]                          Upgrade single or multiple Slackware
                                            binary packages from a older to a
                                            newer one.
  -o, [package...]                          Reinstall signle or multiple
                                            Slackware binary packages with the
                                            same packages if the exact.
  -r, [package...]                          Removes a previously installed
                                            Slackware binary packages.
  -d, [package...]                          Display the packages contents and
                                            file list.

You can read more about slpkg from manpage or see examples from readme file.
Homepage: https://github.com/dslackw/slpkg
"""
    print("\nslpkg - version {0} | Slackware release: {1}\n".format(
        _m.__version__, _m.slack_rel))
    print options.__doc__


def usage(repo):
    error_repo = ""
    if repo and repo not in _m.repositories:
        all_repos = RepoList().all_repos
        del RepoList().all_repos
        if repo in all_repos:
            error_repo = ("slpkg: error: repository '{0}' is not activated"
                          "\n".format(repo))
        else:
            error_repo = ("slpkg: error: repository '{0}' does not exist"
                          "\n".format(repo))
    view = [
        "\nslpkg - version {0} | Slackware release: {1}\n".format(
            _m.__version__, _m.slack_rel),
        "Usage: slpkg Commands:",
        "             [update] [upgrade] [repo-add [repository name] [URL]]",
        "             [repo-remove [repository]] [repo-list]",
        "             [repo-info [repository]] [update [slpkg]]\n",
        "             Optional arguments:",
        "             [-h] [-v] [-a [script.tar.gz] [sources...]]",
        "             [-b list, [...] --add, --remove]",
        "             [-q list, [...] --add, --remove]",
        "             [-q build, install, build-install]",
        "             [-g config, config=[editor]]",
        "             [-l [repository], --index, --installed]",
        "             [-c [repository] --upgrade]",
        "             [-s [repository] [package...]",
        "             [-t [repository] [package]",
        "             [-p [repository] [package], --color=[]]",
        "             [-n [SBo package]] [-F [...]] [-f [...]] [-i [...]]",
        "             [-u [...]] [-o  [...]] [-r [...]] [-d [...]]\n",
        error_repo,
        "For more information try 'slpkg -h, --help' or view manpage\n"
    ]
    for usg in view:
        print(usg)

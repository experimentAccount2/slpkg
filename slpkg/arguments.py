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
    arguments = [
        "\nslpkg - version {0} | Slackware release: {1}\n".format(
            _m.__version__, _m.slack_rel),
        "Slpkg is a user-friendly package manager for Slackware "
        "installations\n",
        "Commands:",
        "   update                                   Run this command to update all",
        "                                            the packages list.",
        "   upgrade                                  Delete and recreate all packages",
        "                                            lists.",
        "   repo-add [repository name] [URL]         Add custom repository.",
        "   repo-remove [repository]                 Remove custom repository.",
        "   repo-list                                Print a list of all the",
        "                                            repositories.",
        "   repo-info [repository]                   Get information about a",
        "                                            repository.",
        "   update slpkg                             Upgrade the program directly from",
        "                                            repository.\n",
        "Optional arguments:",
        "  -h, --help                                print this help message and exit",
        "  -v, --version                             print program version and exit.",
        "  -a, [script.tar.gz] [source...]           Auto build SBo packages.",
        "                                            If you already have downloaded the",
        "                                            script and the source code you can",
        "                                            build a new package with this",
        "                                            command.",
        "  -b, [package...] --add, --remove          Manage packages in the blacklist. ",
        "      list                                  Add or remove packages and print",
        "                                            the list. Each package is added",
        "                                            here will not be accessible by the",
        "                                            program.",
        "  -q, [package...] --add, --remove          Manage SBo packages in the queue.",
        "      list, build, install, build-install   Add or remove and print the list",
        "                                            of packages. Build and then install",
        "                                            ths packages from the queue.",
        "  -g, config, config=[editor]               Configuration file management.",
        "                                            Print the configuration file or",
        "                                            edit.",
        "  -l, [repository], --index, --installed    List of repositories packages.",
        "                                            Print a list of all available",
        "                                            packages repository, index or print",
        "                                            only packages installed on the",
        "                                            system.",
        "  -c, [repository] --upgrade                Check and print of available",
        "                                            packages for upgrade.",
        "  -s, [repository] [package...]             Sync packages. Install packages",
        "                                            directly from remote repositories",
        "                                            with all dependencies.",
        "  -t, [repository] [package]                package tracking dependencies",
        "  -p, [repository] [package], --color=[]    print package description",
        "  -n, [package]                             view SBo site packages in terminal",
        "  -F, [package...]                          find packages from repositories",
        "  -f, [package...]                          find installed packages",
        "  -i, [package...]                          install binary packages",
        "  -u, [package...]                          upgrade binary packages",
        "  -o, [package...]                          reinstall binary packages",
        "  -r, [package...]                          remove binary packages",
        "  -d, [package...]                          display the package "
        "contents\n",
    ]
    for opt in arguments:
        print(opt)


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

#!/usr/bin/python
# -*- coding: utf-8 -*-

# blacklist.py file is part of slpkg.

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


from utils import Utils
from splitting import split_package
from __metadata__ import MetaData as _meta_


class BlackList(object):
    """Blacklist class to add, remove or listed packages
    in blacklist file."""
    def __init__(self):
        self.meta = _meta_
        self.quit = False
        self.blackfile = "/etc/slpkg/blacklist"
        self.black_conf = Utils().read_file(self.blackfile)

    def get_black(self):
        """Return blacklist packages from /etc/slpkg/blacklist
        configuration file."""
        blacklist = []
        for read in self.black_conf.splitlines():
            read = read.lstrip()
            if not read.startswith("#"):
                blacklist.append(read.replace("\n", ""))
        return blacklist

    def listed(self):
        """Print blacklist packages
        """
        print("\nPackages in blacklist:\n")
        for black in self.get_black():
            if black:
                print("{0}{1}{2}".format(self.meta.color["GREEN"], black,
                                         self.meta.color["ENDC"]))
                self.quit = True
        if self.quit:
            print("")   # new line at exit

    def add(self, pkgs):
        """Add blacklist packages if not exist
        """
        blacklist = self.get_black()
        pkgs = set(pkgs)
        print("\nAdd packages in blacklist:\n")
        with open(self.blackfile, "a") as black_conf:
            for pkg in pkgs:
                if pkg not in blacklist:
                    print("{0}{1}{2}".format(self.meta.color["GREEN"], pkg,
                                             self.meta.color["ENDC"]))
                    black_conf.write(pkg + "\n")
                    self.quit = True
            black_conf.close()
        if self.quit:
            print("")   # new line at exit

    def remove(self, pkgs):
        """Remove packages from blacklist
        """
        print("\nRemove packages from blacklist:\n")
        with open(self.blackfile, "w") as remove:
            for line in self.black_conf.splitlines():
                if line not in pkgs:
                    remove.write(line + "\n")
                else:
                    print("{0}{1}{2}".format(self.meta.color["RED"], line,
                                             self.meta.color["ENDC"]))
                    self.quit = True
            remove.close()
        if self.quit:
            print("")   # new line at exit

    def packages(self, pkgs, repo):
        """Return packages in blacklist or by repository
        """
        black = []
        for bl in self.get_black():
            pr = bl.split(":")
            for pkg in pkgs:
                # blacklist packages by repository priority
                if (pr[0] == repo and pr[1].startswith("*") and
                        pr[1].endswith("*")):
                    if repo == "sbo" and pr[1][1:-1] in pkg:
                        black.append(pkg)
                    elif pr[1][1:-1] in pkg:
                        black.append(split_package(pkg)[0])
                elif pr[0] == repo and pr[1].endswith("*"):
                    if repo == "sbo" and pkg.startswith(pr[1][:-1]):
                        black.append(pkg)
                    elif pkg.startswith(pr[1][:-1]):
                        black.append(split_package(pkg)[0])
                elif pr[0] == repo and pr[1].startswith("*"):
                    if repo == "sbo" and pkg.endswith(pr[1][1:]):
                        black.append(pkg)
                    elif pkg.endswith(pr[1][1:]):
                        black.append(split_package(pkg)[0])
                elif pr[0] == repo and "*" not in pr[1]:
                    if repo == "sbo":
                        black.append(pr[1])
                    else:
                        black.append(split_package(pkg)[0])
                # normal blacklist packages
                if bl.startswith("*") and bl.endswith("*"):
                    if repo == "sbo" and bl[1:-1] in pkg:
                        black.append(pkg)
                    elif bl[1:-1] in pkg:
                        black.append(split_package(pkg)[0])
                elif bl.endswith("*"):
                    if repo == "sbo" and pkg.startswith(bl[:-1]):
                        black.append(pkg)
                    elif pkg.startswith(bl[:-1]):
                        black.append(split_package(pkg)[0])
                elif bl.startswith("*"):
                    if repo == "sbo" and pkg.endswith(bl[1:]):
                        black.append(pkg)
                    elif pkg.endswith(bl[1:]):
                        black.append(split_package(pkg)[0])
            if bl not in black and "*" not in bl:
                black.append(bl)
        return black

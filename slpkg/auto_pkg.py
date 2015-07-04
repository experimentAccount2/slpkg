#!/usr/bin/python
# -*- coding: utf-8 -*-

# auto_pkg.py file is part of slpkg.

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


from messages import Msg
from pkg.manager import PackageManager
from __metadata__ import MetaData as _meta_


class Auto(object):

    def __init__(self, packages):
        self.packages = packages
        self.meta = _meta_
        self.commands = {
            "1": "installpkg",
            "2": "upgradepkg --install-new",
            "3": "upgradepkg --reinstall"
        }

    def select(self):
        print("\nFound Slackware binary package for installation:\n")
        for pkg in self.packages:
            print(" " + pkg.split("/")[-1])
        print("")
        Msg().template(78)
        print("| Chose a command:")
        Msg().template(78)
        for key in sorted(self.commands):
            print("| {0}. {1}{2}{3}".format(key, self.meta.color["GREEN"],
                                            self.commands[key],
                                            self.meta.color["ENDC"]))
        Msg().template(78)
        self.choice = raw_input(" > ")
        self.execute()

    def execute(self):
        if self.choice in self.commands.keys():
            if self.choice == "1":
                PackageManager(self.packages).install("")
            elif self.choice in ["2", "3"]:
                PackageManager(self.packages).upgrade(
                    self.commands[self.choice][11:])

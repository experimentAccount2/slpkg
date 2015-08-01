#!/usr/bin/python
# -*- coding: utf-8 -*-

# new_config.py file is part of slpkg.

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


import os

from __metadata__ import MetaData as _meta_


class NewConfig(object):

    def __init__(self):
        self.meta = _meta_
        self.red = self.meta.color["RED"]
        self.endc = self.meta.color["ENDC"]
        self.etc = "/etc/"
        self.news = []

    def find_new(self):
        """Find all '.new' files from /etc/ folder
        and subfolders
        """
        print("\nSearch for .new configuration files:\n")
        for path, dirs, files in os.walk(self.etc):
            for f in files:
                if f.endswith(".new"):
                    self.news.append(os.path.join(path, f))

    def view_new(self):
        """print .new configuration files
        """
        self.find_new()
        for n in self.news:
            print("{0}".format(n))
        print("\nInstalled {0} new configuration files:\n".format(
            len(self.news)))
        self.choices()

    def choices(self):
        """Menu options for new configuration files
        """
        br = ""
        if self.meta.use_colors in ["off", "OFF"]:
            br = ")"
        print("     {0}O{1}{2}verwrite all old configuration files with new "
              "ones".format(self.red, self.endc, br))
        print("       The old files will be saved with suffix .old")
        print("     {0}R{1}{2}emove all .new files".format(
            self.red, self.endc, br))
        print("     {0}P{1}{2}rompt O, R, option for each single file\n".format(
            self.red, self.endc, br))
        choose = raw_input("What would you like to do [O/R/P]? ")
        if choose == "O":
            self.overwrite_all()
        elif choose == "R":
            self.remove_all()
        elif choose == "P":
            self.prompt()

    def overwrite_all(self):
        pass

    def remove_all(self):
        pass

    def prompt(self):
        for p in self.news:
            print("{0}".format(p))

    def _remove(self):
        pass

    def _overwrite(self):
        pass

NewConfig().view_new()

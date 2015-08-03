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
import shutil

from messages import Msg
from __metadata__ import MetaData as _meta_


class NewConfig(object):

    def __init__(self):
        self.meta = _meta_
        self.red = self.meta.color["RED"]
        self.endc = self.meta.color["ENDC"]
        self.br = ""
        if self.meta.use_colors in ["off", "OFF"]:
            self.br = ")"
        # self.etc = "/etc/"
        self.etc = "/home/dslackw/Downloads/test/"
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
        print("")
        Msg().template(78)
        print("| Installed {0} new configuration files:".format(
            len(self.news)))
        Msg().template(78)
        self.choices()

    def choices(self):
        """Menu options for new configuration files
        """
        print("| {0}O{1}{2}verwrite all old configuration files with new "
              "ones".format(self.red, self.endc, self.br))
        print("|  The old files will be saved with suffix .old")
        print("| {0}R{1}{2}emove all .new files".format(
            self.red, self.endc, self.br))
        print("| {0}K{1}{2}eep the old and .new files, no changes".format(
            self.red, self.endc, self.br))
        print("| {0}P{1}{2}rompt O, R, option for each single file".format(
            self.red, self.endc, self.br))
        Msg().template(78)
        choose = raw_input("\nWhat would you like to do [O/R/P]? ")
        if choose == "O":
            self.overwrite_all()
        elif choose == "R":
            self.remove_all()
        elif choose == "K":
            self.keep
        elif choose == "P":
            self.prompt()

    def overwrite_all(self):
        """Overwrite all .new files and keep
        old with suffix .old
        """
        for n in self.news:
            if os.path.isfile(n[:-4]):
                shutil.copy2(n[:-4], n[:-4] + ".old")
            if os.path.isfile(n):
                shutil.move(n, n[:-4])

    def remove_all(self):
        """Remove all .new files
        """
        for n in self.news:
            if os.path.isfile(n):
                os.remove(n)

    def prompt(self):
        print("")
        Msg().template(78)
        print("| Choose what to do file by file:")
        print("| {0}K{1}{2}epp, {3}O{4}{5}verwrite, {6}R{7}{8}emove, "
              "{9}D{10}{11}iff, {12}M{13}{14}erge".format(
                  self.red, self.endc, self.br, self.red, self.endc, self.br,
                  self.red, self.endc, self.br, self.red, self.endc, self.br,
                  self.red, self.endc, self.br))
        Msg().template(78)
        for n in self.news:
            self.question(n)

    def question(self, n):
        prompt_ask = raw_input("{0} [K/O/R/D/M]? ".format(n))
        if prompt_ask == "O":
            self._overwrite(n)

    def _remove(self):
        pass

    def _overwrite(self, n):
        if os.path.isfile(n[:-4]):
            shutil.copy2(n[:-4], n[:-4] + ".old")
        if os.path.isfile(n):
            shutil.move(n, n[:-4])

    def keep(self):
        pass

NewConfig().view_new()

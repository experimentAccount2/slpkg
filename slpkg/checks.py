#!/usr/bin/python
# -*- coding: utf-8 -*-

# checks.py file is part of slpkg.

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
from arguments import usage
from sbo.check import sbo_upgrade
from slack.patches import Patches
from binary.check import pkg_upgrade
from __metadata__ import MetaData as _meta_


class Updates(object):

    def __init__(self, repo):
        self.repo = repo
        self.meta = _meta_

    def run(self):
        if self.repo in self.meta.repositories:
            if self.repo == "sbo":
                self.check = len(sbo_upgrade(skip=""))
            elif self.repo == "slack":
                if self.meta.only_installed in ["on", "ON"]:
                    self.check = len(pkg_upgrade(self.repo, skip=""))
                else:
                    self.check = Patches(skip="", flag="").store()
                    Msg().done()
            else:
                self.check = len(pkg_upgrade(self.repo, skip=""))
            self.status()
        else:
            usage(self.repo)

    def status(self):
        if self.check > 1:
            print("\nNews in ChangeLog.txt\n")
        else:
            print("\nNo changes in ChangeLog.txt\n")

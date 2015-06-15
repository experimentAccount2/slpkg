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

from arguments import usage
from init import Initialization
from __metadata__ import MetaData as _meta_


class Updates(object):
    """Checking for news in ChangeLog.txt
    """
    def __init__(self, repo):
        self.repo = repo
        self.meta = _meta_
        self.check = 2
        self.st = ""
        self._init = Initialization(True)
        self.all_repos = {
            "slack": self._init.slack,
            "sbo": self._init.sbo,
            "rlw": self._init.rlw,
            "alien": self._init.alien,
            "slacky": self._init.slacky,
            "studio": self._init.studio,
            "slackr": self._init.slackr,
            "slonly": self._init.slonly,
            "ktown": self._init.ktown,
            "multi": self._init.multi,
            "slacke": self._init.slacke,
            "salix": self._init.salix,
            "slackl": self._init.slackl,
            "rested": self._init.rested,
            "msb": self._init.msb
        }

    def run(self):
        """Run and check if new in ChangeLog.txt
        """
        if self.repo in self.meta.default_repositories:
            try:
                self.check = self.all_repos[self.repo]()
            except OSError:
                usage(self.repo)
        elif self.repo in self.meta.repositories:
            self.check = self._init.custom(self.repo)
        else:
            usage(self.repo)
        self.status()
        print(self.st)

    def ALL(self):
        """Check ALL enabled repositories ChangeLogs
        """
        for repo in self.meta.repositories:
            if repo in self.meta.default_repositories:
                try:
                    self.check = self.all_repos[repo]()
                except OSError:
                    usage(self.repo)
            elif repo in self.meta.repositories:
                self.check = self._init.custom(repo)
            self.status()
            print("Repository '{0}':\n {1}".format(repo, self.st))

    def status(self):
        """Print messages
        """
        if self.check == 1:
            self.st = "\nNews in ChangeLog.txt\n"
        elif self.check == 0:
            self.st = "\nNo changes in ChangeLog.txt\n"

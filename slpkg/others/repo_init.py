#!/usr/bin/python
# -*- coding: utf-8 -*-

# repo_init.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
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

from repositories import Repo
from slpkg.__metadata__ import (
    lib_path,
    slacke_sub_repo,
    default_repositories
)

from slpkg.slack.slack_version import slack_ver


class RepoInit(object):
    '''
    Return PACKAGES.TXT and mirror by repository
    '''

    def __init__(self, repo):
        self.repo = repo
        self.mirror = ''

    def fetch(self):
        if self.repo in default_repositories:
            exec('self._init_{0}()'.format(self.repo))
        else:
            exec('self._init_custom()')

        f = open(self.lib, "r")
        PACKAGES_TXT = f.read()
        f.close()
        return PACKAGES_TXT, self.mirror

    def _init_custom(self):
        self.lib = lib_path + "{0}_repo/PACKAGES.TXT".format(self.repo)
        self.mirror = "{0}".format(Repo().custom_repository()[self.repo])

    def _init_rlw(self):
        self.lib = lib_path + "rlw_repo/PACKAGES.TXT"
        self.mirror = "{0}{1}/".format(Repo().rlw(), slack_ver())

    def _init_alien(self):
        self.lib = lib_path + "alien_repo/PACKAGES.TXT"
        self.mirror = Repo().alien()

    def _init_slacky(self):
        self.lib = lib_path + "slacky_repo/PACKAGES.TXT"
        arch = ""
        if os.uname()[4] == "x86_64":
            arch = "64"
        self.mirror = "{0}slackware{1}-{2}/".format(Repo().slacky(), arch,
                                                    slack_ver())

    def _init_studio(self):
        self.lib = lib_path + "studio_repo/PACKAGES.TXT"
        arch = ""
        if os.uname()[4] == "x86_64":
            arch = "64"
        self.mirror = "{0}slackware{1}-{2}/".format(Repo().studioware(),
                                                    arch, slack_ver())

    def _init_slackr(self):
        self.lib = lib_path + "slackr_repo/PACKAGES.TXT"
        self.mirror = Repo().slackers()

    def _init_slonly(self):
        self.lib = lib_path + "slonly_repo/PACKAGES.TXT"
        arch = "{0}-x86".format(slack_ver())
        if os.uname()[4] == "x86_64":
            arch = "{0}-x86_64".format(slack_ver())
        self.mirror = "{0}{1}/".format(Repo().slackonly(), arch)

    def _init_ktown(self):
        self.lib = lib_path + "ktown_repo/PACKAGES.TXT"
        self.mirror = Repo().ktown()

    def _init_multi(self):
        self.lib = lib_path + "multi_repo/PACKAGES.TXT"
        self.mirror = Repo().multi()

    def _init_slacke(self):
        arch = ""
        if os.uname()[4] == "x86_64":
            arch = "64"
        elif os.uname()[4] == "arm":
            arch = "arm"
        self.lib = lib_path + "slacke_repo/PACKAGES.TXT"
        self.mirror = "{0}slacke{1}/slackware{2}-{3}/".format(
            Repo().slacke(), slacke_sub_repo[1:-1], arch, slack_ver())

    def _init_salix(self):
        arch = "i486"
        if os.uname()[4] == "x86_64":
            arch = "x86_64"
        self.lib = lib_path + "salix_repo/PACKAGES.TXT"
        self.mirror = "{0}{1}/{2}/".format(Repo().salix(), arch, slack_ver())

    def _init_slackl(self):
        arch = "i486"
        if os.uname()[4] == "x86_64":
            arch = "x86_64"
        self.lib = lib_path + "slackl_repo/PACKAGES.TXT"
        self.mirror = "{0}{1}/current/".format(Repo().slackel(), arch)

    def _init_rested(self):
        self.lib = lib_path + "rested_repo/PACKAGES.TXT"
        self.mirror = Repo().restricted()

#!/usr/bin/python
# -*- coding: utf-8 -*-

# __metadata__.py

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# This program is free software: you can redistribute it and/or modify
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

__all__ = "slpkg"
__author__ = "dslackw"
__version_info__ = (2, 0, 4)
__version__ = "{0}.{1}.{2}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "d.zlatanidis@gmail.com"


f = open("/etc/slpkg/slpkg.conf", "r")
conf = f.read()
f.close()

''' temponary path '''
tmp = "/tmp/"

for line in conf.splitlines():
    line = line.lstrip()
    if line.startswith("VERSION"):
        slack_rel = line[8:].strip()
    if line.startswith("BUILD"):
        build_path = line[6:].strip()
    if line.startswith("PACKAGES"):
        slpkg_tmp_packages = line[9:].strip()
    if line.startswith("PATCHES"):
        slpkg_tmp_patches = line[8:].strip()

if not slack_rel or slack_rel not in ['stable', 'current']:
    slack_rel = "stable"

if not build_path:
    build_path = "/tmp/slpkg/build/"
elif not build_path.endswith("/"):
    build_path = build_path + "/"

if not slpkg_tmp_packages:
    slpkg_tmp_packages = tmp + "slpkg/packages/"
elif not slpkg_tmp_packages.endswith("/"):
    slpkg_tmp_packages = slpkg_tmp_packages + "/"

if not slpkg_tmp_patches:
    slpkg_tmp_patches = tmp + "slpkg/patches/"
elif not slpkg_tmp_patches.endswith("/"):
    slpkg_tmp_patches = slpkg_tmp_patches + "/"

''' repositories '''
repositories = [
    "sbo",
    "slack",
    "rlw",
    "alien",
    "slacky"
]

''' file spacer '''
sp = "-"

''' current path '''
path = os.getcwd() + "/"

''' library path '''
lib_path = "/var/lib/slpkg/"

''' log path '''
log_path = "/var/log/slpkg/"

''' packages log files path '''
pkg_path = "/var/log/packages/"

''' blacklist conf path '''
bls_path = "/etc/slpkg/"

''' computer architecture '''
arch = os.uname()[4]

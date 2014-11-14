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


# temponary path
tmp = "/tmp/"

if not os.path.exists("/etc/slpkg"):
    os.mkdir("/etc/slpkg")

slpkg_conf = [
    "# Configuration file for slpkg\n",
    "\n",
    "# slpkg.conf file is part of slpkg.\n",
    "\n",
    "# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>\n",
    "# All rights reserved.\n",
    "\n",
    "# Utility for easy management packages in Slackware\n",
    "\n",
    "# https://github.com/dslackw/slpkg\n",
    "\n",
    "# Slpkg is free software: you can redistribute it and/or modify\n",
    "# it under the terms of the GNU General Public License as published by\n",
    "# the Free Software Foundation, either version 3 of the License, or\n",
    "# (at your option) any later version.\n",
    "# This program is distributed in the hope that it will be useful,\n",
    "# but WITHOUT ANY WARRANTY; without even the implied warranty of\n",
    "# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n",
    "# GNU General Public License for more details.\n",
    "# You should have received a copy of the GNU General Public License\n",
    "# along with this program. If not, see <http://www.gnu.org/licenses/>.\n",
    "\n",
    "# Slackware version 'stable' or 'current'.\n",
    "VERSION=stable\n",
    "\n",
    "# Build directory for repository slackbuilds.org. In this directory\n"
    "# downloaded sources and scripts for building.\n",
    "BUILD=/tmp/slpkg/build/\n",
    "\n",
    "# Download directory for others repositories that use binaries files\n"
    "# for installation.\n",
    "PACKAGES=/tmp/slpkg/packages/\n",
    "\n",
    "# Download directory for Slackware patches file.\n",
    "PATCHES=/tmp/slpkg/patches/\n"
    "\n",
    "# Delete all downloaded files if DEL_ALL is 'on'.\n",
    "DEL_ALL=on\n"
    "\n",
    "# Delete build directory after each process if DEL_BUILD is 'on'.\n",
    "DEL_BUILD=off\n"
]

if not os.path.isfile("/etc/slpkg/slpkg.conf"):
    with open("/etc/slpkg/slpkg.conf", "w") as conf:
        for line in slpkg_conf:
            conf.write(line)
        conf.close()

f = open("/etc/slpkg/slpkg.conf", "r")
conf = f.read()
f.close()

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
    if line.startswith("DEL_ALL"):
        del_all = line[8:].strip()
    if line.startswith("DEL_BUILD"):
        del_build = line[10:].strip()

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

if not del_all or del_all not in ['on', 'off']:
    del_all = "on"

if not del_build or del_build not in ['on', 'off']:
    del_build = "off"

# repositories
repositories = [
    "sbo",
    "slack",
    "rlw",
    "alien",
    "slacky"
]

# file spacer
sp = "-"

# current path
path = os.getcwd() + "/"

# library path
lib_path = "/var/lib/slpkg/"

# log path
log_path = "/var/log/slpkg/"

# packages log files path
pkg_path = "/var/log/packages/"

# blacklist conf path
bls_path = "/etc/slpkg/"

# computer architecture
arch = os.uname()[4]

#!/usr/bin/python
# -*- coding: utf-8 -*-

# build_check.py file is part of slpkg.

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


from slpkg.messages import Msg
from slpkg.splitting import split_package
from slpkg.__metadata__ import MetaData as _meta_

from slpkg.pkg.find import find_package

from slpkg.sbo.build_num import BuildNumber


def slack_package(prgnam):
    """Search for binary packages in output directory
    """
    binary = ""
    # Get build number from prgnam.SlackBuild script
    build1 = BuildNumber("", "-".join(prgnam.split("-")[:-1])).get()
    for pkg in find_package(prgnam + _meta_.sp, _meta_.output):
        # Get build number from binary package
        build2 = split_package(pkg[:-4])[3]
        if pkg[:-4].endswith("_SBo") and build1 == build2:
            binary = pkg
            break
    if not find_package(binary, _meta_.output):
        Msg().build_FAILED(prgnam)
        raise SystemExit()
    return ["".join(_meta_.output + binary)]

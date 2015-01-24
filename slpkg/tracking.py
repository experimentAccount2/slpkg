#!/usr/bin/python
# -*- coding: utf-8 -*-

# tracking.py file is part of slpkg.

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


from utils import (
    read_file,
    remove_dbs,
    dimensional_list
)
from messages import (
    template,
    msg_done,
    msg_resolving
)
from __metadata__ import (
    lib_path,
    pkg_path,
    color,
    sp
)

from pkg.find import find_package

from sbo.search import sbo_search_pkg
from sbo.dependency import Requires

from binary.search import search_pkg
from binary.dependency import Dependencies


def track_dep(name, repo):
    '''
    View tree of dependencies and also
    highlight packages with color green
    if allready installed and color red
    if not installed.
    '''
    msg_resolving()
    if repo == "sbo":
        dependencies_list = Requires().sbo(name)
        find_pkg = sbo_search_pkg(name)
    else:
        PACKAGES_TXT = read_file(lib_path + '{0}_repo/PACKAGES.TXT'.format(
            repo))
        dependencies_list = Dependencies(PACKAGES_TXT, repo).binary(name)
        find_pkg = search_pkg(name, repo)
    msg_done()
    if find_pkg:
        requires, dependencies = [], []
        requires = dimensional_list(dependencies_list)
        requires.reverse()
        dependencies = remove_dbs(requires)
        if dependencies == []:
            dependencies = ["No dependencies"]
        pkg_len = len(name) + 24
        print("")    # new line at start
        template(pkg_len)
        print("| Package {0}{1}{2} dependencies :".format(color['CYAN'], name,
                                                          color['ENDC']))
        template(pkg_len)
        print("\\")
        print(" +---{0}[ Tree of dependencies ]{1}".format(color['YELLOW'],
                                                           color['ENDC']))
        index = 0
        for pkg in dependencies:
            index += 1
            if find_package(pkg + sp, pkg_path):
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, color['GREEN'],
                                                  pkg, color['ENDC']))
            else:
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, color['RED'],
                                                  pkg, color['ENDC']))
        print("")    # new line at end
    else:
        print("\nNo package was found to match\n")

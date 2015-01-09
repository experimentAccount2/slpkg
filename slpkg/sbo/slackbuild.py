#!/usr/bin/python
# -*- coding: utf-8 -*-

# slackbuild.py file is part of slpkg.

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

import sys

from dependency import sbo_dependencies_pkg
from search import sbo_search_pkg
from __metadata__ import color
from messages import template


class SBoInstall(object):

    def __init__(self, slackbuilds):
        self.slackbuilds = slackbuilds
        sys.stdout.write("{0}Reading package lists ...{1}".format(
            color['GREY'], color['ENDC']))
        sys.stdout.flush()

    def start(self):
        self.slackbuilds = ['Flask', 'asdaf', 'PyAudio', 'PySDL2', 'flexget',
                            'werwer']

        self.deps = []
        self.package_not_found = []
        for dep in self.slackbuilds:
            if sbo_search_pkg(dep):
                self.deps += (sbo_dependencies_pkg(dep))
            else:
                self.package_not_found.append(dep)
        sys.stdout.write("{0}Done{1}\n".format(color['GREY'], color['ENDC']))
        print("\nThe following packages will be automatically "
              "installed or upgraded \nwith new version:\n")
        self.top_view()
        print self.package_not_found
        print self.remove_dbs()

    def one_for_all(self):
        '''
        Because there are dependencies that depend on other
        dependencies are created lists into other lists.
        Thus creating this loop create one-dimensional list.
        '''
        requires = []
        for dep in self.deps:
            requires += dep
        # Inverting the list brings the
        # dependencies in order to be installed.
        requires.reverse()
        return requires

    def remove_dbs(self):
        '''
        Many packages use the same dependencies, in this loop
        creates a new list by removing duplicate dependencies but
        without spoiling the line must be installed.
        '''
        dependencies = []
        for duplicate in self.one_for_all():
            if duplicate not in dependencies:
                dependencies.append(duplicate)
        return dependencies

    def top_view(self):
        '''
        View top template
        '''
        template(78)
        print("{0}{1}{2}{3}{4}{5}{6}".format(
            "| Package", " " * 30,
            "Version", " " * 10,
            "Arch", " " * 9,
            "Repository"))
        template(78)

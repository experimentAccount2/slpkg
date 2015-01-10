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

import os
import sys

from dependency import sbo_dependencies_pkg
from search import sbo_search_pkg
from __metadata__ import color, pkg_path
from messages import template
from greps import SBoGrep


from slpkg.pkg.find import find_package


class SBoInstall(object):

    def __init__(self, slackbuilds):
        self.slackbuilds = slackbuilds
        self.unst = ["UNSUPPORTED", "UNTESTED"]
        sys.stdout.write("{0}Reading package lists ...{1}".format(
            color['GREY'], color['ENDC']))
        sys.stdout.flush()

    def start(self):
        self.slackbuilds = ['Flask', 'asdaf', 'PyAudio', 'PySDL2', 'flexget',
                            'werwer', 'skype']

        self.deps, dependencies = [], []
        self.package_not_found, self.package_found = [], []
        for sbo in self.slackbuilds:
            if sbo_search_pkg(sbo):
                self.deps += sbo_dependencies_pkg(sbo)
                self.package_found.append(sbo)
            else:
                self.package_not_found.append(sbo)
        dependencies, dep_src = self.sbo_version_source(self.remove_dbs())
        self.master_packages, mas_src = self.sbo_version_source(
            self.package_found)
        sys.stdout.write("{0}Done{1}\n".format(color['GREY'], color['ENDC']))
        print("\nThe following packages will be automatically "
              "installed or upgraded \nwith new version:\n")
        self.top_view()
        for sbo, ar in zip(self.master_packages, mas_src):
            if sbo not in dependencies:
                self.view_packages(self.tag(sbo), '-'.join(sbo.split('-')[:-1]),
                                   sbo.split('-')[-1], self.select_arch(ar))
        print("Installing for dependencies:")
        for dep, ar in zip(dependencies, dep_src):
            self.view_packages(self.tag(dep), '-'.join(dep.split('-')[:-1]),
                               dep.split('-')[-1], self.select_arch(ar))

    def sbo_version_source(self, slackbuilds):
        sbo_versions, sources = [], []
        for sbo in slackbuilds:
            sbo_ver = '{0}-{1}'.format(sbo, SBoGrep(sbo).version())
            sbo_versions.append(sbo_ver)
            sources.append(SBoGrep(sbo).source())
        return [sbo_versions, sources]

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

    def view_packages(self, *args):
        '''
        View slackbuild packages with version and arch
        args[0] package color
        args[1] package
        args[2] version
        args[3] arch
        '''
        color_arch = ''
        if self.unst[0] in args[3] or self.unst[1] in args[3]:
            color_arch = color['RED']
        print(" {0}{1}{2}{3} {4}{5}{6} {7}{8}{9}{10}".format(
            args[0], args[1], color['ENDC'], " " * (37-len(args[1])),
            args[2], " " * (16-len(args[2])),
            color_arch, args[3], color['ENDC'], " " * (13-len(args[3])),
            "SBo"))

    def tag(self, sbo):
        '''
        Tag with color green if package already installed,
        color yellow for packages to upgrade and color red
        if not installed.
        '''
        if find_package(sbo, pkg_path):
            paint = color['GREEN']
        elif find_package(sbo.split('-')[0] + '-', pkg_path):
            paint = color['YELLOW']
        else:
            paint = color['RED']
        return paint

    def select_arch(self, src):
        '''
        Looks if sources unsupported or untested
        from arch else select arch
        '''
        arch = os.uname()[4]
        if arch.startswith("i") and arch.endswith("86"):
            arch = "i486"
        for item in self.unst:
            if item in src:
                arch = item
        return arch

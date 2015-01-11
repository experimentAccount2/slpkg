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
        self.deps = []
        self.package_not_found = []
        self.package_found = []

        sys.stdout.write("{0}Reading package lists ...{1}".format(
            color['GREY'], color['ENDC']))
        sys.stdout.flush()

    def start(self):
        self.slackbuilds = ['Flask', 'asdaf', 'PyAudio', 'PySDL2', 'flexget',
                            'werwer', 'skype']

        dependencies, tagc = [], ''
        count_ins = count_upg = count_uni = 0
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
                tagc, count_ins, count_upg, count_uni = self.tag(sbo,
                                                                 count_ins,
                                                                 count_upg,
                                                                 count_uni)
                self.view_packages(tagc, '-'.join(sbo.split('-')[:-1]),
                                   sbo.split('-')[-1], self.select_arch(ar))
        print("Installing for dependencies:")
        for dep, ar in zip(dependencies, dep_src):
            tagc, count_ins, count_upg, count_uni = self.tag(dep, count_ins,
                                                             count_upg,
                                                             count_uni)
            self.view_packages(tagc, '-'.join(dep.split('-')[:-1]),
                               dep.split('-')[-1], self.select_arch(ar))

        count_total = (count_ins + count_upg + count_uni)
        print("\nInstalling summary")
        print("=" * 79)
        print("{0}Total {1} {2}.".format(
            color['GREY'], count_total, self.msg(count_total)))
        print("{0} {1} will be installed, {2} allready installed and "
              "{3} {4}".format(count_uni, self.msg(count_uni), count_ins,
                               count_upg, self.msg(count_upg)))
        print("will be upgraded.{0}\n".format(color['ENDC']))

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
        print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
            "| Package", " " * 17,
            "Version", " " * 12,
            "Arch", " " * 4,
            "Build", " " * 2,
            "Repos", " " * 10,
            "Size"))
        template(78)

    def view_packages(self, *args):
        '''
        View slackbuild packages with version and arch
        args[0] package color
        args[1] package
        args[2] version
        args[3] arch
        '''
        print(" {0}{1}{2}{3} {4}{5} {6}{7}{8}{9}{10}{11:>11}{12}".format(
            args[0], args[1], color['ENDC'],
            " " * (24-len(args[1])), args[2],
            " " * (18-len(args[2])), args[3],
            " " * (15-len(args[3])), "",
            "", "SBo", "", ""))

    def tag(self, sbo, count_ins, count_upg, count_uni):
        '''
        Tag with color green if package already installed,
        color yellow for packages to upgrade and color red
        if not installed.
        '''
        if find_package(sbo, pkg_path):
            paint = color['GREEN']
            count_ins += 1
        elif find_package('-'.join(sbo.split('-')[:-1]) + '-', pkg_path):
            paint = color['YELLOW']
            count_upg += 1
        else:
            paint = color['RED']
            count_uni += 1
        return paint, count_ins, count_upg, count_uni

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

    def msg(self, count):
        '''
        Print singular plural
        '''
        message = "package"
        if count > 1:
            message = message + "s"
        return message

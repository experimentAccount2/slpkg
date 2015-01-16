#!/usr/bin/python
# -*- coding: utf-8 -*-

# install.py file is part of slpkg.

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

from slpkg.sizes import units
from slpkg.remove import delete
from slpkg.repositories import Repo
from slpkg.checksum import check_md5
from slpkg.blacklist import BlackList
from slpkg.downloader import Download
from slpkg.grep_md5 import pkg_checksum
from slpkg.splitting import split_package
from slpkg.messages import (
    pkg_not_found,
    template
)
from slpkg.__metadata__ import (
    pkg_path,
    lib_path,
    log_path,
    slpkg_tmp_packages,
    default_answer,
    color,
    slacke_sub_repo,
    default_repositories
)

from slpkg.pkg.find import find_package
from slpkg.pkg.manager import PackageManager

from slpkg.slack.slack_version import slack_ver

from greps import repo_data
from dependency import Dependencies


class OthersInstall(object):

    def __init__(self, packages, repo, version):
        self.packages = packages
        self.repo = repo
        self.version = version
        self.dwn, self.dep_dwn = [], []
        self.install, self.dep_install = [], []
        self.comp_sum, self.dep_comp_sum = [], []
        self.uncomp_sum, self.dep_uncomp_sum = [], []
        self.deps_pass = False
        print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
              color['CYAN'], ', '.join(self.packages), color['ENDC']))
        sys.stdout.write("{0}Reading package lists ...{1}".format(
            color['GREY'], color['ENDC']))
        sys.stdout.flush()
        self.step = 800 * len(packages)

        if repo in default_repositories:
            exec('self._init_{0}()'.format(self.repo))
        else:
            exec('self._init_custom()')

        f = open(self.lib, "r")
        self.PACKAGES_TXT = f.read()
        f.close()
        num_lines = sum(1 for line in self.PACKAGES_TXT)
        self.step = num_lines / 1000

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

    def start(self):
        '''
        Install packages from official Slackware distribution
        '''
        mas_sum = dep_sum = pkg_sum = [0, 0, 0]
        (self.dwn, self.install, self.comp_sum,
         self.uncomp_sum) = self.store(self.packages)
        sys.stdout.write("{0}Done{1}\n".format(color['GREY'], color['ENDC']))
        dependencies = self.resolving_deps()
        self.deps_pass = True
        (self.dep_dwn, self.dep_install, self.dep_comp_sum,
         self.dep_uncomp_sum) = self.store(dependencies)
        sys.stdout.write("{0}Done{1}\n".format(color['GREY'], color['ENDC']))
        print("")   # new line at start
        if self.install:
            self.top_view()
            print("Installing:")
            mas_sum = self.views(self.install, self.comp_sum)
            if dependencies:
                print("Installing for dependencies:")
                dep_sum = self.views(self.dep_install, self.dep_comp_sum)
            pkg_sum = [sum(i) for i in zip(mas_sum, dep_sum)]
            unit, size = units(self.comp_sum, self.uncomp_sum)
            print unit, size


    def resolving_deps(self):
        '''
        Return package dependencies
        '''
        requires, dependencies = [], []
        sys.stdout.write("{0}Resolving dependencies ...{1}".format(
            color['GREY'], color['ENDC']))
        sys.stdout.flush()
        for dep in self.packages:
            deps = Dependencies().others(dep, self.repo)
            # Create one list for all packages
            for pkg in deps:
                requires += pkg
            requires.reverse()
            # Remove double dependencies
            for duplicate in requires:
                if duplicate not in dependencies:
                    dependencies.append(duplicate)
        return dependencies

    def views(self, install, comp_sum):
        '''
        Views packages
        '''
        pkg_sum = uni_sum = upg_sum = 0
        # fix repositories align
        self.repo = self.repo + (' ' * (6 - (len(self.repo))))
        for pkg, comp in zip(install, comp_sum):
            pkg_split = split_package(pkg[:-4])
            if find_package(pkg_split[0] + "-" + pkg_split[1], pkg_path):
                pkg_sum += 1
                COLOR = color['GREEN']
            elif find_package(pkg_split[0] + "-", pkg_path):
                COLOR = color['YELLOW']
                upg_sum += 1
            else:
                COLOR = color['RED']
                uni_sum += 1
            print(" {0}{1}{2}{3} {4}{5} {6}{7}{8}{9}{10}{11:>11}{12}".format(
                COLOR, pkg_split[0], color['ENDC'],
                " " * (24-len(pkg_split[0])), pkg_split[1],
                " " * (18-len(pkg_split[1])), pkg_split[2],
                " " * (8-len(pkg_split[2])), pkg_split[3],
                " " * (7-len(pkg_split[3])), self.repo,
                comp, " K"))
        return [pkg_sum, upg_sum, uni_sum]

    def top_view(self):
        template(78)
        print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
            "| Package", " " * 17,
            "Version", " " * 12,
            "Arch", " " * 4,
            "Build", " " * 2,
            "Repos", " " * 10,
            "Size"))
        template(78)

    def store(self, packages):
            '''
            Store and return packages for install
            '''
            dwn, install, comp_sum, uncomp_sum = ([] for i in range(4))
            black = BlackList().packages()
            # name = data[0]
            # location = data[1]
            # size = data[2]
            # unsize = data[3]
            data = repo_data(self.PACKAGES_TXT, self.step, self.repo,
                             self.version)
            for pkg in packages:
                for name, loc, comp, uncomp in zip(data[0], data[1], data[2],
                                                   data[3]):
                    if pkg in name and pkg not in black:
                        dwn.append("{0}{1}/{2}".format(self.mirror, loc, name))
                        install.append(name)
                        comp_sum.append(comp)
                        uncomp_sum.append(uncomp)
            if not install:
                for pkg in packages:
                    for name, loc, comp, uncomp in zip(data[0], data[1],
                                                       data[2], data[3]):
                        if pkg in split_package(name)[0] and not self.deps_pass:
                            dwn.append("{0}{1}/{2}".format(self.mirror, loc,
                                                           name))
                            install.append(name)
                            comp_sum.append(comp)
                            uncomp_sum.append(uncomp)
            dwn.reverse()
            install.reverse()
            comp_sum.reverse()
            uncomp_sum.reverse()
            return [dwn, install, comp_sum, uncomp_sum]

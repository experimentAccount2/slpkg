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
from slpkg.messages import template
from slpkg.checksum import check_md5
from slpkg.blacklist import BlackList
from slpkg.downloader import Download
from slpkg.grep_md5 import pkg_checksum
from slpkg.splitting import split_package
from slpkg.utils import (
    remove_dbs,
    dimensional_list
)
from slpkg.__metadata__ import (
    color,
    pkg_path,
    log_path,
    default_answer,
    slpkg_tmp_packages,
)

from slpkg.pkg.find import find_package
from slpkg.pkg.manager import PackageManager

from slpkg.slack.slack_version import slack_ver

from greps import repo_data
from repo_init import RepoInit
from dependency import Dependencies


class OthersInstall(object):

    def __init__(self, packages, repo, version):
        self.packages = packages
        self.repo = repo
        self.version = version
        self.tmp_path = slpkg_tmp_packages
        self.dwn, self.dep_dwn = [], []
        self.install, self.dep_install = [], []
        self.comp_sum, self.dep_comp_sum = [], []
        self.uncomp_sum, self.dep_uncomp_sum = [], []
        self.dependencies = []
        self.deps_dict = {}
        self.deps_pass = False
        self.answer = ''
        print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
              color['CYAN'], ', '.join(self.packages), color['ENDC']))
        sys.stdout.write("{0}Reading package lists ...{1}".format(
            color['GREY'], color['ENDC']))
        sys.stdout.flush()

        self.PACKAGES_TXT, self.mirror = RepoInit(self.repo).fetch()
        num_lines = sum(1 for line in self.PACKAGES_TXT)
        self.step = num_lines / 1000

    def start(self):
        '''
        Install packages from official Slackware distribution
        '''
        try:
            mas_sum = dep_sum = sums = [0, 0, 0]
            self.packages = self.clear_masters()
            (self.dwn, self.install, self.comp_sum,
             self.uncomp_sum) = self.store(self.packages)
            sys.stdout.write("{0}Done{1}\n".format(color['GREY'],
                                                   color['ENDC']))
            self.dependencies = self.resolving_deps()
            self.deps_pass = True
            (self.dep_dwn, self.dep_install, self.dep_comp_sum,
             self.dep_uncomp_sum) = self.store(self.dependencies)
            sys.stdout.write("{0}Done{1}\n".format(color['GREY'],
                                                   color['ENDC']))
            print("")   # new line at start
            if self.install:
                self.top_view()
                print("Installing:")
                mas_sum = self.views(self.install, self.comp_sum)
                if self.dependencies:
                    print("Installing for dependencies:")
                    dep_sum = self.views(self.dep_install, self.dep_comp_sum)
                sums = [sum(i) for i in zip(mas_sum, dep_sum)]
                unit, size = units(self.comp_sum, self.uncomp_sum)
                print("\nInstalling summary")
                print("=" * 79)
                print("{0}Total {1} {2}.".format(color['GREY'],
                                                 len(self.install),
                                                 self.msg(len(self.install))))
                print("{0} {1} will be installed, {2} will be upgraded and "
                      "{3} will be reinstalled.".format(sums[2],
                                                        self.msg(sums[2]),
                                                        sums[1], sums[0]))
                print("Need to get {0} {1} of archives.".format(size[0],
                                                                unit[0]))
                print("After this process, {0} {1} of additional disk "
                      "space will be used.{2}".format(size[1], unit[1],
                                                      color['ENDC']))
                self.answer = self.continue_install()
                if self.answer in ['y', 'Y']:
                    self.install.reverse()
                    Download(self.tmp_path, self.dwn).start()
                    self.install_packages()
                    # self.write_deps(self, dependencies)
                    delete(self.tmp_path, self.install)
            else:
                print('\nNot found packages for installation\n')
        except KeyboardInterrupt:
            print("")   # new line at exit
            sys.exit(0)

    def clear_masters(self):
        '''
        Clear master packages if already exist in dependencies
        or if added to install two or more times
        '''
        packages = []
        for mas in remove_dbs(self.packages):
            if mas not in self.dependencies:
                packages.append(mas)
        return packages

    def install_packages(self):
        '''
        Install or upgrade packages
        '''
        for inst in self.install:
            package = (self.tmp_path + inst).split()
            self.checksums(inst)
            if os.path.isfile(pkg_path + inst[:-4]):
                print("[ {0}reinstalling{1} ] --> {2}".format(color['GREEN'],
                                                              color['ENDC'],
                                                              inst))
                PackageManager(package).reinstall()
            elif find_package(split_package(inst)[0] + "-", pkg_path):
                print("[ {0}upgrading{1} ] --> {2}".format(color['YELLOW'],
                                                           color['ENDC'], inst))
                PackageManager(package).upgrade()
            else:
                print("[ {0}installing{1} ] --> {2}".format(color['GREEN'],
                                                            color['ENDC'],
                                                            inst))
                PackageManager(package).upgrade()

    def checksums(self, install):
        '''
        Checksums before install
        '''
        if self.repo == "alien" and self.version == "stable":
            check_md5(pkg_checksum("/" + slack_ver() + "/" + install,
                                   self.repo), self.tmp_path + install)
        elif self.repo == "alien" and self.version == "current":
            check_md5(pkg_checksum("/" + self.version + "/" + install,
                                   self.repo), self.tmp_path + install)
        else:
            check_md5(pkg_checksum(install, self.repo), self.tmp_path + install)

    def write_deps(self, dependencies):
        '''
        Write dependencies in a log file
        into directory `/var/log/slpkg/dep/`
        '''
        if len(dependencies) > 1:
            name = dependencies[-1]
            if find_package(name + "-", pkg_path):
                dep_path = log_path + "dep/"
                if not os.path.exists(dep_path):
                    os.mkdir(dep_path)
                if os.path.isfile(dep_path + name):
                    os.remove(dep_path + name)
                if len(dependencies[:-1]) > 0:
                    with open(dep_path + name, "w") as f:
                        for dep in dependencies[:-1]:
                            f.write(dep + "\n")
                    f.close()

    def continue_install(self):
        '''
        Default answer
        '''
        if default_answer == "y":
            self.answer = default_answer
        else:
            self.answer = raw_input("\nWould you like to continue [Y/n]? ")
        return self.answer

    def msg(self, count):
        '''
        Print singular plural
        '''
        message = "package"
        if count > 1:
            message = message + "s"
        return message

    def resolving_deps(self):
        '''
        Return package dependencies
        '''
        requires, dependencies = [], []
        sys.stdout.write("{0}Resolving dependencies ...{1}".format(
            color['GREY'], color['ENDC']))
        sys.stdout.flush()
        for dep in self.packages:
            requires += Dependencies().others(dep, self.repo)
        dependencies = dimensional_list(requires)
        dependencies.reverse()
        return remove_dbs(dependencies)

    def views(self, install, comp_sum):
        '''
        Views packages
        '''
        pkg_sum = uni_sum = upg_sum = 0
        # fix repositories align
        repo = self.repo + (' ' * (6 - (len(self.repo))))
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
                " " * (7-len(pkg_split[3])), repo,
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
        data = repo_data(self.PACKAGES_TXT, self.step, self.repo, self.version)
        for pkg in packages:
            for name, loc, comp, uncomp in zip(data[0], data[1], data[2],
                                               data[3]):
                if pkg == split_package(name)[0] and pkg not in black:
                    dwn.append("{0}{1}/{2}".format(self.mirror, loc, name))
                    install.append(name)
                    comp_sum.append(comp)
                    uncomp_sum.append(uncomp)
        if not install:
            for pkg in packages:
                for name, loc, comp, uncomp in zip(data[0], data[1], data[2],
                                                   data[3]):
                    if pkg in split_package(name)[0] and not self.deps_pass:
                        dwn.append("{0}{1}/{2}".format(self.mirror, loc, name))
                        install.append(name)
                        comp_sum.append(comp)
                        uncomp_sum.append(uncomp)
        dwn.reverse()
        install.reverse()
        comp_sum.reverse()
        uncomp_sum.reverse()
        return [dwn, install, comp_sum, uncomp_sum]

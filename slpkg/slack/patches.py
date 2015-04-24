#!/usr/bin/python
# -*- coding: utf-8 -*-

# patches.py file is part of slpkg.

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
import subprocess

from slpkg.utils import Utils
from slpkg.sizes import units
from slpkg.messages import Msg
from slpkg.url_read import URL
from slpkg.remove import delete
from slpkg.checksum import check_md5
from slpkg.blacklist import BlackList
from slpkg.downloader import Download
from slpkg.grep_md5 import pkg_checksum
from slpkg.splitting import split_package
from slpkg.__metadata__ import MetaData as _m

from slpkg.pkg.find import find_package
from slpkg.pkg.manager import PackageManager

from slpkg.binary.greps import repo_data

from mirrors import mirrors
from slack_version import slack_ver


class Patches(object):

    def __init__(self):
        self.version = _m.slack_rel
        self.patch_path = _m.slpkg_tmp_patches
        self.pkg_for_upgrade = []
        self.dwn_links = []
        self.upgrade_all = []
        self.count_added = 0
        self.count_upg = 0
        self.upgraded = []
        self.installed = []
        self.comp_sum = []
        self.uncomp_sum = []
        Msg().reading()
        if self.version == "stable":
            self.PACKAGES_TXT = URL(mirrors("PACKAGES.TXT",
                                            "patches/")).reading()
            self.step = 20
        else:
            self.PACKAGES_TXT = URL(mirrors("PACKAGES.TXT", "")).reading()
            self.step = 700

    def start(self):
        '''
        Install new patches from official Slackware mirrors
        '''
        try:
            self.store()
            Msg().done()
            if self.upgrade_all:
                print("\nThese packages need upgrading:\n")
                Msg().template(78)
                print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
                    "| Package", " " * 17,
                    "Version", " " * 12,
                    "Arch", " " * 4,
                    "Build", " " * 2,
                    "Repos", " " * 10,
                    "Size"))
                Msg().template(78)
                print("Upgrading:")
                self.views()
                unit, size = units(self.comp_sum, self.uncomp_sum)
                print("\nInstalling summary")
                print("=" * 79)
                print("{0}Total {1} {2} will be upgraded and {3} will be "
                      "installed.".format(_m.color['GREY'],
                                          self.count_upg,
                                          Msg().pkg(self.upgrade_all),
                                          self.count_added))
                print("Need to get {0} {1} of archives.".format(size[0],
                                                                unit[0]))
                print("After this process, {0} {1} of additional disk space "
                      "will be used.{2}".format(size[1], unit[1],
                                                _m.color['ENDC']))
                print('')
                if Msg().answer() in ['y', 'Y']:
                    Download(self.patch_path, self.dwn_links).start()
                    self.upgrade_all = Utils().check_downloaded(
                        self.patch_path, self.upgrade_all)
                    self.upgrade()
                    self.kernel()
                    Msg().reference(self.installed, self.upgraded)
                    delete(self.patch_path, self.upgrade_all)
            else:
                slack_arch = ""
                if os.uname()[4] == "x86_64":
                    slack_arch = 64
                print("\nSlackware{0} '{1}' v{2} distribution is up to "
                      "date\n".format(slack_arch, self.version, slack_ver()))
        except KeyboardInterrupt:
            print("")   # new line at exit
            sys.exit(0)

    def store(self):
        '''
        Store and return packages for upgrading
        '''
        data = repo_data(self.PACKAGES_TXT, self.step, 'slack')
        black = BlackList().packages()
        for name, loc, comp, uncomp in zip(data[0], data[1], data[2], data[3]):
            repo_pkg_name = split_package(name)[0]
            if (not os.path.isfile(_m.pkg_path + name[:-4]) and
                    repo_pkg_name not in black):
                self.dwn_links.append("{0}{1}/{2}".format(mirrors("", ""),
                                                          loc, name))
                self.comp_sum.append(comp)
                self.uncomp_sum.append(uncomp)
                self.upgrade_all.append(name)
                self.count_upg += 1
                if not find_package(repo_pkg_name, _m.pkg_path):
                    self.count_added += 1
                    self.count_upg -= 1

    def views(self):
        '''
        Views packages
        '''
        for upg, size in sorted(zip(self.upgrade_all, self.comp_sum)):
            pkg_split = split_package(upg[:-4])
            color = _m.color['YELLOW']
            if not find_package(pkg_split[0], _m.pkg_path):
                color = _m.color['RED']
            print(" {0}{1}{2}{3} {4}{5} {6}{7}{8}{9}{10}{11:>12}{12}".format(
                color, pkg_split[0], _m.color['ENDC'],
                " " * (24-len(pkg_split[0])), pkg_split[1],
                " " * (18-len(pkg_split[1])), pkg_split[2],
                " " * (8-len(pkg_split[2])), pkg_split[3],
                " " * (7-len(pkg_split[3])), "Slack",
                size, " K")).rstrip()

    def upgrade(self):
        '''
        Upgrade packages
        '''
        for pkg in self.upgrade_all:
            check_md5(pkg_checksum(pkg, "slack_patches"), self.patch_path + pkg)
            pkg_ver = '{0}-{1}'.format(split_package(pkg)[0],
                                       split_package(pkg)[1])
            if find_package(split_package(pkg)[0] + "-", _m.pkg_path):
                print("[ {0}upgrading{1} ] --> {2}".format(_m.color['YELLOW'],
                                                           _m.color['ENDC'],
                                                           pkg[:-4]))
                PackageManager((self.patch_path + pkg).split()).upgrade()
                self.upgraded.append(pkg_ver)
            else:
                print("[ {0}installing{1} ] --> {2}".format(_m.color['GREEN'],
                                                            _m.color['ENDC'],
                                                            pkg[:-4]))
                PackageManager((self.patch_path + pkg).split()).upgrade()
                self.installed.append(pkg_ver)

    def kernel(self):
        '''
        Check if kernel upgraded if true
        then reinstall 'lilo'
        '''
        for core in self.upgrade_all:
            if "kernel" in core:
                if _m.default_answer == "y":
                    answer = _m.default_answer
                else:
                    print("")
                    Msg().template(78)
                    print("| {0}*** HIGHLY recommended reinstall 'LILO' "
                          "***{1}".format(_m.color['RED'], _m.color['ENDC']))
                    Msg().template(78)
                    answer = raw_input("\nThe kernel has been upgraded, "
                                       "reinstall `LILO` [Y/n]? ")
                if answer in ['y', 'Y']:
                    subprocess.call("lilo", shell=True)
                    break

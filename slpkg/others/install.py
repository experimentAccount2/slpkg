#!/usr/bin/python
# -*- coding: utf-8 -*-

# install.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

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

from init import Initialization
from blacklist import BlackList
from splitting import split_package
from messages import pkg_not_found, template
from __metadata__ import slpkg_tmp, pkg_path, lib_path
from colors import RED, GREEN, CYAN, YELLOW, GREY, ENDC

from pkg.find import find_package
from pkg.manager import PackageManager

from sizes import units
from remove import delete
from greps import repo_data
from download import slack_dwn
from slack_version import slack_ver


class Others(object):

    def __init__(self, package, repo):
        self.package = package
        self.repo = repo
        self.tmp_path = slpkg_tmp + "packages/"
        Initialization().rlw()
        Initialization().alien()
        print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
              CYAN, self.package, ENDC))
        sys.stdout.write("{0}Reading package lists ...{1}".format(GREY, ENDC))
        sys.stdout.flush()
        if not os.path.exists(slpkg_tmp):
            os.mkdir(slpkg_tmp)
        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)
        self.step = 700
        if self.repo == "rlw":
            lib = lib_path + "rlw_repo/PACKAGES.TXT"
            f = open(lib, "r")
            self.mirror = "http://rlworkman.net/pkgs/{0}".format(slack_ver())
        else:
            lib = lib_path + "alien_repo/PACKAGES.TXT"
            f = open(lib, "r")
            self.mirror = "http://www.slackware.com/~alien/slackbuilds/"
            self.step = self.step * 2
        self.PACKAGES_TXT = f.read()
        f.close()

    def start(self):
        '''
        Install packages from official Slackware distribution
        '''
        try:
            data = repo_data(self.PACKAGES_TXT, self.step, self.repo)
            (dwn_links, install_all,
             comp_sum, uncomp_sum) = store(data[0], data[1], data[2], data[3],
                                           self.package, self.mirror, self.repo)
            sys.stdout.write("{0}Done{1}\n\n".format(GREY, ENDC))
            if install_all:
                template(78)
                print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
                    "| Package", " " * 17,
                    "Version", " " * 12,
                    "Arch", " " * 4,
                    "Build", " " * 2,
                    "Repos", " " * 10,
                    "Size"))
                template(78)
                print("Installing:")
                sums = views(install_all, comp_sum, self.repo)
                unit, size = units(comp_sum, uncomp_sum)
                msg = msgs(install_all, sums[2])
                print("\nInstalling summary")
                print("=" * 79)
                print("{0}Total {1} {2}.".format(GREY, len(install_all),
                                                 msg[0]))
                print("{0} {1} will be installed, {2} will be upgraded and "
                      "{3} will be resettled.".format(sums[2], msg[1],
                                                      sums[1], sums[0]))
                print("Need to get {0} {1} of archives.".format(size[0],
                                                                unit[0]))
                print("After this process, {0} {1} of additional disk space "
                      "will be used.{2}".format(size[1], unit[1], ENDC))
                read = raw_input("\nWould you like to install [Y/n]? ")
                if read == "Y" or read == "y":
                    slack_dwn(self.tmp_path, dwn_links)
                    install(self.tmp_path, install_all)
                    delete(self.tmp_path, install_all)
            else:
                pkg_not_found("", self.package, "No matching", "\n")
        except KeyboardInterrupt:
            print   # new line at exit
            sys.exit()


def store(*args):
    '''
    Store and return packages for install
    '''
    dwn, install, comp_sum, uncomp_sum = ([] for i in range(4))
    for name, loc, comp, uncomp in zip(args[0], args[1], args[2], args[3]):
        if args[4] in name and args[4] not in BlackList().packages():
            if args[6] == "rlw":
                dwn.append("{0}{1}/{2}".format(args[5], loc, name))
            else:
                arch = os.uname()[4]
                if arch.startswith("i") and arch.endswith("86"):
                    arch = ""
                else:
                    arch = "64"
                ver = slack_ver()
                dwn.append("{0}{1}/pkg{2}/{3}/{4}".format(args[5], args[4],
                                                          arch, ver, name))
            install.append(name)
            comp_sum.append(comp)
            uncomp_sum.append(uncomp)
    return [dwn, install, comp_sum, uncomp_sum]


def views(install_all, comp_sum, repository):
    '''
    Views packages
    '''
    pkg_sum = uni_sum = upg_sum = 0
    if repository == "rlw":
        repository = repository + "  "
    for pkg, comp in zip(install_all, comp_sum):
        pkg_split = split_package(pkg[:-4])
        if os.path.isfile(pkg_path + pkg[:-4]):
            pkg_sum += 1
            COLOR = GREEN
        elif find_package(pkg_split[0] + "-", pkg_path):
            COLOR = YELLOW
            upg_sum += 1
        else:
            COLOR = RED
            uni_sum += 1
        print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11:>12}{12}".format(
            COLOR, pkg_split[0], ENDC,
            " " * (25-len(pkg_split[0])), pkg_split[1],
            " " * (19-len(pkg_split[1])), pkg_split[2],
            " " * (8-len(pkg_split[2])), pkg_split[3],
            " " * (7-len(pkg_split[3])), repository,
            comp, " K"))
    return [pkg_sum, upg_sum, uni_sum]


def msgs(install_all, uni_sum):
    '''
    Print singular plural
    '''
    msg_pkg = "package"
    msg_2_pkg = msg_pkg
    if len(install_all) > 1:
        msg_pkg = msg_pkg + "s"
    if uni_sum > 1:
        msg_2_pkg = msg_2_pkg + "s"
    return [msg_pkg, msg_2_pkg]


def install(tmp_path, install_all):
    '''
    Install or upgrade packages
    '''
    for install in install_all:
        package = (tmp_path + install).split()
        if os.path.isfile(pkg_path + install[:-4]):
            print("[ {0}reinstalling{1} ] --> {2}".format(
                  GREEN, ENDC, install))
            PackageManager(package).reinstall()
        elif find_package(split_package(install)[0] + "-", pkg_path):
            print("[ {0}upgrading{1} ] --> {2}".format(
                  YELLOW, ENDC, install))
            PackageManager(package).upgrade()
        else:
            print("[ {0}installing{1} ] --> {2}".format(
                  GREEN, ENDC, install))
            PackageManager(package).upgrade()

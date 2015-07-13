#!/usr/bin/python
# -*- coding: utf-8 -*-

# init.py file is part of slpkg.

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


import os
import sys

from url_read import URL
from toolbar import status
from repositories import Repo
from file_size import FileSize
from downloader import Download
from __metadata__ import MetaData as _meta_

from slack.mirrors import mirrors
from slack.slack_version import slack_ver


class Initialization(object):

    def __init__(self, check):
        self.check = check
        self.meta = _meta_
        self.conf_path = self.meta.conf_path
        self.log_path = self.meta.log_path
        self.lib_path = self.meta.lib_path
        self.tmp_path = self.meta.tmp_path
        self.build_path = self.meta.build_path
        self.slpkg_tmp_packages = self.meta.slpkg_tmp_packages
        self.slpkg_tmp_patches = self.meta.slpkg_tmp_patches
        if not os.path.exists(self.conf_path):
            os.mkdir(self.conf_path)
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        if not os.path.exists(self.lib_path):
            os.mkdir(self.lib_path)
        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)
        if not os.path.exists(self.build_path):
            os.makedirs(self.build_path)
        if not os.path.exists(self.slpkg_tmp_packages):
            os.makedirs(self.slpkg_tmp_packages)
        if not os.path.exists(self.slpkg_tmp_patches):
            os.makedirs(self.slpkg_tmp_patches)

    def custom(self, name):
        """Creating user select repository local library
        """
        repo = Repo().custom_repository()[name]
        log = self.log_path + name + "/"
        lib = self.lib_path + "{0}_repo/".format(name)
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        PACKAGES_TXT = "{0}{1}".format(repo, lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}{1}".format(repo, md5_file)
        ChangeLog_txt = "{0}{1}".format(repo, log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file,
                    PACKAGES_TXT, md5_file, CHECKSUMS_MD5, lst_file,
                    FILELIST_TXT)

    def slack(self):
        """Creating slack local libraries
        """
        log = self.log_path + "slack/"
        lib = self.lib_path + "slack_repo/"
        repo_name = log[:-1].split("/")[-1]
        lib_file = "PACKAGES.TXT"
        # lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        packages = mirrors(lib_file, "")
        FILELIST_TXT = ""
        pkg_checksums = mirrors(md5_file, "")
        extra = mirrors(lib_file, "extra/")
        ext_checksums = mirrors(md5_file, "extra/")
        pasture = mirrors(lib_file, "pasture/")
        pas_checksums = mirrors(md5_file, "pasture/")
        PACKAGES_TXT = ("{0} {1} {2}".format(packages, extra, pasture))
        CHECKSUMS_MD5 = ("{0} {1} {2}".format(pkg_checksums, ext_checksums,
                                              pas_checksums))
        ChangeLog_txt = mirrors(log_file, "")
        if self.check:
            return self.checks_logs(log, ChangeLog_txt)
        self.down(lib, PACKAGES_TXT, repo_name)
        self.down(lib, CHECKSUMS_MD5, repo_name)
        self.down(log, ChangeLog_txt, repo_name)
        self.remote(log, ChangeLog_txt, lib, PACKAGES_TXT, CHECKSUMS_MD5,
                    FILELIST_TXT, repo_name)

        # self.write(lib, lib_file, PACKAGES_TXT)
        # self.write(lib, md5_file, CHECKSUMS_MD5)
        # self.write(log, log_file, ChangeLog_txt)
        # self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
        #            md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def sbo(self):
        """Creating sbo local library
        """
        repo = Repo().sbo()
        log = self.log_path + "sbo/"
        lib = self.lib_path + "sbo_repo/"
        lib_file = "SLACKBUILDS.TXT"
        lst_file = ""
        md5_file = ""
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        SLACKBUILDS_TXT = "{0}{1}/{2}".format(repo, slack_ver(), lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = ""
        ChangeLog_txt = "{0}{1}/{2}".format(repo, slack_ver(), log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, SLACKBUILDS_TXT)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file,
                    SLACKBUILDS_TXT, md5_file, CHECKSUMS_MD5, lst_file,
                    FILELIST_TXT)

    def rlw(self):
        """Creating rlw local library
        """
        repo = Repo().rlw()
        log = self.log_path + "rlw/"
        lib = self.lib_path + "rlw_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        PACKAGES_TXT = "{0}{1}/{2}".format(repo, slack_ver(), lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}{1}/{2}".format(repo, slack_ver(), md5_file)
        ChangeLog_txt = "{0}{1}/{2}".format(repo, slack_ver(), log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def alien(self):
        """Creating alien local library
        """
        ar = "x86"
        ver = slack_ver()
        arch = os.uname()[4]
        repo = Repo().alien()
        log = self.log_path + "alien/"
        lib = self.lib_path + "alien_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        if arch == "x86_64":
            ar = arch
        if self.meta.slack_rel == "current":
            ver = self.meta.slack_rel
        PACKAGES_TXT = "{0}/{1}/{2}/{3}".format(repo, ver, ar, lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}/{1}/{2}/{3}".format(repo, ver, ar, md5_file)
        ChangeLog_txt = "{0}{1}".format(repo, log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def slacky(self):
        """Creating slacky.eu local library
        """
        ar = ""
        arch = os.uname()[4]
        repo = Repo().slacky()
        log = self.log_path + "slacky/"
        lib = self.lib_path + "slacky_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        if arch == "x86_64":
            ar = "64"
        PACKAGES_TXT = "{0}slackware{1}-{2}/{3}".format(repo, ar, slack_ver(),
                                                        lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}slackware{1}-{2}/{3}".format(repo, ar, slack_ver(),
                                                         md5_file)

        ChangeLog_txt = "{0}slackware{1}-{2}/{3}".format(repo, ar, slack_ver(),
                                                         log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def studio(self):
        """Creating studio local library
        """
        ar = ""
        arch = os.uname()[4]
        repo = Repo().studioware()
        log = self.log_path + "studio/"
        lib = self.lib_path + "studio_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        if arch == "x86_64":
            ar = "64"
        PACKAGES_TXT = "{0}slackware{1}-{2}/{3}".format(repo, ar, slack_ver(),
                                                        lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}slackware{1}-{2}/{3}".format(repo, ar, slack_ver(),
                                                         md5_file)
        ChangeLog_txt = "{0}slackware{1}-{2}/{3}".format(repo, ar, slack_ver(),
                                                         log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def slackr(self):
        """Creating slackers local library
        """
        repo = Repo().slackers()
        log = self.log_path + "slackr/"
        lib = self.lib_path + "slackr_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        PACKAGES_TXT = "{0}{1}".format(repo, lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}{1}".format(repo, md5_file)
        ChangeLog_txt = "{0}{1}".format(repo, log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def slonly(self):
        """Creating slackers local library
        """
        ver = slack_ver()
        ar = "{0}-x86".format(ver)
        arch = os.uname()[4]
        repo = Repo().slackonly()
        log = self.log_path + "slonly/"
        lib = self.lib_path + "slonly_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        if arch == "x86_64":
            ar = "{0}-x86_64".format(ver)
        if self.meta.slack_rel == "current" and arch == "x86_64":
            ar = "{0}-x86_64".format(self.meta.slack_rel)
        PACKAGES_TXT = "{0}{1}/{2}".format(repo, ar, lib_file)
        FILELIST_TXT = "{0}{1}/{2}".format(repo, ar, lst_file)
        CHECKSUMS_MD5 = "{0}{1}/{2}".format(repo, ar, md5_file)
        ChangeLog_txt = "{0}{1}/{2}".format(repo, ar, log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def ktown(self):
        """Creating alien ktown local library
        """
        repo = Repo().ktown()
        log = self.log_path + "ktown/"
        lib = self.lib_path + "ktown_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        PACKAGES_TXT = "{0}{1}".format(repo, lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}{1}".format(repo, md5_file)
        ChangeLog_txt = "{0}{1}".format(repo, log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def multi(self):
        """Creating alien multilib local library
        """
        ver = slack_ver()
        repo = Repo().multi()
        log = self.log_path + "multi/"
        lib = self.lib_path + "multi_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        if self.meta.slack_rel == "currnet":
            ver = self.meta.slack_rel
        PACKAGES_TXT = "{0}{1}/{2}".format(repo, ver, lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}{1}/{2}".format(repo, ver, md5_file)
        ChangeLog_txt = "{0}{1}".format(repo, log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def slacke(self):
        """Creating Slacke local library
        """
        ar = ""
        arch = os.uname()[4]
        repo = Repo().slacke()
        log = self.log_path + "slacke/"
        lib = self.lib_path + "slacke_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        if arch == "x86_64":
            ar = "64"
        elif arch == "arm":
            ar = "arm"
        PACKAGES_TXT = "{0}slacke{1}/slackware{2}-{3}/{4}".format(
            repo, self.meta.slacke_sub_repo[1:-1], ar, slack_ver(), lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}slacke{1}/slackware{2}-{3}/{4}".format(
            repo, self.meta.slacke_sub_repo[1:-1], ar, slack_ver(), md5_file)
        ChangeLog_txt = "{0}slacke{1}/slackware{2}-{3}/{4}".format(
            repo, self.meta.slacke_sub_repo[1:-1], ar, slack_ver(), log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def salix(self):
        """Creating SalixOS local library
        """
        ar = "i486"
        arch = os.uname()[4]
        repo = Repo().salix()
        log = self.log_path + "salix/"
        lib = self.lib_path + "salix_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        if arch == "x86_64":
            ar = "x86_64"
        PACKAGES_TXT = "{0}{1}/{2}/{3}".format(repo, ar, slack_ver(), lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}{1}/{2}/{3}".format(repo, ar, slack_ver(), md5_file)
        ChangeLog_txt = "{0}{1}/{2}/{3}".format(repo, ar, slack_ver(), log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def slackl(self):
        """Creating slackel.gr local library
        """
        ar = "i486"
        arch = os.uname()[4]
        repo = Repo().slackel()
        log = self.log_path + "slackl/"
        lib = self.lib_path + "slackl_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        if arch == "x86_64":
            ar = "x86_64"
        PACKAGES_TXT = "{0}{1}/current/{2}".format(repo, ar, lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}{1}/current/{2}".format(repo, ar, md5_file)
        ChangeLog_txt = "{0}{1}/current/{2}".format(repo, ar, log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def rested(self):
        """Creating alien restricted local library
        """
        repo = Repo().restricted()
        log = self.log_path + "rested/"
        lib = self.lib_path + "rested_repo/"
        lib_file = "PACKAGES.TXT"
        lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        PACKAGES_TXT = "{0}{1}".format(repo, lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}{1}".format(repo, md5_file)
        ChangeLog_txt = "{0}{1}".format(repo, log_file)
        if self.check:
            return self.checks_logs(log, log_file, ChangeLog_txt)
        self.write(lib, lib_file, PACKAGES_TXT)
        self.write(lib, md5_file, CHECKSUMS_MD5)
        self.write(log, log_file, ChangeLog_txt)
        self.remote(log, log_file, ChangeLog_txt, lib, lib_file, PACKAGES_TXT,
                    md5_file, CHECKSUMS_MD5, lst_file, FILELIST_TXT)

    def msb(self):
        """Creating MATE local library
        """
        ar = "x86"
        arch = os.uname()[4]
        repo = Repo().msb()
        log = self.log_path + "msb/"
        lib = self.lib_path + "msb_repo/"
        repo_name = log[:-1].split("/")[-1]
        lib_file = "PACKAGES.TXT"
        # lst_file = ""
        md5_file = "CHECKSUMS.md5"
        log_file = "ChangeLog.txt"
        if not os.path.exists(log):
            os.mkdir(log)
        if not os.path.exists(lib):
            os.mkdir(lib)
        if arch == "x86_64":
            ar = "x86_64"
        PACKAGES_TXT = "{0}{1}/{2}/{3}/{4}".format(
            repo, slack_ver(), self.meta.msb_sub_repo[1:-1], ar, lib_file)
        FILELIST_TXT = ""
        CHECKSUMS_MD5 = "{0}{1}/{2}/{3}/{4}".format(
            repo, slack_ver(), self.meta.msb_sub_repo[1:-1], ar, md5_file)
        ChangeLog_txt = "{0}{1}".format(repo, log_file)
        if self.check:
            return self.checks_logs(log, ChangeLog_txt)
        self.down(lib, PACKAGES_TXT, repo_name)
        self.down(lib, CHECKSUMS_MD5, repo_name)
        self.down(log, ChangeLog_txt, repo_name)
        self.remote(log, ChangeLog_txt, lib, PACKAGES_TXT, CHECKSUMS_MD5,
                    FILELIST_TXT, repo_name)

    def down(self, path, link, repo):
        filename = link.split("/")[-1]
        if not os.path.isfile(path + filename):
            Download(path, link.split(), repo).start()

    def write_file(self, path, archive, contents_txt):
        """Create local file
        """
        try:
            with open("{0}{1}".format(path, archive), "w") as f:
                for line in contents_txt.splitlines():
                    status(0.00003)
                    f.write(line + "\n")
                f.close()
        except KeyboardInterrupt:
            print("")
            sys.exit(0)

    def write(self, path, data_file, file_url):
        """Write repositories files in /var/lib/slpkg
        and /var/log/slpkg"""
        FILE_TXT = ""
        try:
            if not os.path.isfile(path + data_file):
                for fu in file_url.split():
                    FILE_TXT += URL(fu).reading()
                self.write_file(path, data_file, FILE_TXT)
        except KeyboardInterrupt:
            print("")
            sys.exit(0)

    def remote(self, *args):
        log_path = args[0]
        ChangeLog_txt = args[1]
        lib_path = args[2]
        PACKAGES_TXT = args[3]
        CHECKSUMS_MD5 = args[4]
        FILELIST_TXT = args[5]
        repo = args[6]

        check = self.checks_logs(log_path, ChangeLog_txt)
        if check == 1:
            # remove ChangeLog.txt
            os.remove("{0}{1}".format(log_path, ChangeLog_txt.split("/")[-1]))

            # remove PACKAGES.txt
            os.remove("{0}{1}".format(lib_path, PACKAGES_TXT.split("/")[-1]))

            # remove CHECKSUMS.md5
            if CHECKSUMS_MD5:
                os.remove("{0}{1}".format(lib_path,
                                          CHECKSUMS_MD5.split("/")[-1]))

            # remove FILELIST.TXT
            if FILELIST_TXT:
                os.remove("{0}{1}".format(lib_path,
                                          FILELIST_TXT.split("/")[-1]))

            # download ChangeLog.txt file
            self.down(log_path, ChangeLog_txt, repo)

            # download PACKAGES.txt file
            self.down(lib_path, PACKAGES_TXT, repo)

            # create CHECKSUMS.md5 file
            if CHECKSUMS_MD5:
                self.down(lib_path, CHECKSUMS_MD5, repo)

            # create FILELIST.TXT file
            if FILELIST_TXT:
                self.down(lib_path, FILELIST_TXT, repo)

    def checks_logs(self, log_path, url):
        """Checks ChangeLog.txt for changes
        """
        filename = url.split("/")[-1]
        server = FileSize(url).server()
        local = FileSize(log_path + filename).local()
        if server != local:
            return 1
        return 0

    def upgrade(self, only):
        """Remove all package lists with changelog and checksums files
        and create lists again"""
        repositories = self.meta.repositories
        if only:
            repositories = only
        try:
            for repo in repositories:
                changelogs = "{0}{1}{2}".format(self.log_path, repo,
                                                "/ChangeLog.txt")
                if os.path.isfile(changelogs):
                    os.remove(changelogs)
                if os.path.isdir(self.lib_path + "{0}_repo/".format(repo)):
                    for f in (os.listdir(self.lib_path + "{0}_repo/".format(
                            repo))):
                        files = "{0}{1}_repo/{2}".format(self.lib_path, repo, f)
                        if os.path.isfile(files):
                            os.remove(files)
        except KeyboardInterrupt:
            print("")
            sys.exit(0)
        Update().repository(only)


class Update(object):

    def __init__(self):
        self._init = "Initialization(False)"
        self.meta = _meta_
        self.done = "\b{0}Done{1}\n".format(self.meta.color["GREY"],
                                            self.meta.color["ENDC"])
        self.error = "\b{0}Error{1}\n".format(self.meta.color["RED"],
                                              self.meta.color["ENDC"])

    def repository(self, only):
        """Update repositories lists
        """
        print("\nCheck and update repositories:\n")
        default = self.meta.default_repositories
        enabled = self.meta.repositories
        if only:
            enabled = only
        try:
            for repo in enabled:
                sys.stdout.write("{0}Update repository {1}...{2}  ".format(
                    self.meta.color["GREY"], repo, self.meta.color["ENDC"]))
                sys.stdout.flush()
                if repo in default:
                    exec("{0}.{1}()".format(self._init, repo))
                    sys.stdout.write(self.done)
                elif repo in enabled:
                    Initialization(False).custom(repo)
                    sys.stdout.write(self.done)
                else:
                    sys.stdout.write(self.error)
        except KeyboardInterrupt:
            print("")
            sys.exit(0)
        print("")   # new line at end
        sys.exit(0)


def check_exists_repositories():
    """Checking if repositories exists by PACKAGES.TXT file
    """
    update = False
    pkg_list = "PACKAGES.TXT"
    for repo in _meta_.repositories:
        pkg_list = "PACKAGES.TXT"
        if repo == "sbo":
            pkg_list = "SLACKBUILDS.TXT"
        if not os.path.isfile("{0}{1}{2}".format(_meta_.lib_path, repo,
                                                 "_repo/{0}".format(pkg_list))):
            update = True
    if update:
        print("\n  Please update packages lists. Run 'slpkg update'.\n" +
              "  This command should be used to synchronize packages\n" +
              "  lists from the repositories are enabled.\n")
        sys.exit(0)

#!/usr/bin/python
# -*- coding: utf-8 -*-

# clean.py file is part of slpkg.

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
import shutil
from slpkg.__metadata__ import MetaData as _m


class Clean(object):
    """Clean all data like man page, log files, PACKAGES.TXT and
    configuration files. This is useful if 'slpkg' installed via
    'pip' because pip uninstalls only Python packages and script
    and not data. So after run '# pip uninstall slpkg' after run
    '# python clean.py' to remove all data and configuration file.
    """
    def __init__(self):
        self.man_path = _m.man_path
        self.bash_completion = _m.bash_completion
        self.fish_completion = _m.fish_completion
        self.conf_path = _m.conf_path
        self.log_path = _m.log_path
        self.lib_path = _m.lib_path
        self.tmp_path = _m.tmp_path
        self.man_file = "slpkg.8.gz"
        self.bash_completion_file = "slpkg.bash-completion"
        self.fish_completion_file = "slpkg.fish"

    def start(self):
        if os.path.isfile(self.man_path + self.man_file):
            print("Remove man page --> {0}".format(self.man_file))
            os.remove(self.man_path + self.man_file)
        if os.path.isfile(self.bash_completion + self.bash_completion_file):
            print("Remove bash completion file --> {0}".format(
                self.bash_completion_file))
            os.remove(self.bash_completion + self.bash_completion_file)
        if os.path.isfile(self.fish_completion + self.fish_completion_file):
            print("Remove fish completion file --> {0}".format(
                self.fish_completion_file))
            os.remove(self.fish_completion + self.fish_completion_file)
        if os.path.exists(self.conf_path):
            print("Remove configuration directory --> {0}".format(
                self.conf_path))
            shutil.rmtree(self.conf_path)
        if os.path.exists(self.log_path):
            print("Remove log data directory --> {0}".format(self.log_path))
            shutil.rmtree(self.log_path)
        if os.path.exists(self.lib_path):
            print("Remove library data directory --> {0}".format(self.lib_path))
            shutil.rmtree(self.lib_path)
        if os.path.exists(self.tmp_path):
            print("Remove temponary directory --> {0}".format(self.tmp_path))
            shutil.rmtree(self.tmp_path)

if __name__ == '__main__':
    Clean().start()

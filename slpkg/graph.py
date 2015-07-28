#!/usr/bin/python
# -*- coding: utf-8 -*-

# graph.py file is part of slpkg.

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
import subprocess


def graph_deps(deps_dict, image):
    """Generate graph file with depenndencies map tree
    """
    try:
        import pygraphviz as pgv
    except ImportError:
        print("Require 'pygraphviz': Install with '$ slpkg -s sbo pygraphviz'")
        raise SystemExit()
    if image != "ascii":
        check_file(image)
    try:
        G = pgv.AGraph(deps_dict)
        G.layout(prog="fdp")
        if image == "ascii":
            G.write("{0}.dot".format(image))
            graph_easy(image)
        G.draw(image)
    except (IOError, KeyboardInterrupt):
        raise SystemExit()
    if os.path.isfile(image):
        print("Graph image file '{0}' created".format(image))
    raise SystemExit()


def check_file(image):
    """Check for file format and type
    """
    file_format = ["bmp", "canon", "cmap", "cmapx", "cmapx_np", "dot", "eps",
                   "fig", "gd", "gd2", "gif", "gtk", "gv", "ico", "imap",
                   "imap_np", "ismap", "jpe", "jpeg", "jpg", "pdf", "pic",
                   "plain", "plain-ext", "png", "pov", "ps", "ps2", "svg",
                   "svgz", "tif", "tiff", "tk", "vml", "vmlz", "vrml", "wbmp",
                   "x11", "xdot", "xlib"
                   ]
    try:
        if image.split(".")[1] not in file_format:
            print("Format: {0} not recognized. Use one of: {1}".format(
                image.split(".")[1], " ".join(file_format)))
            raise SystemExit()
    except IndexError:
        print("slpkg: error: Image file suffix missing")
        raise SystemExit()


def graph_easy(image):
    """Draw ascii diagram. graph-easy perl modulr require
    """
    if not os.path.isfile("/usr/bin/graph-easy"):
        print("Require 'graph-easy': Install with '$ slpkg -s sbo graph-easy'")
        remove_dot(image)
        raise SystemExit()
    subprocess.call("graph-easy {0}.dot".format(image), shell=True)
    remove_dot(image)
    raise SystemExit()


def remove_dot(image):
    """Remove .dot files
    """
    if os.path.isfile("{0}.dot".format(image)):
        os.remove("{0}.dot".format(image))

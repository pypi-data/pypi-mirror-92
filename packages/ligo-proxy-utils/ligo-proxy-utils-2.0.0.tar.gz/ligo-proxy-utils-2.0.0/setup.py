# -*- coding: utf-8 -*-
# Copyright 2021 Cardiff University
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""Build configuration for ligo-grid-mapfile-manager
"""

import re
from pathlib import Path

from setuptools import setup

try:
    from build_manpages.build_manpages import (
        build_manpages,
        get_build_py_cmd,
        get_install_cmd,
    )
except ImportError:  # can't build manpages, that's ok
    cmdclass = {}
else:
    from setuptools.command.build_py import build_py
    from setuptools.command.install import install
    cmdclass = {
        "build_manpages": build_manpages,
        "build_py": get_build_py_cmd(build_py),
        "install": get_install_cmd(install),
    }

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"


def find_version(path, varname="__version__"):
    """Parse the version metadata in the given file.
    """
    with Path(path).open('r') as fobj:
        version_file = fobj.read()
    version_match = re.search(
        r"^{0} = ['\"]([^'\"]*)['\"]".format(varname),
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# this function only manually specifies things that aren't
# supported by setup.cfg (as of setuptools-30.3.0)
setup(
    cmdclass=cmdclass,
    version=find_version(Path('ligo_proxy_utils') / "__init__.py"),
)

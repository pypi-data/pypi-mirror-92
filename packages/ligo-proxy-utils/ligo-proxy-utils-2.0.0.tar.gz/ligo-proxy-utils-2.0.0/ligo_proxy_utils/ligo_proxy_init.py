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

"""Generate a LIGO.ORG X.509 credential using CIECPLib
"""

import argparse
import warnings

from ciecplib.tool.ecp_get_cert import main as ecp_get_cert

from . import __version__

DEFAULT_HOURS = 277
DEFAULT_IDPHOSTS = [
    "login.ligo.org",
    "login2.ligo.org",
]


def create_parser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="ligo-proxy-init",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="write debug output to stdout",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="write version information to stdout",
    )
    parser.add_argument(
        "-i",
        "--idp-host",
        dest="idp_hosts",
        metavar="hostname",
        default=argparse.SUPPRESS,
        help=(
            "use alternative IdP host, e.g. 'login2.ligo.org', default tries "
            "each of: {}".format(", ".join(DEFAULT_IDPHOSTS))
        ),
    )
    parser.add_argument(
        "-k",
        "--kerberos",
        action="store_true",
        default=False,
        help="enable kerberos negotiation, do not provide username",
    )
    parser.add_argument(
        "-p",
        "--proxy",
        action="store_true",
        default=False,
        help="create RFC 3820 compliant impersonation proxy",
    )
    parser.add_argument(
        "-H",
        "--hours",
        type=int,
        metavar="h",
        default=DEFAULT_HOURS,
        help="proxy is valid for h hours",
    )
    parser.add_argument(
        "-X",
        "--destroy",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "username",
        nargs="?",
        help="username (required if not using --kerberos)",
    )

    # augment parser for argparse-manpage
    parser.man_short_description = "generate an X.509 credential"

    return parser


def parse_command_line(args):
    parser = create_parser()
    args = parser.parse_args(args=args)
    if (
            not (args.version or args.destroy) and
            not (args.username or args.kerberos)
    ):
        parser.error("username is required if not using --kerberos")
    try:  # format --idp-host argument as a list of one
        args.idp_hosts = [args.idp_hosts]
    except AttributeError:  # not given, use defaults
        args.idp_hosts = DEFAULT_IDPHOSTS
    return args


def version(args):
    print("ligo-proxy-init version {}".format(__version__))
    print("ciecplib version", end=" ")
    return ecp_get_cert(args + ["--version"])


def ligo_proxy_init(args=None):
    args = parse_command_line(args)

    # map arguments
    ciecplibargs = []
    if args.username:
        ciecplibargs.extend(("--username", args.username))
    if args.kerberos:
        ciecplibargs.append("--kerberos")
    if args.proxy:
        ciecplibargs.append("--proxy")
    if args.debug:
        ciecplibargs.append("--debug")
    ciecplibargs.extend(("--hours", str(args.hours)))

    # handle special modes
    if args.version:
        return version(ciecplibargs)

    if args.destroy:
        return ecp_get_cert(ciecplibargs + ["--destroy"])

    # run the thing
    for idp in args.idp_hosts:
        curargs = ciecplibargs + [
            "--identity-provider", idp,
        ]
        if args.debug:
            print("Delegating call to ecp_get_cert...")
            print("$ ecp_get_cert {}".format(" ".join(curargs)))
        try:
            ecp_get_cert(curargs)
        except Exception as exc:  # _all_ exceptions are caught
            if idp == args.idp_hosts[-1]:
                raise
            warnings.warn(
                "Caught {}: {}".format(type(exc).__name__, str(exc)),
            )
        else:
            return


if __name__ == "__main__":
    ligo_proxy_init()

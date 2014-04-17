#!/usr/bin/env python3
#
# MinIRC - A modern IRC library using asyncio
#
# Copyright (C) 2013-2014 - Thibaut DIRLIK (thibaut.dirlik@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import sys
import argparse

from minirc.client import Connection


@asyncio.coroutine
def main():

    parser = argparse.ArgumentParser(prog='minirc-cat')
    parser.add_argument('--server', dest='server', action='store', help='Server address', required=True)
    parser.add_argument('--port', dest='port', default=6667, type=int, action='store')
    parser.add_argument('--nick', dest='nick', action='store', required=True)
    parser.add_argument('--ident', dest='ident', default=None, action='store')
    parser.add_argument('--name', dest='name', default=None, action='store')

    args = parser.parse_args(sys.argv[1:])

    if args.ident is None:
        args.ident = args.nick
    if args.name is None:
        args.name = args.nick

    conn = Connection()

    yield from conn.connect(args.server, args.port)
    print('conencted')
    conn.auth(args.nick, args.ident, args.name)
    print('authed')
    yield from conn.run()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

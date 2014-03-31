# AsyncIRC - A modern IRC library using asyncio
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

import re

_ENCODINGS = ('utf-8', 'cp1252')


def irc_decode(data, encodings=_ENCODINGS):
    for encoding in encodings:
        try:
            return data.decode(encoding, errors='strict')
        except UnicodeDecodeError:
            continue
    return data.decode('ascii', errors='ignore')


def split_userhost(userhost):
    split = re.split(r'[!@]', userhost, maxsplit=2)
    nick = split.pop(0)
    ident = split and split.pop(0) or None
    host = split and split.pop(0) or None
    return nick, ident, host
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
    """ Returns a 3-tuple nick, ident, host from the scpecified userhost.

    The returned ``ident`` and ``host`` can be ``None``

    :param userhost: A string in the format ``<nick>[!<ident>@<host>]``.
    """
    nick, _, ident_host = userhost.rpartition('!')
    if not _:  # No '!'
        nick = None
    ident, _, host = ident_host.rpartition('@')
    if not _:  # No '@'
        if nick:
            ident = host
            host = None
        else:
            nick = userhost
            ident = None
            host = None
    if not ident:
        ident = None
    if not host:
        host = None
    if not nick:
        nick = None
    return nick, ident, host
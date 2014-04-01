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


def irc_decode(data):
    """ Decodes bytes coming from IRC.

    This function will try to encode the bytes using the UTF-8 encoding
    which is becoming one of the most used encoding on IRC.

    However, in case of error, it will fallback using the latin-1 encoding,
    which is a codepoint-to-byte encoding, and can't fail.
    """
    try:
        return data.decode('utf-8', errors='strict')
    except UnicodeDecodeError:
        return data.decode('latin-1')


def split_userhost(userhost):
    """ Returns a 3-tuple nick, ident, host from the scpecified userhost.

    The returned ``ident`` and ``host`` can be ``None``

    :param userhost: A string in the format ``<nick>[!<ident>@<host>]``.
    """
    nick, _, ident_host = userhost.rpartition('!')
    if not _:  # No '!', this means we only have a nick, or user@host.
        if '@' not in ident_host:
            return userhost, None, None
        nick = None
    elif nick == '':
        nick = None
    ident, _, host = ident_host.rpartition('@')
    if not _:  # No '@' ! This means we only have an ident.
        ident = None if host == '' else host
        host = None
    if ident == '':
        ident = None
    if host == '':
        host = None
    return nick, ident, host
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

from minirc.tools import irc_decode, split_raw

IRC_CONNECTED = 'connected'  # Connection established
IRC_AUTHED = 'authed'  # Connection established and credentials accepted
IRC_DISCONNECTED = 'disconnected'  # Disconnected


class Connection:

    def __init__(self, encoding='utf-8', loop=None):
        """ Creates a new connection to an IRC server. """
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._stream_reader = None
        self._stream_writer = None
        self._encoding = encoding
        # This future will be set once we got a 001 raw. If the authentication fails,
        # an IRCError exception will be raised, with detailed information.
        self._authed = asyncio.Future(loop=loop)
        self.status = IRC_DISCONNECTED

    def send(self, line, *args, **kwargs):
        if line[-1] != '\n':
            line += '\n'
        if args or kwargs:
            line = line.format(*args, **kwargs)
        self._stream_writer.write(line.encode('utf-8'))

    @asyncio.coroutine
    def connect(self, host, port, ssl=None):
        """ Connects to the specified IRC server. """
        self._stream_reader, self._stream_writer = yield from asyncio.open_connection(
            host, port, ssl=ssl, loop=self._loop)
        self.status = IRC_CONNECTED

    @asyncio.coroutine
    def auth(self, nick, ident, realname, password=None):
        """ Authenticate to the IRC server. """
        self.send('NICK {}', nick)
        self.send('USER 0 0 {} :{}', ident, realname)
        if password:
            self.send('PASS :{}', password)
        yield from self._authed
        self.status = IRC_AUTHED

    @asyncio.coroutine
    def run(self):
        while True:
            data = yield from self._stream_reader.readline()
            if len(data) == 0:
                break
            if data[-1] == 10:  # 10 = \n
                data = data[:-1]
            if data[-1] == 13:  # 13 = \r
                data = data[:-1]
            origin, command, args = split_raw(irc_decode(data))
            print(origin, command, args)
            if command == '001':
                self._authed.set_result(True)

class Channel:
    pass


class User:
    pass

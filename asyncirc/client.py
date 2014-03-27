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

import asyncio

from asyncirc.tools import irc_decode

# A tuple of encodings that will be tried when recieving a message. If UTF8 failed, the message will be decoded
# using CP1252, and it fails again, unknown character will be replaced by '?'.
INPUT_ENCODINGS = ('utf-8', 'cp1252')


class Connection:

    def __init__(self, nick, ident, realname, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._stream_reader = None
        self._stream_writer = None
        self._nick = nick
        self._ident = ident
        self._realname = realname

    def send(self, line, *args, **kwargs):
        if line[-1] != '\n':
            line += '\n'
        if args or kwargs:
            line = line.format(*args, **kwargs)
        self._stream_writer.write(line.encode('utf-8'))

    @asyncio.coroutine
    def connect(self, host, port, password=None, ssl=None):
        self._stream_reader, self._stream_writer = yield from asyncio.open_connection(
            host, port, ssl=ssl, loop=self._loop)
        self.send('NICK {}', self._nick)
        self.send('USER 0 0 {} :{}', self._ident, self._realname)
        if password:
            self.send('PASS {}', password)

    @asyncio.coroutine
    def run(self):
        while True:
            data = yield from self._stream_reader.readline()
            if len(data) == 0:
                break
            line = irc_decode(data)
            print(line)


class Channel:
    pass


class User:
    pass


if __name__ == '__main__':
    e = asyncio.get_event_loop()
    c = Connection('LOOOOL', 'MDR', 'LOOL')
    e.run_until_complete(c.connect('irc.freenode.org', 6667))
    e.run_until_complete(c.run())

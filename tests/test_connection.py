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

from minirc.testing import AsyncIRCBaseTestCase, asynctest
from minirc.client import IRC_CONNECTED, IRC_DISCONNECTED, IRC_AUTHED


class TestConnection(AsyncIRCBaseTestCase):

    @asynctest
    def test_connect(self):
        yield from self.conn.connect(self.server_host, self.server_port)
        self.assertEquals(IRC_CONNECTED, self.conn.status)
        self.conn.disconnect()

    @asynctest
    def test_authed(self):
        yield from self.conn.connect(self.server_host, self.server_port)
        #self.conn.disconnect()
        # self.get_fake_data('traffic/auth.txt')
        # self.conn.auth('Minirc', 'minirc', 'MinIRC!', 'password')
        # yield from self.conn.events['authed'].wait()
        # self.assertEquals(IRC_AUTHED, self.conn.status)
        # self.assertSent('NICK Minirc', 0)
        # self.assertSent('USER 0 0 minirc :MinIRC!', 1)
        # self.assertSent('PASS :password', 2)

    @asynctest
    def test_disconnected(self):
        yield from self.conn.connect(self.server_host, self.server_port)
        self.get_fake_data('traffic/auth.txt', eof=True)
        # self.conn.disconnect()
        # yield from self.conn_run_fut
        # self.assertEquals(IRC_DISCONNECTED, self.conn.status)

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

from minirc.testing import AsyncIRCBaseTestCase
from minirc.client import Connection, IRC_CONNECTED, IRC_DISCONNECTED


class TestConnection(AsyncIRCBaseTestCase):

    def get_incoming_data_generator(self):
        with open('traffic/freenode.txt', 'br') as file:
            yield from file

    def test_connect(self):
        self.assertEquals(IRC_CONNECTED, self.conn.status)

    def test_authed(self):
        self.wait(self.conn.auth, 'Minirc', 'minirc', 'MinIRC!', 'password')
        self.assertSent('NICK Minirc', 0)
        self.assertSent('USER 0 0 minirc :MinIRC!', 1)
        self.assertSent('PASS :password', 2)

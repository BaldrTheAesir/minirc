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

from asyncirc.testing import AsyncIRCBaseTestCase
from asyncirc.client import Connection


class TestConnection(AsyncIRCBaseTestCase):

    def get_incoming_data_generator(self):
        with open('traffic/freenode.txt', 'br') as file:
            yield from file

    def test_connect_success(self):
        conn = Connection('nick', 'ident', 'realname')
        self.loop.run_until_complete(conn.connect('localhost', 8888))
        self.loop.run_until_complete(conn.run())

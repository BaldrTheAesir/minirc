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

from unittest import TestCase
from asyncirc.tools import irc_decode, split_userhost


class TestTools(TestCase):

    def test_splituserhost(self):
        nick, ident, host = split_userhost('nick!ident@host')
        self.assertEqual(nick, 'nick')
        self.assertEqual(ident, 'ident')
        self.assertEqual(host, 'host')
        nick, ident, host = split_userhost('nick!ident')
        self.assertEqual(nick, 'nick')
        self.assertEqual(ident, 'ident')
        self.assertEqual(host, None)
        nick, ident, host = split_userhost('nick')
        self.assertEqual(nick, 'nick')
        self.assertEqual(ident, None)
        self.assertEqual(host, None)
        nick, ident, host = split_userhost('')
        self.assertEqual(nick, '')
        self.assertEqual(ident, None)
        self.assertEqual(host, None)

    def test_irc_decode(self):
        pass
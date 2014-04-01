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

    def test_splituserhost_full(self):
        nick, ident, host = split_userhost('nick!ident@host')
        self.assertEqual('nick', nick)
        self.assertEqual('ident', ident)
        self.assertEqual('host', host)

    def test_splituserhost_nohost(self):
        nick, ident, host = split_userhost('nick!ident')
        self.assertEqual('nick', nick)
        self.assertEqual('ident', ident)
        self.assertEqual(None, host)

    def test_splituserhost_noident(self):
        nick, ident, host = split_userhost('nick!@host')
        self.assertEqual('nick', nick)
        self.assertEqual(None, ident)
        self.assertEqual('host', host)

    def test_splituserhost_noident_nohost(self):
        nick, ident, host = split_userhost('nick!@')
        self.assertEqual('nick', nick)
        self.assertEqual(None, ident)
        self.assertEqual(None, host)

    def test_splituserhost_nonick(self):
        nick, ident, host = split_userhost('ident@host')
        self.assertEqual(None, nick)
        self.assertEqual('ident', ident)
        self.assertEqual('host', host)
        nick, ident, host = split_userhost('!ident@host')
        self.assertEqual(None, nick)
        self.assertEqual('ident', ident)
        self.assertEqual('host', host)

    def test_splituserhost_nothing(self):
        nick, ident, host = split_userhost('nick')
        self.assertEqual('nick', nick)
        self.assertEqual(None, ident)
        self.assertEqual(None, host)

    def test_splituserhost_multiplechars(self):
        # This should never happen. However, we consider the right-most character
        # to be the one doing the separation between nick/ident/host.
        nick, ident, host = split_userhost('nick!nick@ident!ident@ident@host')
        self.assertEqual('nick!nick@ident', nick)
        self.assertEqual('ident@ident', ident)
        self.assertEqual('host', host)

    def test_irc_decode(self):
        utf_8_bytes = 'ބ'.encode('utf-8')
        utf_16_bytes = 'ބ'.encode('utf-16')
        utf_32_bytes = 'ބ'.encode('utf-32')
        self.assertEquals(irc_decode(utf_8_bytes), 'ބ')
        self.assertEquals(irc_decode(utf_16_bytes), '\xff\xfe\x84\x07')
        self.assertEquals(irc_decode(utf_32_bytes), '\xff\xfe\x00\x00\x84\x07\x00\x00')

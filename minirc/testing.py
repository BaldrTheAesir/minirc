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

""" This module provides tools to unit-test minirc. """

import unittest
import asyncio
import asyncio.test_utils
import functools
import contextlib

from unittest.mock import MagicMock
from minirc.client import Connection


def asynctest(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        @asyncio.coroutine
        def wrapped_coro():
            yield from func(self, *args, **kwargs)
        return self.loop.run_until_complete(wrapped_coro())
    return wrapper


class AsyncIRCBaseTestCase(unittest.TestCase):

    @asyncio.coroutine
    def _create_connection(self, *args, **kwargs):
        """ A fake function to simulate BaseEventLoop.create_connection(). """
        return self.transport, None

    def setUp(self):
        self.conn_run_fut = False
        self.writer_data = []
        self.transport = MagicMock(spec=asyncio.transports.Transport)
        self.transport.write = self.writer_data.append
        self.transport.close = lambda: self.conn._stream_reader.feed_eof()
        self.loop = asyncio.new_event_loop()
        self.loop.create_connection = self._create_connection
        self.conn = Connection(loop=self.loop)

    def tearDown(self):
        if self.conn_run_fut:
            self.get_fake_eof()
            asyncio.wait_for(self.conn_run_fut, timeout=None, loop=self.loop)

    def get_fake_data(self, *files, eof=True):
        if self.conn_run_fut is False:
            self.conn_run_fut = asyncio.async(self.conn.run(), loop=self.loop)
        for filename in files:
            with open(filename, 'rb') as file:
                for line in file:
                    self.conn._stream_reader.feed_data(line)
        if eof:
            self.get_fake_eof()

    def get_fake_eof(self):
        self.conn._stream_reader.feed_eof()

    def assertSent(self, data, position=None):
        """ Asserts that the specified data has been sent.

        The "\n" is not needed at the end, for simplicity,
        it is added automatically.

        If a ``position`` is specified, it must be at the ``position`` in the
        sent queue, starting from 0.
        """
        if data[-1] != '\n':
            data += '\n'
        data = data.encode('utf-8')
        if position is not None:
            if position+1 > len(self.writer_data):
                self.fail('No data at the specified position')
            self.assertEquals(self.writer_data[position], data)
        else:
            self.assertIn(data, self.writer_data)

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

    @asyncio.coroutine
    def start_server(self):
        """ Starts a local server to recieve connection. """
        self.server = yield from asyncio.start_server(self._client_connected,
            host='localhost', loop=self.loop)
        sock = self.server.sockets[0]
        full_addr = sock.getsockname()
        host, port = full_addr[0], full_addr[1]  # Could contain more elements if IPv6
        return host, port

    @asyncio.coroutine
    def _client_connected(self, reader, writer):
        self.client_reader = reader
        self.client_writer = writer

    def setUp(self):
        self.writer_data = []
        self.loop = asyncio.new_event_loop()
        self.server_host, self.server_port = self.loop.run_until_complete(self.start_server())
        self.conn = Connection(loop=self.loop)
        self.conn_run_fut = None

    def tearDown(self):
        self.client_writer.close()
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())

    def get_fake_data(self, *files, eof=True):
        if self.conn_run_fut is None:
            self.conn_run_fut = asyncio.async(self.conn.run(), loop=self.loop)
        for filename in files:
            with open(filename, 'rb') as file:
                self.client_writer.writelines(file)
        if eof:
            self.client_writer.close()

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

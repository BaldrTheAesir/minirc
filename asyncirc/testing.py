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

""" This module provides tools to unit-test asyncirc. """

import unittest
import asyncio

from unittest.mock import patch


class AsyncIRCBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.writer_data = []
        self.reader_data = self.get_incoming_data_generator()
        self.loop = asyncio.get_event_loop()
        self.patch_open_connection()

    def get_incoming_data_generator(self):
        return iter([])

    def patch_stream_reader(self):
        self.stream_reader_patch = patch('asyncio.StreamReader', spec=asyncio.StreamReader)
        self.stream_reader_patch.readline = asyncio.coroutine(lambda: next(self.reader_data, b''))
        self.stream_reader_patch.start()
        self.addCleanup(self.stream_reader_patch.stop)

    def patch_stream_writer(self):
        self.stream_writer_patch = patch('asyncio.StreamWriter', spec=asyncio.StreamWriter)
        self.stream_writer_patch.write = lambda data: self.writer_data.append(data)
        self.stream_writer_patch.start()
        self.addCleanup(self.stream_writer_patch.stop)

    def patch_open_connection(self):
        self.patch_stream_reader()
        self.patch_stream_writer()
        result = asyncio.Future()
        result.set_result((self.stream_reader_patch, self.stream_writer_patch))
        patcher = patch.object(asyncio, 'open_connection', return_value=result)
        patcher.start()
        self.addCleanup(patcher.stop)

    def assertFirstSent(self, data, clean=True):
        if clean:
            sent_data = self.writer_data.pop(0)
        else:
            sent_data = self.writer_data[0]
        self.assertEquals(sent_data, data)

    def assertSent(self, data):
        self.assertIn(self.writer_data, data)

    def assertNothingSent(self):
        self.assertEquals(len(self.writer_data), 0)
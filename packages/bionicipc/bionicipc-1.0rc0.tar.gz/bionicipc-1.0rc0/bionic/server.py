# Copyright 2020 h3xcode
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# cuz bug with unsubscriptable Union in Python 3.9
# pylint: disable=unsubscriptable-object

"""Module with high-level server abstractions for Bionic IPC"""

import asyncio
import logging

from typing import Union

from . import models, utils, get_version, WATCHDOG_SLEEP
from .connection import Connection, create_connection
from .errors import recognize_error
from .sync import ConnectionLock

logger = logging.getLogger("BionicServer")


class BionicServer:
    """Bionic server"""
    _connection: Connection = None
    _connection_lock: ConnectionLock = ConnectionLock()
    callback_func: callable = None

    def __init__(self):
        logger.info("Initializing BionicIPC v%s", get_version())
        self._loop = asyncio.get_event_loop()
        asyncio.ensure_future(self._watchdog())

    def set_callback(self, func: callable):
        """Set callback for connection"""
        self.callback_func = func

    async def _watchdog(self):
        """Watcher for connection errors"""
        while True:
            await asyncio.sleep(WATCHDOG_SLEEP)
            if self._connection:
                if not self._connection.closed:
                    continue
            logger.warning(
                "Connection closed or broken. Waiting for new one...")
            self._connection_lock.unlock()
            await self._connection_lock
            logger.warning("Connection established.")

    async def _internal_callback(self, reader, writer):
        """Connection listener"""
        logger.info(
            "New connection from %s:%i!", *writer.get_extra_info("peername"))
        if self._connection_lock.get_state():
            writer.close()
            await writer.wait_closed()
            return None
        self._connection = create_connection(reader, writer)
        logger.warning("Connection established with %s:%i",
                       *writer.get_extra_info("peername"))
        self._connection.set_callback(self.callback_func)
        self._connection_lock.lock()

    async def wait_connection(self):
        """Wait for connection"""
        await self._connection_lock

    async def send_call(self, method: str, params: Union[list, dict],
                        raise_on_error: bool = False, return_only_result: bool = False):
        """Wrapper for Connection.send_call()"""
        try:
            if not self._connection_lock.get_state():
                raise ConnectionResetError
            result = await self._connection.send_call(
                models.Call(
                    get_version(),
                    method,
                    params
                )
            )
            utils.raise_if_flag(recognize_error(result.error), raise_on_error)
            return result.result if return_only_result else result
        except ConnectionResetError:
            logger.warning(
                "Looks like no connection. Pausing all transactions...")
            self._connection_lock.unlock()
            await self._connection_lock
            return await self.send_call(method, params)

    async def send_notification(self, method: str, params: Union[list, dict]):
        """Wrapper for Connection.send_notification()"""
        try:
            if not self._connection_lock.get_state():
                raise ConnectionResetError
            return await self._connection.send_notification(
                models.Notification(
                    get_version(),
                    method,
                    params
                )
            )
        except ConnectionResetError:
            logger.warning(
                "Looks like no connection. Pausing all transactions...")
            self._connection_lock.unlock()
            await self._connection_lock
            return await self.send_notification(method, params)

    def start_server(self, host: str = "127.0.0.1", port: int = 8122):
        """Start listening"""
        logger.info("Listening %s on %i", host, port)
        return asyncio.start_server(self._internal_callback, host, port)

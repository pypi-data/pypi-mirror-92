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

"""Module with high-level client abstractions for Bionic IPC"""


import asyncio
import logging

from typing import Union

from . import models, utils, get_version
from .connection import Connection, create_connection
from .errors import recognize_error
from .sync import ConnectionLock

logger = logging.getLogger("BionicClient")


class BionicClient:
    """Bionic client"""
    _connection: Connection = None
    _connection_lock = ConnectionLock()
    max_reconnection_attempts = 5
    reconnection_timeout = 2
    sleep_full = 10
    callback_func: callable = None
    host: str
    port: int

    def __init__(self):
        logger.info("Initializing BionicIPC v%s", get_version())

    def set_callback(self, func: callable):
        """Set callback for connection"""
        self.callback_func = func

    async def connect(self, host: str = "127.0.0.1", port: int = 8122) -> bool:
        """Connect to host, returns True if successful"""
        self.host, self.port = host, port
        logger.info("Connecting to %s:%i", self.host, self.port)
        try:
            self._connection = create_connection(*(await asyncio.open_connection(host, port)))
        except ConnectionRefusedError as e_obj:
            logger.error("Connect to host failed: %s", str(e_obj))
            return False
        if self._connection:
            logger.info("Connected to %s:%i", self.host, self.port)
            asyncio.ensure_future(self._reconn())
            self._connection.set_callback(self.callback_func)
            self._connection_lock.lock()
            return True

    async def _reconn(self):
        """Watcher for connection errors"""
        attempts = 0
        notified = False
        while True:
            if self._connection.closed:
                self._connection_lock.unlock()
                if not notified:
                    logger.warning("Connection closed, trying to reconnect...")
                    notified = True
                logger.debug("[%i/%i] Connecting to %s:%i", attempts,
                             self.max_reconnection_attempts, self.host, self.port)
                try:
                    self._connection = create_connection(
                        *(await asyncio.open_connection(self.host, self.port)))
                    logger.info("Connection success!")
                    attempts = 0
                    notified = False
                    self._connection_lock.lock()
                    continue
                except ConnectionRefusedError as e_obj:
                    logger.debug(e_obj)
                    attempts += 1
                    if attempts > self.max_reconnection_attempts:
                        logger.warning(
                            "The maximum number of attempts has\
                            been reached, sleeping for %i seconds..", self.sleep_full)
                        attempts = 0
                        await asyncio.sleep(self.sleep_full)
            await asyncio.sleep(self.reconnection_timeout)

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
            return result.result.get_data() if return_only_result else result
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

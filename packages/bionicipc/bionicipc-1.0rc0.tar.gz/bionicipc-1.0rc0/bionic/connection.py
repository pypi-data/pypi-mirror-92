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

"""Abstractions for representing asyncio stream as Bionic Connection"""

import zlib
import asyncio
import secrets
import warnings
import logging


from . import models, errors
from .sync import NamedQueue

logger = logging.getLogger("Connection")


async def fallback_cb(connection, data):
    """Dummy fallback cb"""
    warnings.warn(
        "Fell in fallback_cb, please set callback for connection")
    return errors.INTERNAL_SERVER_ERROR


class Connection:
    """Bionic connection

    High level abstraction for asyncio socket stream. Designed for
    Bionic models. Uses a string that is separated from the data with
    a space to identify calls and returns. Takes asyncio.StreamReader
    and asyncio.StreamWriter, obtained from asyncio server callback.
    After initialization it starts infinite stream listening (listen_loop).
    """
    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter
    _queue: NamedQueue = NamedQueue()
    callback = fallback_cb
    closed: bool = False

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        logger.debug("Initiated a new connection")
        self._reader = reader
        self._writer = writer
        asyncio.ensure_future(self.listen_loop())

    def set_callback(self, func: callable):
        """Set callback for connection"""
        self.callback = func or fallback_cb

    async def _communicate(self, data: bytes, register: bool = True, uid: str = None) -> str:
        """Internal method for low-level communicate with other side
        of the connection. Generates uid if not provided. Auto register
        request to queue, if need.
        """
        uid = uid or secrets.token_hex(8)
        logger.debug("Preparing for send %s", uid)
        crc = zlib.crc32(data)
        if register:
            logger.debug("Registering %s in queue", uid)
            self._queue.register(uid)
        d_send = data+b" "+uid.encode()+b" "+hex(crc).encode()+b"\n"
        logger.debug("Sending: %s", str(d_send))
        self._writer.write(d_send)
        await self._writer.drain()
        return uid

    async def _raise_internal_error(self, error: tuple, uid: str):
        """Errors raiser for internal purposes"""
        await self._communicate(
            models.create_respond(models.Error(*error)).get_raw_data(), register=False, uid=uid)

    def get_wait_tasks(self) -> int:
        """Get socket i/o waiters

        Returns waiters count as integer.
        """
        return self._queue.waiters_count()

    async def listen_loop(self):
        """Infinite listen loop

        Used by all internal tasks to obtain any data from other side of
        the connection. Uses NamedQueue to synchronize data distribution.
        """
        while True:
            data_raw: bytes = await self._reader.readline()
            if data_raw == b"":
                logger.warning("Empty data, closing connection!")
                self._writer.close()
                await self._writer.wait_closed()
                self.closed = True
                return
            logger.debug("Received data. Decrypting...")
            try:
                data, uid, crc = tuple(data_raw[:-1].split(b" "))
            except ValueError:
                logger.debug("Failed to parse data, skipping...")
                continue

            uid, crc = uid.decode(), crc.decode()
            logger.debug("Parse successfull, uid: %s", uid)

            if not hex(zlib.crc32(data)) == crc:
                logger.debug("Invalid data CRC for %s, skipping...", uid)
                continue

            logger.debug("Pushing %s to queue", uid)
            if not self._queue.commit(uid, data):
                logger.debug("%s not in queue, calling cb", uid)
                try:
                    pdata = models.parse_data(data)
                except models.ParseError:
                    await self._raise_internal_error(errors.TRANSACTION_PARSE_ERROR, uid)
                    continue
                call = False
                if isinstance(pdata, models.Call):
                    call = True
                try:
                    ret = await self.callback(self, pdata)
                except Exception:  # pylint: disable=broad-except
                    logger.exception("Error while executing callback")
                    await self._raise_internal_error(errors.INTERNAL_SERVER_ERROR, uid)
                    continue
                if not ret:
                    if call:
                        logger.error(
                            "Callback must return smth, because %s is call.", uid)
                        await self._raise_internal_error(errors.INTERNAL_SERVER_ERROR, uid)
                        continue
                    await self._communicate(b"ok", register=False, uid=uid)
                else:
                    await self._communicate(
                        models.create_respond(ret).get_raw_data(), register=False, uid=uid)

    async def wait_data(self, uid: str) -> bytes:
        """Block until the uid data is received

        Waiting for listen_loop to get data that matches the given
        uid. Returns bytes on completion.
        """
        logger.debug("Waiting for %s", uid)
        return await self._queue.wait(uid)

    async def send_call(self, call: models.Call) -> models.Respond:
        """Send Bionic call to other side of the connection

        Sends the other side of the connection a Bionic call, and
        blocks it until it receives a reply. Can raise the response
        parsing exception. Returns models.Respond in case if success.

        @returns models.Respond
        """
        logger.debug("Sending call")
        uid = await self._communicate(call.get_raw_data())
        return models.parse_data(await self.wait_data(uid))

    async def send_notification(self, notification: models.Notification) -> bool:
        """Send Bionic notification to other side of the connection
        """
        logger.debug("Sending notification")
        uid = await self._communicate(notification.get_raw_data())
        if (await self.wait_data(uid)) == b"ok":
            return True
        logger.warning("Notification failed!")
        return False


def create_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> Connection:
    """Create Connection from asyncio StreamReader and StreamWriter
    """
    return Connection(reader, writer)

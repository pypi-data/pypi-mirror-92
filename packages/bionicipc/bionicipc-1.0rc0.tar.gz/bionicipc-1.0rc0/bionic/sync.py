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

"""Bionic utils for synchronization"""

from asyncio import events


class UndefinedTaskException(Exception):
    """Undefined task"""
    ...


class NamedQueue:
    """A named queue where each element has its own id

    Provides the ability to asynchronously control the receipt
    and transmission of data. Requires an identifier for each data block
    """

    def __init__(self):
        self._tasks = {}
        self._loop = events.get_event_loop()

    def register(self, uid: str):
        """Register an item to the queue.

        It is needed in order to prevent possible errors due to the
        fact that the data will arrive earlier than they may be waited
        """
        fut = self._loop.create_future()
        self._tasks[uid] = fut

    def commit(self, uid: str, data: bytes):
        """Commit to unfinished task. All coroutines waiting for
        task finish are awakened. If task uid isn`t in tasks,
        UndefinedTaskException will be raised.
        """
        if uid not in self._tasks:
            return False

        fut = self._tasks[uid]
        if not fut.done():
            fut.set_result(data)
        return True

    def clear(self):
        """Reset the internal tasks store to empty state"""
        self._tasks = {}

    def waiters_count(self) -> int:
        """Return waiters count"""
        return len(self._tasks)

    async def wait(self, uid: str) -> bytes:
        """Block until the task is not finished."""

        if uid not in self._tasks:
            raise UndefinedTaskException

        fut = self._tasks[uid]
        try:
            return await fut
        finally:
            self._tasks.pop(uid)


class ConnectionLock:
    """Lock for sync connections"""

    def __init__(self):
        self._loop = events.get_event_loop()
        self._fut = self._loop.create_future()

    def __await__(self):
        """Async wait"""
        return self._fut.__await__()

    def get_state(self):
        """Returns True if locked, False if unlocked"""
        return self._fut.done()

    def lock(self):
        """Lock connection"""
        if self._fut.done():
            return False
        self._fut.set_result(True)
        return True

    def unlock(self):
        """Unlock connection"""
        if not self._fut.done():
            return False
        self._fut = self._loop.create_future()
        return True

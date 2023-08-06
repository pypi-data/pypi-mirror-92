#  Copyright (c) 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import time

from healthcheck_python.data.base_service import BaseService


class PeriodicService(BaseService):
	"""
	Periodic Service
	This service has to be updated periodically, otherwise it is marked as failed
	"""

	def __init__(self, name, timeout=10):
		super().__init__(name)
		self._timeout = timeout

		self._last_start = None
		self._last_end = None
		self._timeout = None

		self._status = False

	def json(self):
		"""
		Returns all attributes as dict
		:return: dict, all object attributes
		"""
		return {
			'status': self._status,
			'last_start': self._last_start, 'last_end': self._last_end, 'timeout': self._timeout
		}

	def add_new_point(self, point):
		"""
		Add new function call
		:param point: dict, new function call data
		"""
		if point is None:
			return

		self._last_start = point['start_time']
		self._last_end = point['end_time']
		self._timeout = point['timeout']

	def is_healthy(self, current_time=None):
		"""
		Check if last call is within timeout limits
		:param current_time: time.time() object, Optional, check the status with specific time
		:return: boolean, service status
		"""
		if self._last_end is None:
			return False
		if current_time is None:
			current_time = time.time()

		self._status = current_time - self._last_end <= self._timeout
		return self._status

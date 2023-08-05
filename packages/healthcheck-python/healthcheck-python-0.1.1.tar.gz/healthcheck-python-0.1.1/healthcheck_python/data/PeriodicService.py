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

from healthcheck_python.data.BaseService import BaseService


class PeriodicService(BaseService):

	def __init__(self, name, timeout=10):
		super().__init__(name)
		self._timeout = timeout

		self._last_start = None
		self._last_end = None
		self._timeout = None

	def __str__(self):
		return "5"

	def add_new_point(self, point):
		if point is None:
			return

		self._last_start = point['start_time']
		self._last_end = point['end_time']
		self._timeout = point['timeout']

	def is_healthy(self):
		if self._last_end is None:
			return False
		current_time = time.time()

		return current_time - self._last_end <= self._timeout

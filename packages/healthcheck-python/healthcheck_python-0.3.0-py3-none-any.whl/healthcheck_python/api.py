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

from multiprocessing import Process, Queue, cpu_count
from queue import Empty

import bottle

from healthcheck_python.release import __version__


class HealthCheckApi(Process):
	"""
	API responder class
	Creates a bottle instance and reports the health status
	"""

	def __init__(self, host, port, status_queue, daemon=False):
		super().__init__()

		self._host = host
		self._port = port
		self._status_queue = status_queue
		self.daemon = daemon

		self._app = bottle.Bottle()
		self._app.queue = Queue()
		self._app.nb_workers = cpu_count()

		self._app.route('/', method="GET", callback=HealthCheckApi._index)
		self._app.route('/health', method="GET", callback=self._health)

	def __del__(self):
		self.terminate()

	def run(self):
		bottle.run(self._app, host=self._host, port=self._port)

	@staticmethod
	def _index():
		return f"Hello there! I'm py-healthcheck v{__version__}"

	def _health(self):
		"""
		Health check path
		/health
		:return: overall status str(boolean).
		:return: If verbose mode enabled, return a dict with details about every service
		"""
		is_verbose = 'v' in bottle.request.query.keys()
		try:
			status = self._status_queue.get(block=False, timeout=1)
		except Empty:
			status = {'status': False, 'data': {}}

		if is_verbose:
			return status

		return str(status['status']).lower()

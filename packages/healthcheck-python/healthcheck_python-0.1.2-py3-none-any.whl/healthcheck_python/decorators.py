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

import functools
import time

import healthcheck_python


def periodic(_func=None, *, service='unknown', timeout=5):
	"""
	Periodic check decorator
	Add this to your periodically called functions
	:param _func: Wrapped function
	:param service: Service name. This name will be reported with API call
	:param timeout: The timeout in seconds needed between to consecutive _func() calls
	before marking the service down
	:return: original return values of _func()
	"""

	def wrapper(func):
		@functools.wraps(func)
		def wrapper_func(*args, **kwargs):
			start_time = time.time()
			ret_val = func(*args, **kwargs)
			end_time = time.time()
			healthcheck_python.message_queue.put(
				{'name': service, 'start_time': start_time, 'end_time': end_time, 'timeout': timeout}
			)
			return ret_val

		return wrapper_func

	if _func is None:
		return wrapper
	return wrapper(_func)

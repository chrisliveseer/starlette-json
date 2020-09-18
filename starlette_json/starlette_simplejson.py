import typing

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

try:
	from simplejson import loads, dumps
except ImportError:
	loads = dumps = None

async def simplejson_loads(self) -> typing.Any:
	if not hasattr(self, '_json'):
		body = await self.body()
		self._json = loads(body, **self.json_opts)
	return self._json

class SimpleJsonMiddleware(BaseHTTPMiddleware):
	def __init__(self, app, **kwargs):
		self.app = app
		self.json_opts = kwargs
		super(SimpleJsonMiddleware, self).__init__(app)

	async def dispatch(self, request, call_next):
		response = await call_next(request)
		response.json = simplejson_loads
		return response

valid_args = {
	'skipkeys',
	'ensure_ascii',
	'check_circular',
	'allow_nan',
	'cls',
	'indent',
	'separators',
	'encoding',
	'default',
	'use_decimal',
	'namedtuple_as_object',
	'tuple_as_array',
	'bigint_as_string',
	'sort_keys',
	'item_sort_key',
	'for_json',
	'ignore_nan',
	'int_as_string_bitcount',
	'iterable_as_array',
}

class SimpleJsonResponse(Response):
	'''
	See available dumps kwargs here
		https://simplejson.readthedocs.io/en/latest/#simplejson.dump
	'''
	media_type = "application/json"

	def __init__(self, *args, **kwargs):
		self.render_args = {arg: v for arg,v in kwargs.items() if arg in valid_args}
		base_args = {arg: v for arg,v in kwargs.items() if arg not in valid_args}
		super(SimpleJsonResponse, self).__init__(*args, **base_args)

	def render(self, content: typing.Any) -> bytes:
		return dumps(content, **self.render_args).encode('utf-8')
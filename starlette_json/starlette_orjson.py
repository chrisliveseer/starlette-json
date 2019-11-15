import typing
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

try:
	from orjson import loads, dumps
except ImportError:
	loads = dumps = None

async def orjson_loads(self) -> typing.Any:
	if not hasattr(self, '_json'):
		body = await self.body()
		self._json = loads(body)
	return self._json

class ORJsonMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request, call_next):
		response = await call_next(request)
		response.json = orjson_loads
		return response

valid_args = {
	'default', # To serialize a subclass or arbitrary types, specify default as a callable that returns a supported type. default may be a function, lambda, or callable class instance.
	'option', # To specify multiple options, mask them together, e.g., option=orjson.OPT_STRICT_INTEGER | orjson.OPT_NAIVE_UTC
}
class ORJsonResponse(Response):
	'''
	See available dump kwargs here
		https://github.com/ijl/orjson#serialize
	'''
	media_type = "application/json"

	def __init__(self, *args, **kwargs):
		self.render_args = {arg: v for arg,v in kwargs.items() if arg in valid_args}
		base_args = {arg: v for arg,v in kwargs.items() if arg not in valid_args}
		super(ORJsonResponse, self).__init__(*args, **base_args)

	def render(self, content: typing.Any) -> bytes:
		return dumps(content, **self.render_args)

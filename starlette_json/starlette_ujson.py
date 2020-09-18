import typing
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

try:
	from ujson import loads, dumps
except ImportError:
	loads = dumps = None

async def ujson_loads(self) -> typing.Any:
	if not hasattr(self, '_json'):
		body = await self.body()
		self._json = loads(body)
	return self._json

class UJsonMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request, call_next):
		response = await call_next(request)
		response.json = ujson_loads
		return response

valid_args = {
	'encode_html_chars', # Used to enable special encoding of "unsafe" HTML characters into safer Unicode sequences. Default is False
	'ensure_ascii', # Limits output to ASCII and escapes all extended characters above 127. Default is true. If your end format supports UTF-8 setting this option to false is highly recommended to save space
	'escape_forward_slashes', # Controls whether forward slashes (/) are escaped. Default is True
	'indent' # Controls whether indention ("pretty output") is enabled. Default is 0 (disabled)
}

class UJsonResponse(Response):
	'''
	See available render kwargs here
		https://github.com/esnme/ultrajson/blob/master/README.rst
	'''
	media_type = "application/json"

	def __init__(self, *args, **kwargs):
		self.render_args = {arg: v for arg,v in kwargs.items() if arg in valid_args}
		base_args = {arg: v for arg,v in kwargs.items() if arg not in valid_args}
		if 'ensure_ascii' not in self.render_args:
			self.render_args['ensure_ascii'] = False
		super(UJsonResponse, self).__init__(*args, **base_args)

	def render(self, content: typing.Any) -> bytes:
		return dumps(content, **self.render_args).encode('utf-8')
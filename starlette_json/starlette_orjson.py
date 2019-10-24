import typing

from starlette.responses import Response

try:
	from orjson import dumps
except ImportError:
	dumps = None
	
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
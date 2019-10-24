import typing

from starlette.responses import Response

try:
	from rapidjson import dumps
except ImportError:
	dumps = None
	
valid_args = {
	'skipkeys', # (bool) – whether invalid dict keys will be skipped
	'ensure_ascii', # (bool) – whether the output should contain only ASCII characters
	'indent', # (int) – indentation width to produce pretty printed JSON
	'default', # (callable) – a function that gets called for objects that can’t otherwise be serialized
	'sort_keys', # (bool) – whether dictionary keys should be sorted alphabetically
	'number_mode', # (int) – enable particular behaviors in handling numbers
	'datetime_mode', # (int) – how should datetime, time and date instances be handled
	'uuid_mode', # (int) – how should UUID instances be handled
	'allow_nan' # (bool) – compatibility flag equivalent to number_mode=NM_NAN
}
	
class RapidJsonResponse(Response):
	'''
	See available dump kwargs here
		https://python-rapidjson.readthedocs.io/en/latest/dumps.html
	'''
	media_type = "application/json"
	
	def __init__(self, *args, **kwargs):
		self.render_args = {arg: v for arg,v in kwargs.items() if arg in valid_args}
		super(RapidJsonResponse, self).__init__(*args, **kwargs)
		
	def render(self, content: typing.Any) -> bytes:
		return dumps(content, **self.render_args).encode("utf-8")
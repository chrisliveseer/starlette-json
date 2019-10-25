import typing

from starlette.responses import Response

try:
	from simplejson import dumps
except ImportError:
	dumps = None
	
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
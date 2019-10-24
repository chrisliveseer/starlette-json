# Starlette Json

## Introduction
Starlette json responses for various json serializers available in the python community.

### Why:
- Remove `ujson` dependency from core starlette package
- Add adaptors for other serializers
- Customize serializer rendering settings

## Requirements
- Python 3.6+
- [Starlette](https://github.com/encode/starlette)

## Installation
```console
$ pip install starlette-json
```

## Optional installs
Install at least one of these:
- [orjson](https://github.com/ijl/orjson) `pip install orjson`
- [Ultrajson](https://github.com/esnme/ultrajson) `pip install ujson`
- [Rapidjson](https://github.com/python-rapidjson/python-rapidjson) `pip install python-rapidjson`
- [SimpleJson](https://github.com/simplejson/simplejson) `pip install simplejson`
	
## Usage
### Basic
```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse

from starlette_json import ORJsonResponse, UJsonResponse, RapidJsonResponse, SimpleJsonResponse

app = Starlette()
data = {'Hello': 'World'}

@app.route('/json')
def json():
	return JSONResponse(data)
	
@app.route('/orjson')
def orjson():
	return ORJsonResponse(data)
	
@app.route('/ujson')
def ujson():
	return UJsonResponse(data)
	
@app.route('/rapidjson')
def rapidjson():
	return RapidJsonResponse(data)
	
@app.route('/simplejson')
def rapidjson():
	return SimpleJsonResponse(data)
```

### Custom rendering options:
See the docs for the specific json serializer for available options

```python
from starlette.applications import Starlette
from starlette_json import ORJsonResponse, UJsonResponse, RapidJsonResponse
import orjson

app = Starlette()
data = {'Hello': 'World'}

@app.route('/orjson')
def orjson():
	return ORJsonResponse(
		data, 
		default=lambda x: str(x), 
		option=orjson.OPT_STRICT_INTEGER | orjson.OPT_NAIVE_UTC
	)
	
@app.route('/ujson')
def ujson():
	return UJsonResponse(
		data, 
		encode_html_chars=True, 
		ensure_ascii=False, 
		escape_forward_slashes=False
	)
	
@app.route('/rapidjson')
def rapidjson():
	return RapidJsonResponse(data, sort_keys=True, indent=4)
	
@app.route('/simplejson')
def rapidjson():
	return SimpleJsonResponse(
		data,
		skipkeys=False,
		ensure_ascii=True,
		check_circular=True,
		allow_nan=True
	)
```

## Contributing
PRs very welcome.
[CONTRIBUTING.md](CONTRIBUTING.md)

### Todo
- Tests?
- Figure out how to integrate custom json parser for `starlette.request`
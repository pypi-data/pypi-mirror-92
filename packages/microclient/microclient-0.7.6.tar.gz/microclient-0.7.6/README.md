# Microclient
Microclient is a library for building simple python clients for your REST APIs.

Basic usage:
```python
from microclient import BaseClient, EndpointInfo

class ZOOClient(BaseClient):
    service_name = 'ZOO API'
    endpoints = [
        EndpointInfo("animals", [
            EndpointInfo("cats", "GET"),
            EndpointInfo("dogs", "GET"),
            EndpointInfo("elephants", "GET"),
        ]),
        EndpointInfo("zoo-status", "GET"),
        EndpointInfo("tickets", "GET, POST, DELETE")
    ]
```

Which translates into client like this:
```python
zoo_client = ZooClient('http://localhost:8000')
zoo_client.animals.cats() # sends GET request to http://localhost:8000/animals/cats
zoo_client.tickets.post(data={'amount': 2})  # sends POST request to http://localhost:8000/tickets with json data
```

For now, authorization can be done via Auth Token on client initialization:
```python
zoo_client = ZooClient('http://localhost:8000', auth='some_token')
```
And the token will be appended to every request header. By default the Authorization header prefix is `Token` but it can be set like this:
```python
zoo_client = ZooClient('http://localhost:8000', auth='some_token', auth_prefix="Bearer")
```
Which will send header like this:
`"Authorization": "Bearer some_token"`

## Responses
Every endpoint called on a microclient will return `LazyResponse` object, which is - as the name suggests - lazy loaded. `Lazy Response` has three main properties that are most important:
`data` (preferably JSON response data, but will fallback to byte-string content on decode failure), `status` (integer status code) and `headers` (response headers).


Currently microclient is working with json data only (requests and responses).

## Testing
If you want to unit test the client without actually calling the underlying API, use `LazyResponse` properties to check for proper endpoint, method and data sent.
Example:
```python
zoo_client = ZooClient('http://localhost:8000')
response = zoo_client.animals.cats()
print(response.url, response.method, response.request_data)
# http://localhost:8000/animals/cats, GET, None 
response = zoo_client.tickets.post(data={'amount': 2})
print(response.url, response.method, response.request_data)
# http://localhost:8000/tickets, POST, {'amount': 2}
``` 
#### DECPRECATION NOTICE:
In previous versions of microclient, you can also test the same things using `debug` to switch between actually calling and testing your client.
Example:

```python
zoo_client = ZooClient('http://localhost:8000')
zoo_client.debug = True
print(zoo_client.animals.cats())
# (http://localhost:8000/animals/cats, GET, None) 
print(zoo_client.tickets.post(data={'amount': 2}))
# (http://localhost:8000/tickets, POST, {'amount': 2})
``` 
However, `debug` property will not be available starting with version 1.0 (in a few months probably) and it's recommended to switch to `LazyResponse` approach.

## Headers
Headers can be appended on 4 levels:
 - global - will be appended for evey request this client makes:
```python
class ZOOClient(BaseClient):
    service_name = 'ZOO API'
    global_headers = {"Content-Type": "application/*"}
    endpoints = [
        EndpointInfo("animals", "GET")
    ]
```
 - on a group of endpoints:
```python
class ZOOClient(BaseClient):
    service_name = 'ZOO API'
    endpoints = [
        EndpointInfo("animals", [
            EndpointInfo("cats", "GET"),
            EndpointInfo("dogs", "GET"),
            EndpointInfo("elephants", "GET"),
        ], headers={"Content-Type": "application/*"}),  
# Every endpoint inside 'animals' will append these headers ('animals' itself included)
]
```
 - on a single endpoint:
```python
class ZOOClient(BaseClient):
    service_name = 'ZOO API'
    endpoints = [
        EndpointInfo("animals", [
            EndpointInfo("cats", "GET", headers={"Content-Type": "application/*"}),
            EndpointInfo("dogs", "GET"),
            EndpointInfo("elephants", "GET"),
        ]),  
]
```
 - on a single request:
```python
zoo_client = ZooClient('http://localhost:8000')
response = zoo_client.animals.cats(headers={"Content-Type": "application/*"})
```

# Handling response data
Microclient relies on 'Content-Type' headers sent with response when parsing response data. If there is no such header in response, it will fall back to raw content (in most cases that means `bytes` object).
No MIME sniffing is done whatsoever. Currently, some basic content-types are handled, but feel free to address more of them.

# Logging
Microclient by default logs every request sent by every client to stdout using `loguru` library (check it out here it's awesome - https://loguru.readthedocs.io/en/stable/index.html). If you don't need those logs at all you can turn them off by calling `disable` method on loguru logger like this:
```python
from loguru import logger
logger.disable('microclient')
``` 
Now, loguru will not propagate the logs from microclient library at all.
If you configure loguru to handle log levels differently and `microclient` is not disabled from logging, it will follow your settings no problem, since it uses same interface as your program - `loguru` logger.

# ChangeLog

## v0.7.6
 - added support for more content-types. Microclient relies on 'Content-Type' headers of response when handling response data parsing
 and does not perform MIME sniffing.

## v0.7.5:
 - Microclient now recognizes the response by headers, so if its not declared as JSON it will return raw bytes content.
 In future other content types will be supported.

## v0.7.4:
 - Logging truncates long strings (except url) so it doesnt flood the console.

## v0.7.3:
 - Fixed formatting query params when provided with only null-like values. Example:
 `{"param1": None, "param2": ''}) -> ''`. Previously was `{"param1": None, "param2": ''}) -> '?'`
## v0.7:
 - Added headers support for single request, single endpoint, inner endpoint (group of endpoints) and global for client.
 - Added timing diagnostic for every request (available at `request_time` attribute in `LazyResponse`)
 - Fixed a bug where your IDE could point that `resource_id` parameter must be a `str`.

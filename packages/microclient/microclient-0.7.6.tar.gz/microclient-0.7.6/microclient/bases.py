import re
from dataclasses import dataclass, field
from functools import partial, wraps
from typing import List, Callable, Any

import requests
from loguru import logger

from .response import LazyResponse
from .utils import dict_to_query_params


class InvalidMethodException(Exception):
    """
    Thrown when trying to use nonexistent HTTP method.
    """
    pass


class NoBaseUrlException(Exception):
    """
    Throw when extending EcmClient base and not providing a `base_url` class variable.
    """
    pass


class MultipleMethodsAvailable(Exception):
    """
    Thrown when Endpoint object is called and has more then one available methods to call.
    Example:
        Endpoint supports POST and GET and we called it as `endpoint()` but we should call it like
        `endpoint.post()` or `endpoint.get()`.
    """
    pass


def http_method_call(method):
    """
    Decorator for calling a http method. Used by Endpoint class.
    Main use is to log every activity before calling.
    :param method: Name of the HTTP method.
    :return: Wrapped function
    """

    def deco(func):
        @wraps(func)
        def wrapper(self, resource_id=None, data=None, debug=False, headers=None, **q_params):
            url = self._get_url(resource_id, **q_params)
            if method not in self.available_methods:
                logger.error(f"Endpoint {url} failed. HTTP method {method} not available.")
                raise InvalidMethodException(f'{method} is not supported by this endpoint.')
            if debug or self.debug:
                return url, method, data
            headers = self._get_request_headers(headers)
            method_call = partial(func, self=self, resource_id=resource_id, data=data, headers=headers, **q_params)
            return LazyResponse(method_call, url, method, data, headers)

        return wrapper

    return deco


class ClientChild:
    """
    Small mixin class for creating an API client child that reads base_url and debug values
    directly from parent (so its dynamic - when parent changes debug/base_urls, all children also change debugs/base_urls)
    """

    def __init__(self, parent, inner_url):
        self.parent = parent
        self.inner_base_url = inner_url

    @property
    def debug(self):
        return self.parent.debug

    @property
    def base_url(self):
        return f"{self.parent.base_url}{f'/{self.inner_base_url}' if self.inner_base_url else ''}"

    @property
    def verify_ssl(self):
        return self.parent.verify_ssl

    @property
    def auth(self):
        return self.parent.auth

    @property
    def auth_prefix(self):
        return self.parent.auth_prefix

    @property
    def parent_headers(self):
        return self.parent.global_headers


class Endpoint(ClientChild):
    """
    Representation of an REST API Endpoint
    """

    def __init__(self, parent, name: str, available_methods: list, headers: dict = None):
        super().__init__(parent, name)
        self.name = name
        self.available_methods = [method.upper().strip() for method in available_methods]
        self.METHOD_SWITCH = {
            'GET': self.get,
            'POST': self.post,
            'PATCH': self.patch,
            'DELETE': self.delete,
            'PUT': self.put
        }
        self.endpoint_headers = headers or {}

    def __call__(self, resource_id=None, data=None, debug=False, headers: dict = None, **q_params):
        """
        When Endpoint is supporting only one HTTP method, it can be called directly like:
            client.endpoint()
        instead of for example:
            client.endpoint.get()
        :param data: Json data for the endpoint.
        :param q_params: Optional query string parameters.
        :return: Json data returned by the endpoint.
        """
        if len(self.available_methods) != 1:
            raise MultipleMethodsAvailable(f"There are multiple methods available on this Endpoint (`{self.name}`). Please use one of the helper methods (post(), get(), etc.)")
        else:
            f = self.METHOD_SWITCH[self.available_methods[0]]
            return f(resource_id=resource_id, data=data, debug=debug, headers=headers, **q_params)

    def _get_url(self, resource_id=None, **q_params):
        """
        Based on the parameters provided creates an endpoint URL dynamically.
        Parses optional q_params dictionary into query string, also appends an
        identifier when provided, for example:
            client.endpoint.get('some-id', search='phrase', limit=5)
        translates to URL:
            `/endpoint/some-id?search=phrase&limit=5`
        :param resource_id: Optional identifier for this endpoint.
        :param q_params: Optional query parameters.
        :return: A prepared URL.
        """
        return f"{self.base_url}{f'/{resource_id}' if resource_id else ''}{dict_to_query_params(q_params)}"

    def _get_request_headers(self, request_headers: dict = None):
        if request_headers is None:
            request_headers = {}
        request_headers.update(self.parent_headers)
        request_headers.update(self.endpoint_headers)
        if self.auth:
            request_headers.update({"Authorization": f"{self.auth_prefix} {self.auth}"})
        return request_headers

    @http_method_call('GET')
    def get(self, resource_id=None, data=None, debug=False, headers: dict = None, **q_params):
        return requests.get(self._get_url(resource_id, **q_params), verify=self.verify_ssl, headers=headers)

    @http_method_call('POST')
    def post(self, resource_id=None, data=None, debug=False, headers: dict = None, **q_params):
        return requests.post(self._get_url(resource_id, **q_params), json=data, verify=self.verify_ssl, headers=headers)

    @http_method_call('PUT')
    def put(self, resource_id=None, data=None, debug=False, headers: dict = None, **q_params):
        return requests.put(self._get_url(resource_id, **q_params), json=data, verify=self.verify_ssl, headers=headers)

    @http_method_call('PATCH')
    def patch(self, resource_id=None, data=None, debug=False, headers: dict = None, **q_params):
        return requests.patch(self._get_url(resource_id, **q_params), json=data, verify=self.verify_ssl, headers=headers)

    @http_method_call('DELETE')
    def delete(self, resource_id=None, data=None, debug=False, headers: dict = None, **q_params):
        return requests.delete(self._get_url(resource_id, **q_params), verify=self.verify_ssl, headers=headers)

    def __repr__(self):
        return f"{self.base_url} - {self.available_methods}"


@dataclass
class EndpointInfo:
    name: str
    info: str or list
    headers: dict = field(default_factory=dict)

    def __iter__(self):
        return iter((self.name, self.info, self.headers))


class EndpointSchema:
    """
     A mixin that enables to build a schema of endpoints exposed by the API from the `endpoints` tuple tree-like structure.
     When provided with `endpoints`, automatically creates all methods for the API Client object. The rules of defining the schema are as follows.
     Whole `endpoints` variable is a list of tuples with two values - first is the endpoint name (IMPORTANT: without any  trailing/leading slashes)
     and the second is either a HTTP method name or another list of `endpoints` (same format as root `endpoints`).
     Example:
     class APIClass(EndpointSchema):
          base_url = "http://localhost:1234"
          endpoints = [
             ("dictionaries", [
                 ("authors", "GET"),
                 ("affiliations", "GET"),
                 ("keywords", "GET"),
                 ("tags", "GET"),
                 ("namedEntities", "GET"),
             ]),
             ("healthCheck", "GET"),
             ("documents", [
                ("", "POST, GET"),
                ("work-files", "GET")
             ])
         ]

      Creates a class that can be used like this:
       api_client = APIClass()
       api_client.healthCheck()  <- we defined healthCheck as a single HTTP method endpoint.
       api_client.dictionaries.authors()  <- we defined dictionaries as a 'nested' endpoint, so we can access the inner endpoints be referencing 'dictionaries' attribute.
       api_client.dictionaries.affiliations()
       api_client.dictionaries.tags()
       api_client.documents.post({"some": "data"}) <- we declared that documents endpoint supports two methods - POST and GET so we need to tell the client which one we are using.
       api_client.documents.get("some_id") <- same with GET
       api_client.documents.work_files() <- additionally, we can call a more specific action on the documents endpoint
    """
    endpoints: List[Endpoint] = []

    # Simple dictionary to map a HTTP method string to a actual requests method.
    HTTP_METHODS = {
        'GET',
        'POST',
        'PATCH',
        'DELETE',
        'PUT',
    }

    def __init__(self):
        self._endpoint = None
        self._dynamic_endpoint = None
        for endpoint in self.endpoints:
            self._create_endpoint(endpoint)

    def _create_endpoint(self, endpoint: EndpointInfo):
        """
        Main entry for creating automatic endpoint-to-object-method mapping.
        Parses an Endpoint tuple and created an appropriate attribute:
        If the endpoint info is a string, that means its just a single method endpoint, so it creates
        an attribute as a function using `self._create_http_attribute()`,
        If the endpoint info is a list that means there are another endpoints nested inside it, so it creates
        an InnerEndpoint object as attribute with this name.

        :param endpoint: Endpoint tuple
        """
        name, info, optional_headers = endpoint
        if name == '':
            self._endpoint = Endpoint(self, '', self._parse_and_sanitize_https_methods(info), headers=optional_headers)
        if EndpointSchema.is_dynamic_endpoint(name):
            self._dynamic_endpoint = DynamicInnerEndpoint(self, info, optional_headers)
        attribute_name = EndpointSchema.sanitize_attribute_name(name)
        if isinstance(info, str):
            setattr(self, attribute_name, self._create_http_attribute(info, name, optional_headers))
        elif isinstance(info, list):
            setattr(self, attribute_name, InnerEndpoint(self, name, info, optional_headers))

    def _parse_and_sanitize_https_methods(self, methods: str):
        methods = methods.split(',')
        methods_sanitized = []
        for method in methods:
            method = method.strip().upper()
            try:
                assert method in self.HTTP_METHODS
            except AssertionError:
                logger.warning(f"{method} is not a valid HTTP method.")
                raise InvalidMethodException(f"{method} is not a valid HTTP method.")
            methods_sanitized.append(method)
        return methods_sanitized

    def _create_http_attribute(self, methods: str, endpoint: str, headers: dict = None) -> Callable:
        """
        Returns a function calling an endpoint in the API defined under `self.base_url`.
        :param methods: HTTP methods to be used
        :param endpoint: API Endpoint name
        :return: Prepared function
        """
        methods_sanitized = self._parse_and_sanitize_https_methods(methods)
        return Endpoint(self, endpoint, methods_sanitized, headers=headers)

    def __call__(self, resource_id=None, data=None, debug=False, headers: dict = None, **q_params):
        if self._endpoint:
            return self._endpoint(resource_id, data, debug, headers, **q_params)
        else:
            raise InvalidMethodException("This client is not callable.")

    def __getattr__(self, item):
        if not self._endpoint:
            raise AttributeError(f"{item} is not available on {self}")
        return getattr(self._endpoint, item)

    def __getitem__(self, item):
        if not self._dynamic_endpoint:
            raise AttributeError(f"{item} is not available on {self}")
        return self._dynamic_endpoint[item]

    @staticmethod
    def sanitize_attribute_name(endpoint_name: str):
        temp = endpoint_name.split('-')
        endpoint_name = '_'.join(temp)
        return endpoint_name.strip('/')

    @staticmethod
    def is_dynamic_endpoint(route_name: str):
        route_name = route_name.strip('/')
        match = re.search(r'{.*}', route_name)
        return match is not None


class BaseClient(EndpointSchema):
    """
    Version 1

    Base class for creating an object representing an REST API and exposing endpoints as instance methods.
    For example if we have an API named 'Foo' with endpoint '/get-bar' that can be reached by a GET method we have a object
    with like:
        foo = Foo()
        foo.get_bar()
    where of course `get_bar()` is making a GET request to the '/get-bar' endpoint.
    """

    # Name of the ECM service - for verbosity only.
    service_name: str

    # Should this client verify SSL certificate on secure connections (defaults to true)
    # It will be passed down to requests API, so it can also be a path to valid certificate.
    # See: https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification
    verify_ssl = True

    # Headers dictionary to append to every request
    global_headers = {}

    def __init__(self, base_url=None, auth=None, auth_prefix='Token'):
        """
        Raises exception if no base url is defined in class.
        Also creates methods automatically if endpoints are provided.
        :param base_url: Base URL of the implemented API - with protocol, host and port if needed.
        :param auth: Auth token to be passed in Authorization header
        :param auth_prefix: Token prefix in the Authorization header, defaults to 'Token'
        """
        self.base_url = base_url if base_url else self.base_url
        self._debug = False
        self.auth = auth
        self.auth_prefix = auth_prefix
        if self.verify_ssl is False:
            logger.warning("Verify SSL flag was set to False, all connections will not be secure, proceed with caution.")
        if not self.base_url:
            raise NoBaseUrlException(f"No base URL was set for {self}")
        super().__init__()

    @property
    def debug(self):
        """
        The debug property is to allow basically testing the API client. If set to True,
        all the endpoints calls are not executed - instead, each method call returns the full endpoint that it was about to call,
        the HTTP method that it wanted to use, and optional request body.
        :return: Is debug enabled
        """
        return self._debug

    @debug.setter
    def debug(self, value):
        logger.warning("DEPRECATION WARNING: Debug property will not be available in the version 1.0 of microclient. Use LazyResponses attributes instead. More info on: https://pypi.org/project/microclient/")
        self._debug = value

    def _perform_request(self, http_method: str, endpoint: str, resource_id: Any = None, debug=False, headers: dict = None, json_data: dict = None, **query_params):
        """
        A function that is basically a wrapper for other methods - it should be used
        when there is a very specific way of calling an endpoint.

        :param http_method: HTTP method
        :param endpoint: endpoint name
        :param json_data: data to be sent to the endpoint
        :param query_params: optional query params appended to the URL
        :param resource_id: optional id to append to the end of the endpoint. Can be anything with __str__ implemented..
        :return: JSON data returned by the API
        """
        f = self._create_http_attribute(http_method, endpoint)
        return f(resource_id, json_data, debug=self.debug or debug, headers=headers, **query_params)

    def __str__(self):
        return f"{self.service_name} client - {self.base_url}"

    def __repr__(self):
        return str(self)


class InnerEndpoint(EndpointSchema, ClientChild):
    def __init__(self, parent: BaseClient, inner_base_url, endpoints=None, headers=None):
        if endpoints is not None:
            self.endpoints = endpoints
        headers = headers or {}
        self.global_headers = {**parent.global_headers, **headers}
        ClientChild.__init__(self, parent, inner_base_url)
        EndpointSchema.__init__(self)

    def _perform_request(self, http_method: str, endpoint: str, resource_id: Any = None, debug=False, headers: dict = None, json_data: dict = None, **query_params):
        """
        To ensure that InnerEndpoint can use perform_request (lets say its backward compatibility)
        we define this function as a call to parents perform_request.
        :param http_method: HTTP method
        :param endpoint: endpoint name
        :param json_data: data to be sent to the endpoint
        :param query_params: optional query params appended to the URL
        :param resource_id: optional id to append to the end of the endpoint. Can be anything with __str__ implemented.
        :return: JSON data returned by the API
        """
        endpoint = f'{self.inner_base_url}/{endpoint}'
        return self.parent._perform_request(http_method, endpoint, resource_id, debug, json_data, headers=headers, **query_params)


class DynamicInnerEndpoint(InnerEndpoint):

    def __init__(self, parent, endpoints, headers=None):
        super(DynamicInnerEndpoint, self).__init__(parent, '', endpoints, headers)

    def __getitem__(self, item):
        self.inner_base_url = item
        return self

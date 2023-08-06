import time
from json import JSONDecodeError
from typing import Callable
from loguru import logger

import requests

from microclient.utils import truncate_if_necessary

REPR_LIMIT = 50

CONTENT_DISPATCH = {
    'application/json': 'json',
    'application/vnd.api+json': 'json',
    'text/plain': 'text',
    'text/html': 'text',
    'application/octet-stream': 'bin'
}


def get_mimetype(content_type: str):
    mimetype, *_ = content_type.split(';')
    return mimetype


def match_content_type(incoming_content_type):
    if not incoming_content_type:
        return
    mimetype = get_mimetype(incoming_content_type)
    return CONTENT_DISPATCH.get(mimetype)


class LazyResponse:

    def __init__(self, method_call: Callable[..., requests.Response], url: str, method: str, data=None, headers=None):
        self._response: requests.Response = None
        self._response_loaded = False
        self._get_response = method_call
        self.url = url
        self.method = method
        self.request_data = data
        self.response_time = None
        self.request_headers = headers

    def _truncate_long_strings(self):
        method = truncate_if_necessary(self.method, REPR_LIMIT)
        request_data = truncate_if_necessary(self.request_data, REPR_LIMIT)
        request_headers = truncate_if_necessary(self.request_headers, REPR_LIMIT)
        return method, request_data, request_headers

    def _load_response(self):
        if not self._response_loaded:
            method, request_data, request_headers = self._truncate_long_strings()
            logger.info(f"REQUEST: {self.url} | method: {method} | data: {request_data} | headers: {request_headers}")
            start = time.time()
            self._response = self._get_response()
            self.response_time = time.time() - start
            self._response_loaded = True
            logger.info(f"RESPONSE: {self.url} | {self.status} | {self.response_time:.4f} seconds")

    @property
    def data(self):
        self._load_response()
        content_type = self._response.headers.get('Content-Type')
        matched_type = match_content_type(content_type)
        if matched_type == 'json':
            try:
                response_data = self._response.json()
            except JSONDecodeError:
                logger.warning(f"{self.url} did not respond with valid JSON, falling back to raw content.")
                response_data = self._response.content
        elif matched_type == 'text':
            response_data = self._response.content.decode(self._response.encoding)
        elif matched_type == 'bin':
            # This is when we are convinced that the response holds bytes data
            response_data = bytes(self._response.content)
        else:
            # This is when we are don't know whats inside response, so we are falling back to raw content.
            logger.warning(f"Cannot determine response content-type from {self.url} falling back to raw content")
            response_data = self._response.content
        return response_data

    @property
    def status(self) -> int:
        self._load_response()
        return self._response.status_code

    @property
    def headers(self) -> dict:
        self._load_response()
        return self._response.headers

    def __repr__(self):
        method, request_data, _ = self._truncate_long_strings()
        return f"LazyResponse(request_data={request_data}, url={self.url}, method={method})"

    def __str__(self):
        return str(self.data)

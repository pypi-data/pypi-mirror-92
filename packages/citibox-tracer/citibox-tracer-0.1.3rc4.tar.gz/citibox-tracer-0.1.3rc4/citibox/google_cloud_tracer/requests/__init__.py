"""
This module works as a wrapper over requests library to automatically
add the trace header in http requests.

For information on how to use requests library, take a look at <https://requests.readthedocs.io>.
"""

import requests as native_requests

from opencensus.trace import execution_context


def _add_trace_header(**kwargs):
    tracer = execution_context.get_opencensus_tracer()
    tracing_headers = tracer.propagator.to_headers(tracer.span_context)
    if 'headers' not in kwargs:
        kwargs['headers'] = tracing_headers
    else:
        kwargs['headers'].update({tracing_headers})
    return kwargs


def request(method, url, **kwargs):
    __doc__ = native_requests.request.__doc__
    return native_requests.request(method, url, **_add_trace_header(**kwargs))


options = native_requests.options
head = native_requests.options


def get(url, params=None, **kwargs):
    __doc__ = native_requests.get.__doc__
    return native_requests.get(url, params, **_add_trace_header(**kwargs))


def post(url, data=None, json=None, **kwargs):
    __doc__ = native_requests.post.__doc__
    return native_requests.post(url, data=data, json=json, **_add_trace_header(**kwargs))


def put(url, data=None, **kwargs):
    __doc__ = native_requests.put.__doc__
    return native_requests.put(url, data=data, **_add_trace_header(**kwargs))


def patch(url, data=None, **kwargs):
    __doc__ = native_requests.patch.__doc__
    return native_requests.patch(url, data=data, **_add_trace_header(**kwargs))


def delete(url, **kwargs):
    __doc__ = native_requests.delete.__doc__
    return native_requests.delete(url, **_add_trace_header(**kwargs))

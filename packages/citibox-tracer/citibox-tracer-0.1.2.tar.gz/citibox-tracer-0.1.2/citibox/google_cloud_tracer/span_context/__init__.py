import abc
from enum import Enum

import logging

logger = logging.getLogger(__name__)


class SpanContextBuilder(abc.ABC):
    SPAN_PREFIX = "DEFAULT"
    DEFAULT_GOOGLE_TRACE_HEADER_NAME = 'X-Cloud-Trace-Context'

    def __init__(self, propagator, trace_header_key):
        self._propagator = propagator
        self._trace_header_key = trace_header_key if trace_header_key else self.DEFAULT_GOOGLE_TRACE_HEADER_NAME

    @abc.abstractmethod
    def build_span_context(self, headers: dict, body: dict = None, **kwargs):
        pass


class PubSubSpanContextBuilder(SpanContextBuilder):
    SPAN_PREFIX = "PUBSUB"

    def build_span_context(self, headers: dict, body: dict = None, **kwargs):
        header = None
        try:
            header = body['message']['attributes'][self._trace_header_key]
        except (KeyError, TypeError):
            header = None
        finally:
            return self._propagator.from_header(header)


class HttpSpanContextBuilder(SpanContextBuilder):
    SPAN_PREFIX = "HTTP"

    def build_span_context(self, headers: dict, body: str = None, **kwargs):
        span_context = None
        for key, header in headers.items():
            if key.upper() == self._trace_header_key.upper():
                span_context = self._propagator.from_header(header)

        if not span_context:
            span_context = self._propagator.from_headers(headers)

        return span_context


class SpanContextFactory:
    class UserAgents(Enum):
        PUBSUB_USER_AGENT = "CloudPubSub-Google"

    def __init__(self, propagator=None, trace_header_key=None):
        self.propagator = propagator
        self.trace_header_key = trace_header_key

    def get_span_context_builder(self, user_agent: str = None) -> SpanContextBuilder:
        if user_agent == self.UserAgents.PUBSUB_USER_AGENT.value or user_agent == "Java/13.0.2":
            logger.debug('Getting PUBSUB trace context builder')
            return PubSubSpanContextBuilder(self.propagator, self.trace_header_key)

        else:
            logger.debug('Getting HTTP trace context builder')
            return HttpSpanContextBuilder(self.propagator, self.trace_header_key)


__all__ = ["SpanContextFactory"]

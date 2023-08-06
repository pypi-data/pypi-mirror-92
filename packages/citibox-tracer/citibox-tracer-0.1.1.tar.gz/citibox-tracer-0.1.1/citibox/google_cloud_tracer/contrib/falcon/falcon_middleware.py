from typing import List
import logging

from falcon import Request, Response

from opencensus.trace import utils
from opencensus.trace.base_exporter import Exporter
from opencensus.trace.propagation import trace_context_http_header_format
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
from opencensus.trace import tracer as tracer_module
from opencensus.trace import span as span_module
from opencensus.trace import (
    attributes_helper,
    execution_context,
    print_exporter,
    samplers,
)
from opencensus.trace.propagation.google_cloud_format import GoogleCloudFormatPropagator

from citibox.google_cloud_tracer import SpanContextFactory

HTTP_HOST = attributes_helper.COMMON_ATTRIBUTES['HTTP_HOST']
HTTP_METHOD = attributes_helper.COMMON_ATTRIBUTES['HTTP_METHOD']
HTTP_PATH = attributes_helper.COMMON_ATTRIBUTES['HTTP_PATH']
HTTP_ROUTE = attributes_helper.COMMON_ATTRIBUTES['HTTP_ROUTE']
HTTP_URL = attributes_helper.COMMON_ATTRIBUTES['HTTP_URL']
HTTP_STATUS_CODE = attributes_helper.COMMON_ATTRIBUTES['HTTP_STATUS_CODE']

logger = logging.getLogger(__name__)


class FalconMiddleware:

    """
    :type excluded_paths: list
    :param excluded_paths: Paths that do not trace.
    :type sampler: :class:`~opencensus.trace.samplers.base.Sampler`
    :param sampler: A sampler. It should extend from the base
                    :class:`.Sampler` type and implement
                    :meth:`.Sampler.should_sample`. Defaults to
                    :class:`.ProbabilitySampler`. Other options include
                    :class:`.AlwaysOnSampler` and :class:`.AlwaysOffSampler`.
    :type exporter: :class:`~opencensus.trace.base_exporter.exporter`
    :param exporter: An exporter. Default to
                     :class:`.PrintExporter`. The rest options are
                     :class:`.FileExporter`, :class:`.LoggingExporter` and
                     trace exporter extensions.
    :type propagator: :class: 'object'
    :param propagator: A propagator. Default to
                       :class:`.TraceContextPropagator`. The rest options
                       are :class:`.BinaryFormatPropagator`,
                       :class:`.GoogleCloudFormatPropagator` and
                       :class:`.TextFormatPropagator`.
    """
    def __init__(self, excluded_paths: List[str] = None, sampler: samplers.Sampler = None, exporter: Exporter = None,
                 propagator=None):
        self._excluded_paths = excluded_paths or []
        self._sampler = sampler or samplers.ProbabilitySampler()
        self._exporter = exporter or print_exporter.PrintExporter()
        self._propagator = propagator or trace_context_http_header_format.TraceContextPropagator()

        self._span_context_factory = SpanContextFactory(self._propagator)

        self._excluded_hosts = [
            "localhost",
            "127.0.0.1"
        ]

    def process_request(self, req: Request, resp: Response):
        if utils.disable_tracing_url(req.path, self._excluded_paths):
            return

        try:
            span_context_builder = self._span_context_factory.get_span_context_builder(req.user_agent)
            span_context = span_context_builder.build_span_context(headers=req.headers, body=req.media)
            tracer = tracer_module.Tracer(
                span_context=span_context,
                sampler=self._sampler,
                exporter=self._exporter,
                propagator=self._propagator
            )
            span = tracer.start_span()
            span.span_kind = span_module.SpanKind.SERVER
            span.name = f'[{span_context_builder.SPAN_PREFIX} - {req.method}] {req.path}'

            tracer.add_attribute_to_current_span(HTTP_HOST, req.host)
            tracer.add_attribute_to_current_span(HTTP_METHOD, req.method)
            tracer.add_attribute_to_current_span(HTTP_PATH, req.path)
            tracer.add_attribute_to_current_span(HTTP_URL, req.uri)
            execution_context.set_opencensus_attr('exclude_hostnames', self._excluded_hosts)

            tracer.current_span()

            req.context.trace_headers = self._propagator.to_headers(span_context)
        except Exception:
            logger.error(f'Failed to trace request', exc_info=True)

    def process_resource(self, req: Request, resp: Response, resource, params: dict):
        if utils.disable_tracing_url(req.path, self._excluded_paths):
            return
        try:
            tracer = execution_context.get_opencensus_tracer()
            tracer.add_attribute_to_current_span(HTTP_ROUTE, resource.__class__.__name__)
        except Exception:
            logger.error(f'Failed to trace resource', exc_info=True)

    def process_response(self, req: Request, resp: Response, resource, req_succeeded: bool):
        if utils.disable_tracing_url(req.path, self._excluded_paths):
            return

        try:
            tracer = execution_context.get_opencensus_tracer()
            tracer.add_attribute_to_current_span(HTTP_STATUS_CODE, int(resp.status[:3]))

            tracer.end_span()
            tracer.finish()
        except Exception:
            logger.error(f'Failed to trace response', exc_info=True)


class GoogleCloudFalconMiddleware(FalconMiddleware):
    """

        :param string project_id: Google cloud project ID
        :param list excluded_paths: List of excluded paths to NOT trace
        :param <opencensus.trace.samplers.Sampler> sampler: Sampler to use, defaults to <samplers.AlwaysOnSampler>
    """
    def __init__(self, project_id, excluded_paths: List[str] = None, sampler: samplers.Sampler = None):
        super().__init__(
            excluded_paths=excluded_paths,
            sampler=sampler,
            exporter=stackdriver_exporter.StackdriverExporter(project_id=project_id),
            propagator=GoogleCloudFormatPropagator()
        )

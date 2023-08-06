import os

from opencensus.ext.stackdriver.trace_exporter import StackdriverExporter
from opencensus.trace.propagation.google_cloud_format import GoogleCloudFormatPropagator
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.span import SpanKind
from opencensus.trace.tracer import Tracer


class FakeTracer(Tracer):
    def finish(self):
        return

    def span(self, name='span'):
        return

    def start_span(self, name='span'):
        return

    def end_span(self):
        return

    def add_attribute_to_current_span(self, attribute_key, attribute_value):
        return


def start_gcp_trace(trace_id=None, project_id="", span_name="GCP") -> Tracer:
    if disable_tracer_environment():
        return FakeTracer()

    propagator = GoogleCloudFormatPropagator()
    span_context = propagator.from_header(trace_id)
    tracer = Tracer(
        span_context=span_context,
        sampler=AlwaysOnSampler(),
        exporter=StackdriverExporter(project_id=project_id),
        propagator=propagator
    )
    span = tracer.start_span(span_name)
    span.span_kind = SpanKind.SERVER

    tracer.current_span()
    return tracer


def disable_tracer_environment():
    return not (os.environ.get('TRACER') or os.environ.get('tracer'))

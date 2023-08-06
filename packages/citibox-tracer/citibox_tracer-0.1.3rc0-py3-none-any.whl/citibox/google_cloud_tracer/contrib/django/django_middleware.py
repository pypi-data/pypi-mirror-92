from typing import List

import django
import six
from django.db import connection
from opencensus.ext.django.middleware import (
    OpencensusMiddleware,
    _trace_db_call,
    EXCLUDELIST_PATHS,
    EXCLUDELIST_HOSTNAMES,

)
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
from opencensus.trace.propagation.google_cloud_format import GoogleCloudFormatPropagator
from opencensus.common import configuration
from opencensus.trace import samplers
from opencensus.trace.propagation import trace_context_http_header_format
from citibox.google_cloud_tracer.tracer import disable_tracer_environment


class GoogleCloudFalconMiddleware(OpencensusMiddleware):

    def __init__(self, get_response=None):
        self.get_response = get_response
        settings = getattr(django.conf.settings, 'TRACING', {})

        self.sampler = (settings.get('SAMPLER', None)
                        or samplers.AlwaysOffSampler())
        if isinstance(self.sampler, six.string_types):
            self.sampler = configuration.load(self.sampler)

        self.exporter = settings.get('EXPORTER', None) or \
            stackdriver_exporter.StackdriverExporter(project_id=settings.get('GCP_PROJECT', None))
        if isinstance(self.exporter, six.string_types):
            self.exporter = configuration.load(self.exporter)

        self.propagator = settings.get('PROPAGATOR', None) or \
            GoogleCloudFormatPropagator()
        if isinstance(self.propagator, six.string_types):
            self.propagator = configuration.load(self.propagator)

        self.excludelist_paths = settings.get(EXCLUDELIST_PATHS, None)

        self.excludelist_hostnames = settings.get(EXCLUDELIST_HOSTNAMES, None)

        if django.VERSION >= (2,):  # pragma: NO COVER
            connection.execute_wrappers.append(_trace_db_call)

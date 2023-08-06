import logging
import json
import os

from google.cloud import pubsub_v1
from google.api_core import exceptions

from opencensus.trace import execution_context

from citibox.google_cloud_tracer.span_context import SpanContextBuilder
from citibox.google_cloud_tracer.tracer import disable_tracer_environment


class GoogleCloudPubSubPublisher:
    def __init__(self,
                 credentials_path: str = None,
                 project_id: str = None,
                 topic_prefix: str = "",
                 **kwargs):
        """GoogleCloud PubSub publisher constructor

        :type credentials_path: str
        :param credentials_path: Path to gcp json credentials file. If set to none will try to authenticate via environment

        :type project_id: str
        :param project_id: GCP project id, if not set will try to get it from environment

        :type topic_prefix: str
        :param topic_prefix: Sets a prefix in your PubSub topic to all events, as MyTopicPrefix_event_name

        """
        if credentials_path:
            self.publisher = pubsub_v1.PublisherClient.from_service_account_file(credentials_path)
        else:
            self.publisher = pubsub_v1.PublisherClient()
        if project_id:
            self._project_id = project_id
        else:
            self._project_id = os.environ.get('GCP_PROJECT', '')
        self._topic_prefix = topic_prefix
        self._logger = logging.getLogger(self.__class__.__name__)
        self._topic_cache = []

    def _get_or_create_topic(self, topic):
        topic_name = f'projects/{self._project_id}/topics/{self._topic_prefix + topic}'
        if topic_name not in self._topic_cache:
            try:
                pub_sub_topic = self.publisher.get_topic(topic_name)
            except exceptions.NotFound:  # pragma: no cover
                pub_sub_topic = self.publisher.create_topic(topic_name)
            self._topic_cache += [pub_sub_topic.name] if pub_sub_topic is not None else []
        return topic_name

    @staticmethod
    def _get_tracing_metadata():
        if disable_tracer_environment():
            return {}

        tracer = execution_context.get_opencensus_tracer()
        tracing_header = tracer.propagator.to_header(tracer.span_context)
        return {
            SpanContextBuilder.DEFAULT_GOOGLE_TRACE_HEADER_NAME: tracing_header
        }

    def publish_event(self, event: dict, event_id: str = None, topic: str = "", metadata: dict = None):
        if not metadata:
            metadata = {}

        self._logger.info(f'publishing event to pubsub', extra={"event": json.dumps(event)})
        metadata.update(self._get_tracing_metadata())
        future = self.publisher.publish(
            topic=self._get_or_create_topic(topic),
            data=json.dumps(event).encode('utf-8'),
            **metadata
        )
        if future.exception():
            self._logger.error(f'Error publishing message: {future.exception()}', extra={"event": json.dumps(event)})
        elif future.done():
            self._logger.info(f'Event {event_id or ""} published to pubsub')
        self._logger.debug(f'Event {event_id or ""} published', extra={"event": json.dumps(event)})

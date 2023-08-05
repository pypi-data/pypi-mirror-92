from django.conf import settings
from django.core.management.base import BaseCommand
from django_sqs_extended_client.aws.sns_client_extended import SNSClientExtended
from django_sqs_extended_client.queue.common import SignalHandler
import pydoc
import json


class Command(BaseCommand):
    help = 'Process Queue'

    def add_arguments(self, parser):
        parser.add_argument(
            'queue_code',
            type=str,
        )

    def handle(self, *args, **options):
        queue_code = options['queue_code']

        try:
            sns_event = getattr(settings.SNS_EVENT_ENUM, queue_code)
        except AttributeError:
            raise NotImplementedError(f'{queue_code} not implemented in settings.SNSEvent')

        try:
            queue_url = settings.SQS_EVENTS[sns_event.value]['sqs_queue_url']
        except KeyError:
            raise NotImplementedError(f'sqs_queue_url not implemented for settings.SQS_EVENTS[{sns_event.name}.value]')

        signal_handler = SignalHandler()

        while not self.get_received_signal(signal_handler=signal_handler):
            sns = SNSClientExtended(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY,
                                    settings.AWS_DEFAULT_REGION,
                                    settings.AWS_S3_QUEUE_STORAGE_NAME)
            messages = sns.receive_message(queue_url, 1, 10)
            if messages is not None and len(messages) > 0:
                for message in messages:
                    self.process_event(message)
                    sns.delete_message(queue_url, message.get('ReceiptHandle'))

    @staticmethod
    def get_received_signal(signal_handler):
        return signal_handler.received_signal

    @staticmethod
    def process_event(event_message):

        body = event_message.get('Body')
        content = body.get('Message')
        attributes = body.get('MessageAttributes')

        if 'content_type' in attributes:
            content_type = attributes.get('content_type')
            if content_type == 'json':
                data = json.loads(content)
            else:
                data = content
        else:
            data = content

        event_type = attributes.get('event_type')['Value']

        try:
            event_processor_class_path = settings.SQS_EVENTS[event_type]['event_processor']
        except KeyError as e:
            raise NotImplementedError(f'event_processor not implemented for settings.SQS_EVENTS[{event_type}]')
        event_processor_class = pydoc.locate(event_processor_class_path)
        if event_processor_class is None:
            raise FileNotFoundError(f'File "{event_processor_class_path}" not found')
        event_processor_class(data=data).execute()

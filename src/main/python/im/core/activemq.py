
import stomp
import logging

from im.core.config import configs

logger = logging.getLogger('im.core.activemq')


class MessageQueue(object):
    """A message queue from ActiveMQ to send messages to

    :param queue: The name of the queue to send the messages to.

    :param persistent: True if messages should be persistent, defaults to True.

    :param wait: If we should wait for the message to be delivered, defaults \
    to False

    :param host: The host to connect to, defaults to 127.0.0.1

    :param port: the port to connect to, defaults to 616163

    :param priority: The priority for the message , defaults to 6

    :param config: A dictionary to override default/global configuration.
    """

    default_configuration = {
        'dummy': False,
    }

    def __init__(self, queue, persistent=True, wait=False, host='127.0.0.1',
                 priority=6, port=61613, config=None):
        self.config = self.default_configuration.copy()
        self.config.update(configs.get('activemq', {}))
        if config:
            self.config.update(config)
        # XXX get host and port from config
        self.host = host
        self.port = port
        self.queue = queue
        self.persistent = persistent
        self.wait = wait
        self.priority = priority

    def send(self, message, **kwargs):
        """Send a message to the queue with the configured options as headers.

        :param message: The message to send to the queue

        :param kwargs: Extra parameters for the send method of \
        ``stomp.Connection``
        """

        if not message:
            logger.error('Got empty message for queue=%s, persistent=%s',
                self.queue, self.persistent)
            return False

        logger.debug('Debug message for queue=%s persistent=%s, message: %s',
            self.queue, self.persistent, message)

        if self.config.get('dummy'):
            logger.debug('Dummy message, not sending')
            return True

        try:
            conn = stomp.Connection([(self.host, self.port)])
            conn.start()
            conn.connect(wait=self.wait)
            conn.send(message=message, destination='/queue/%s' % self.queue, priority=self.priority,
                persistent=1 if self.persistent else 0, **kwargs)
            conn.stop()
        except stomp.exception.ConnectFailedException, e:
            logger.error(e)
            return False

        return True

    def send_sms(self, sms, override_message=None):
        """Send a message using a :class:`im.core.sms.Sms` instance, will
        serialize the message before sending.

        :param sms: A :class:`im.core.sms.Sms` instance to use as message

        :param override_message: If set then will create a new copy of \
        :class:`im.core.sms.Sms` with the overriding message and use that one.
        """
        if override_message:
            sms = sms.copy(override_message)
        return self.send(sms.serialized)

# -*- coding: utf-8 -*-
import functools
import time
import pika
import threading
from pika.exceptions import ConnectionClosed, ChannelClosed
import logging
logger = logging.getLogger("dingding_notify")


class MQConnection(object):
    def __init__(self, username, password, host, port,
                 virtual_host, connection_attempts, heartbeat, retry_delay, blocked_connection_timeout,
                 exchange_name="amq.direct", routing_key=""):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.connection_attempts = connection_attempts
        self.heartbeat = heartbeat
        self.retry_delay = retry_delay
        self.blocked_connection_timeout = blocked_connection_timeout
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.auth = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(credentials=self.auth, host=host, port=port,
                                      virtual_host=virtual_host, connection_attempts=connection_attempts,
                                      heartbeat=heartbeat, retry_delay=retry_delay,
                                      blocked_connection_timeout=blocked_connection_timeout))

    def consume(self, queue_name="amq.direct"):
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=10)
        self.channel.basic_consume(queue_name, self.consumer_callback, auto_ack=False)

    def reconnect(self):
        try:
            if self.connection and not self.connection.is_closed:
                self.channel.close()
                self.connection.close()
            self.__init__(self.username, self.password, self.host, self.port, self.virtual_host,
                          self.connection_attempts, self.heartbeat, self.retry_delay, self.blocked_connection_timeout,
                          self.exchange_name, self.routing_key)
        except Exception as e:
            logger.error(e)

    def produce(self, exchange, routing_key, data, serializer):
        self.channel = self.connection.channel()
        if serializer:
            data = serializer(data)

        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=data,
                                   properties=pika.BasicProperties(delivery_mode=2))


class MQConsume(MQConnection):
    def consumer_callback(self, ch, method, header, body):
        delivery_tag = method.delivery_tag

        self._do(data=body)

        # 开启子线程，确保消息被ack
        t = threading.Thread(target=self.do_ack, args=(self.connection, ch, delivery_tag))
        t.start()

    def do_ack(self, conn, ch, delivery_tag):
        cb = functools.partial(self.ack_message, ch, delivery_tag)
        conn.add_callback_threadsafe(cb)

    def ack_message(self, ch, deliver_tag):
        if ch.is_open:
            ch.basic_ack(deliver_tag)
        else:
            # channel已经关闭，重连确认
            self.reconnect()
            self.channel.basic_ack(deliver_tag)

    def _do(self, data):
        # 真正消费的函数
        pass

    def start_consume(self, qname):
        while 1:  # 重连机制
            try:
                self.consume(queue_name=qname)
                self.channel.start_consuming()
            except ConnectionClosed as e:
                time.sleep(1)
                logger.error(e)
                self.reconnect()
                self.start_consume(qname)
            except ChannelClosed as e:
                time.sleep(1)
                logger.error(e)
                self.reconnect()
                self.start_consume(qname)
            except Exception as e:
                time.sleep(1)
                logger.error(e)
                self.reconnect()
                self.start_consume(qname)

    def _from_queue(self, qname):
        # 消费入口函数
        self.start_consume(qname)


class MQPublish(MQConnection):
    def _to_queue(self, ex, key, data, count, serializer=None):
        try:
            self.produce(exchange=ex, routing_key=key, data=data, serializer=serializer)
            return True
        except Exception as e:
            if count <= 0:
                raise e
            time.sleep(1)
            self.reconnect()
            self._to_queue(ex, key, data, count=count-1)


if __name__ == '__main__':
    pass
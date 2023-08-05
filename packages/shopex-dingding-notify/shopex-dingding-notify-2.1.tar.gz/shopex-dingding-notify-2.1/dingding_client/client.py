from gevent import monkey
monkey.patch_all()
import gevent
from gevent.queue import JoinableQueue
import json
import time

from lib.log import *
from conf.config import MAXSIZE, RETRY_COUNT, TIME_STEP
from lib.notice_client import NoticeClient
from lib.pyamqp import MQConsume, MQPublish
logger = logging.getLogger("dingding_notify")

req_q = JoinableQueue(MAXSIZE)  # 在内存中开辟空间，用于存放将要发送消息的请求


def send_message(client, to_users):
    """发送消息"""
    while 1:
        try:
            item = req_q.get(timeout=1)
        except Exception as e:
            time.sleep(2)
            continue
        try:
            status, response = client.post(item, to_users)
            if status != "ok":
                logger.error(response)
            time.sleep(TIME_STEP)
        except Exception as e:
            logger.error(e)


class Work(MQConsume):
    """消费MQ的对象"""
    def _do(self, data):
        try:
            if not isinstance(data, dict):
                data = json.loads(data)
        except Exception as e:
            data = {"message": "消息传输格式错误，请传入json数据"}
            logger.error(e)

        try:
            req_q.put(data)
        except Exception as e:
            logger.error(e)

    def main(self, queue_name):
        self._from_queue(queue_name)


class SendMessageToDingDing(object):
    """发送消息到钉钉"""
    def __init__(self, app_key, app_secret, api_url, username="guest", password="guest", host="127.0.0.1", port=5672,
                 virtual_host="/", connection_attempts=5, heartbeat=60, retry_delay=1, blocked_connection_timeout=30):
        self.app_key = app_key
        self.app_secret = app_secret
        self.api_url = api_url
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.connection_attempts = connection_attempts
        self.heartbeat = heartbeat
        self.retry_delay = retry_delay
        self.blocked_connection_timeout = blocked_connection_timeout
        self.gevent_list = []

    def trans(self, to_users, client):
        """启动协程，发送消息到钉钉"""
        g = gevent.spawn(send_message, client, to_users)
        self.gevent_list.append(g)

    def consume(self, queues):
        """启动多个协程，消耗mq队列里面的消息"""
        for queue in queues:
            work = Work(username=self.username, password=self.password, host=self.host, port=self.port,
                        virtual_host=self.virtual_host, connection_attempts=self.connection_attempts,
                        heartbeat=self.heartbeat, retry_delay=self.retry_delay, blocked_connection_timeout=
                        self.blocked_connection_timeout)

            # 启动协程，创建多个连接实例
            g = gevent.spawn(work.main, queue)
            self.gevent_list.append(g)

    def start(self, to_users, queues):
        try:
            to_users = "|".join(to_users)
            sm_client = NoticeClient(self.app_key, self.app_secret, self.api_url)  # 真正发送消息的对象

            # 启动协程
            self.consume(queues)
            self.trans(to_users, sm_client)
            # gevent.joinall(self.gevent_list)
        except Exception as e:
            raise e


class SendMessageToMq(MQPublish):
    """发送消息到mq"""
    def __init__(self, username="guest", password="guest", host="127.0.0.1", port=5672, virtual_host="/",
                 connection_attempts=5, heartbeat=60, retry_delay=1,
                 blocked_connection_timeout=30, exchange_name="amq.direct", routing_key="event",):
        super(SendMessageToMq, self).__init__(username, password, host, port, virtual_host, connection_attempts,
                                              heartbeat, retry_delay, blocked_connection_timeout,
                                              exchange_name, routing_key,)

    def send(self, data):
        self._to_queue(self.exchange_name, self.routing_key, data, RETRY_COUNT)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 3:09 PM
# @Author  : wangdongming
# @Site    : 
# @File    : rabbitmq.py
# @Software: Hifive
import pika
import time
import random
import logging
from queue import Empty
from kombu import Connection


class RabbitMQ(object):

    def __init__(self, config):
        self.conn = Connection(userid=config['user'], password=config['passwd'],
                               hostname=config['host'], port=config['port'],
                               virtual_host=config['vhost'])

    def publisher(self, queue_name, *messages):
        simple_queue = self.conn.SimpleQueue(queue_name)
        for message in messages:
            simple_queue.put(message)
        simple_queue.close()

    def get_one(self, queue_name, block=False, timeout=5):
        simple_queue = self.conn.SimpleQueue(queue_name)
        try:
            message = simple_queue.get(block=block, timeout=timeout)
            message.ack()
            return message.body
        except Empty:
            return None
        finally:
            simple_queue.close()

    def qsize(self, queue_name):
        simple_queue = self.conn.SimpleQueue(queue_name)
        size = simple_queue.qsize()
        simple_queue.close()
        return size

    def release(self):
        self.conn.release()


class RabbitMqChannel(object):

    def __init__(self, queue_name, config, logger=None):
        self.logger = logger or logging.getLogger("rabbitmq")
        self.queue_name = queue_name
        self.config = config
        self._connect()

    @property
    def is_connect(self):
        return hasattr(self, "connection") \
               and self.connection.is_open

    def _connect(self):
        if self.is_connect:
            return
        config = self.config
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(userid=config['user'], password=config['passwd'],
                                      host=config['host'], port=config['port'],
                                      virtual_host=config['vhost']))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def close(self):
        if self.is_connect:
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class RabbitChWorker(RabbitMqChannel):

    def __init__(self, queue_name, receive_msg_callback, config, sleep_sec=None):
        assert (callable(receive_msg_callback))
        self.sleep_sec = sleep_sec or (0, 2)
        self.receive_msg_callback = receive_msg_callback
        super(RabbitChWorker, self).__init__(queue_name, config)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)

        self.channel.start_consuming()
        self.logger.info('[*]Worker running, waiting for messages...')

    def _sleep_time(self):
        sleep_sec = 0
        try:
            if isinstance(self.sleep_sec, int):
                sleep_sec = self.sleep_sec
            elif isinstance(self.sleep_sec, tuple):
                sleep_sec = random.randint(
                    min(self.sleep_sec),
                    max(self.sleep_sec)
                )
        except Exception:
            sleep_sec = 0
        return sleep_sec

    def callback(self, ch, method, properties, body):
        try:
            self.receive_msg_callback(body, properties)
        except Exception:
            self.logger.warning("unhandled error in worker callback.")
        time.sleep(self._sleep_time())
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __enter__(self):
        return self


class RabbitChPublisher(RabbitMqChannel):

    def push(self, message, routing_key=None):
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key or self.queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # 消息持久化,还有其他很多参数
            ))

    def __enter__(self):
        return self


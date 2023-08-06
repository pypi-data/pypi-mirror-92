#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/10/13 14:31
# @Author : Cheny
# @File : sqs.py
# @Software: Hifive
import time
import json
from typing import Callable, Dict, Any

import boto3
import traceback
from botocore.exceptions import EndpointConnectionError


class Sqs:
    def __init__(self, queue=None, queue_url=None, delay_seconds=900, **aws_config):
        self._poll_interval = 20
        if not any((queue, queue_url)):
            raise ValueError('Either `queue` or `queue_url` should be provided.')
        
        self.aws_config = aws_config
        self._session, self._client = self._connect()
        self.delay_seconds = delay_seconds
        
        self._queue_name = queue
        self._queue_url = queue_url
        if not queue_url:
            queues = self._client.list_queues(QueueNamePrefix=self._queue_name)
            for q in queues.get('QueueUrls', []):
                queue_name = self._get_queue_name_from_url(q)
                if queue_name == self._queue_name:
                    self._queue_url = q
                    break
            else:
                raise ValueError('No queue found with name ' + self._queue_name)
        else:
            self._queue_name = self._get_queue_name_from_url(queue_url)
    
    def _connect(self):
        max_retry = 200
        current_retry = 0
        while 1:
            try:
                self._session = boto3.session.Session(**self.aws_config)
                self._client = self._session.client('sqs')
                return self._session, self._client
            except EndpointConnectionError:
                current_retry += 1
                # 弃疗
                if current_retry > max_retry:
                    raise
                # 快弃疗了
                elif current_retry > max_retry // 2:
                    # logger.warning('too much sqs reconnect, connect frequency slow down...')
                    time.sleep(1)
    
    def send_message(self, message, **kwargs):
        """
        sends a message to the queue specified in the constructor
        :param message: (dict)
        :param kwargs: additional optional keyword arguments (DelaySeconds, MessageAttributes, MessageDeduplicationId, or MessageGroupId)
                        See http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Client.send_message for more information
        :return: (dict) the message response from SQS
        """
        # logger.info("Sending message to queue " + self._queue_name)
        for i in range(5):
            try:
                return self._client.send_message(
                    QueueUrl=self._queue_url,
                    MessageBody=json.dumps(message),
                    **kwargs,
                )
            except EndpointConnectionError:
                self._connect()
        else:
            # logger.error(f'Sending message to queue fail with connect error: {message}')
            return
    
    def listening(self, handle_message: Callable[[Dict, Any, Any], bool], **kwargs):
        """
        :param handle_message: handle_message(params_dict, message_attribs, attribs)
        :param kwargs:
        :return:
        """
        # logger.info(f'listen {self._queue_name}')
        
        while True:
            # calling with WaitTimeSeconds of zero show the same behavior as
            # not specifying a wait time, ie: short polling
            try:
                messages = self._client.receive_message(
                    QueueUrl=self._queue_url,
                    WaitTimeSeconds=self._poll_interval,
                    AttributeNames=['ALL', ],
                    MaxNumberOfMessages=1,
                    **kwargs
                )
            except EndpointConnectionError:
                self._connect()
                continue
            
            # 成功连接,重置重试计数器
            if 'Messages' in messages:
                # logger.info("{} sqs messages received".format(len(messages['Messages'])))
                # logger.debug(f'received sqs message {messages}')
                for m in messages['Messages']:
                    receipt_handle = m['ReceiptHandle']
                    m_body = m['Body']
                    message_attribs = None
                    attribs = None
                    
                    try:
                        params_dict = json.loads(m_body)
                    except json.JSONDecodeError:
                        # logger.warning("Unable to parse message - JSON is not formatted properly")
                        continue
                    if 'MessageAttributes' in m:
                        message_attribs = m['MessageAttributes']
                    if 'Attributes' in m:
                        attribs = m['Attributes']
                    
                    # 获取之后立即删除消息
                    try:
                        self._client.delete_message(
                            QueueUrl=self._queue_url,
                            ReceiptHandle=receipt_handle
                        )
                    # 删除时网络错误,那就直接跳过整条消息的处理,没删除
                    # 的消息在一段时间之后,又会重新出现在队列中
                    except EndpointConnectionError:
                        self._connect()
                        continue
                    
                    try:
                        handle_message(params_dict, message_attribs, attribs)
                    except Exception:
                        print(traceback.format_exc())
    
    @staticmethod
    def _get_queue_name_from_url(url):
        return url.split('/')[-1]

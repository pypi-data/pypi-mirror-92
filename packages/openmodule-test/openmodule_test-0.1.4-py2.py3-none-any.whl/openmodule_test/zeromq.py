from __future__ import unicode_literals

import logging
import random
import string
import threading
import time
import types
from contextlib import suppress
from typing import List, Tuple, Optional, Union, Dict
from uuid import uuid4, UUID

import orjson
import zmq
from om.message import Message
from pydantic import BaseModel, Field


def patch_bind_string(bind_string: str) -> str:
    """
    patches bind strings from zmq.Socket.bind so they can be used with zmq.Socket.connect
    """
    return bind_string.replace("://*", "://127.0.0.1")


class TestBroker(threading.Thread):
    __test__ = False

    xsub: zmq.Socket = None
    xpub: zmq.Socket = None

    def __init__(self, sub_bind, pub_bind):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.sub_bind = sub_bind
        self.pub_bind = pub_bind
        self.context = zmq.Context()

    def start(self) -> None:
        # overwriting start ensures that the sockets are bound after calling start()
        # if we bind in run(...) we might bind after another thread, and in the constructor
        # may be surprising to someone using the class aswell
        self.xsub = self.context.socket(zmq.XSUB)
        self.xpub = self.context.socket(zmq.XPUB)
        self.xsub.setsockopt(zmq.LINGER, 0)
        self.xpub.setsockopt(zmq.LINGER, 0)
        self.log.debug(f"binding on sub->{self.sub_bind} and pub->{self.pub_bind}")
        self.xsub.bind(self.sub_bind)
        self.xpub.bind(self.pub_bind)
        super().start()

    def run(self):
        try:
            self.log.debug("proxy started")
            zmq.proxy(self.xsub, self.xpub)
        except zmq.ContextTerminated:
            self.log.debug("context terminated, proxy shutting down")
        with suppress(Exception):
            self.xsub.close()
        with suppress(Exception):
            self.xpub.close()

    def stop(self):
        self.context.term()
        self.join()
        self.log.debug("proxy stopped")


class TestClient(threading.Thread):
    __test__ = False

    _startup_check_delay = 0.05
    _startup_check_iterations = 20  # 40 * 0.05 = 2 seconds

    _command_topic: bytes
    subscribed_topics: set
    pending_topics: Dict[bytes, None]

    pub: zmq.Socket = None
    sub: zmq.Socket = None

    def __init__(self, broker: TestBroker):
        super().__init__()
        self._command_topic = b"_testclient_" + str(uuid4()).encode("ascii")
        self.subscribed_topics = set()
        self.pending_topics = dict()

        self.broker = broker
        self.connected = threading.Event()
        self.log = logging.getLogger(self.__class__.__name__)
        self.recv_lock = threading.Lock()
        self.recv_messages = []
        self.has_messages = threading.Event()
        self.receiving_thread_id = None
        self.send_lock = threading.Lock()

    def subscribe(self, *topics: bytes):
        for topic in topics:
            self.sub.subscribe(topic)
            self.subscribed_topics.add(topic)
            self.pending_topics[topic] = None
        self.wait_for_topics()

    def wait_for_topics(self):
        for x in range(self._startup_check_iterations):
            with self.recv_lock:
                pending_topics = list(self.pending_topics.keys())
            if pending_topics:
                for topic in pending_topics:
                    self._zmq_cmd("hi", topic=topic)
                time.sleep(self._startup_check_delay)
            else:
                break

        assert not self.pending_topics, "error during startup and connect"

    def start(self):
        self.pub = self.broker.context.socket(zmq.PUB)
        self.sub = self.broker.context.socket(zmq.SUB)
        self.pub.setsockopt(zmq.LINGER, 0)
        self.sub.setsockopt(zmq.LINGER, 0)
        self.pub.connect(patch_bind_string(self.broker.sub_bind))
        self.sub.connect(patch_bind_string(self.broker.pub_bind))
        super().start()
        self.subscribe(self._command_topic)

    def _zmq_cmd(self, cmd, topic=None):
        if not self.broker.context.closed:
            Message(cmd=cmd).to_socket(self.pub, topic or self._command_topic)

    def run(self):
        try:
            while True:
                topic, message = Message.from_socket(self.sub)
                if topic == self._command_topic:
                    if message["cmd"] == "exit":
                        break

                with self.recv_lock:
                    if topic in self.pending_topics:
                        del self.pending_topics[topic]
                        continue

                with self.recv_lock:
                    self.recv_messages.append((topic, message))
                    self.has_messages.set()
        except zmq.ContextTerminated:
            pass
        except Exception:  # noqa
            assert False, "Internal exception, shutting down"
        else:
            self.log.debug("client thread stopped gracefully")

        with suppress(Exception):
            self.sub.close()
        with suppress(Exception):
            self.pub.close()

    def send(self, topic: bytes, _message=None, **kwargs):
        if isinstance(_message, BaseModel):
            with self.send_lock:
                self.pub.send_multipart((topic, orjson.dumps(_message.dict())))
        else:
            data = _message or kwargs
            assert isinstance(topic, bytes), "topic must be bytes"
            assert not (_message and kwargs), (
                "pass the message dict as the first parameter, or use the kwargs, not both"
            )
            assert "type" in data, "a message must always have a type"
            if "name" not in data:
                data["name"] = "testcase"
            with self.send_lock:
                Message(**data).to_socket(self.pub, topic)

    def _zmq_pop_from_front(self):
        with self.recv_lock:
            msg = self.recv_messages.pop(0)
            if not self.recv_messages:
                self.has_messages.clear()
            return msg

    def wait_for_message(self, filter, timeout=1) -> Tuple[bytes, dict]:
        """
        :param filter: filter function of type (topic: bytes, message: dict) -> bool
        :return: tuple containing [topic, message]
        """

        # protect the developer from using the client in multiple threads, this is not supported
        with self.recv_lock:
            assert self.receiving_thread_id is None, (
                "the test client is not thread safe! you have to use a separate client for each thread which"
                "wants to receive messages"
            )
            self.receiving_thread_id = threading.get_ident()

        try:
            start = time.time()
            while True:
                if not self.has_messages.wait(timeout=timeout):
                    raise TimeoutError()

                while self.recv_messages:
                    message_topic, message = self._zmq_pop_from_front()
                    if filter(message_topic, message):
                        return message_topic, message

                time_diff = time.time() - start
                if time_diff > timeout:
                    raise TimeoutError()
        finally:
            self.receiving_thread_id = None

    def wait_for_message_on_topic(self, topic=None, timeout=1) -> Tuple[bytes, dict]:
        """
        :return: tuple containing [topic, message]
        """
        assert topic in self.subscribed_topics, (
            "please subscribe to the topic you want to receive from first! call:\n"
            f'  > zmq_client.subscribe("{topic.decode()}")\n'
            f'or set\n'
            f'  > topics = ["{topic.decode()}"] in your test class'
        )
        return self.wait_for_message(lambda recv_topic, _: (not topic) or recv_topic == topic, timeout=timeout)

    def stop(self):
        self._zmq_cmd("exit")
        self.join()


def fake_config(broker: Optional[TestBroker] = None, **kwargs):
    result = {
        "NAME": "test"
    }
    if broker:
        result["BROKER_SUB"] = patch_bind_string(broker.sub_bind)
        result["BROKER_PUB"] = patch_bind_string(broker.pub_bind)

    result.update(kwargs)

    # converts to an object
    config = types.SimpleNamespace()
    for k, v in result.items():
        setattr(config, k, v)
    return config


class _TestRPCRequest(BaseModel):
    """
    we do not want to depend on openmodule, this is a minimal version of the zmq message for the rpc function
    """
    timestamp: float = Field(default_factory=time.time)
    name: str
    type: str
    rpc_id: UUID
    request: Optional[Dict]


class ZMQTestMixin(object):
    topics: List[Union[bytes, str]] = []
    rpc_channels: List[Union[bytes, str]] = []

    zmq_broker: TestBroker
    zmq_client: TestClient

    def setUp(self):
        super(ZMQTestMixin, self).setUp()
        random_suffix = random.choices(string.ascii_letters, k=10)
        self.zmq_broker = TestBroker(f"inproc://test-sub+{random_suffix}", f"inproc://test-pub-{random_suffix}")
        self.zmq_broker.start()
        self.zmq_client = TestClient(self.zmq_broker)
        self.zmq_client.start()

        topics = set(self.topics + [f"rpc-rep-{x}" for x in self.rpc_channels])
        topics = [x.encode("ascii") if isinstance(x, str) else x for x in topics]
        self.zmq_client.subscribe(*topics)

    def zmq_context(self):
        return self.zmq_broker.context

    def zmq_config(self):
        return fake_config(self.zmq_broker)

    def tearDown(self):
        super(ZMQTestMixin, self).tearDown()
        self.zmq_client.stop()
        self.zmq_broker.stop()

    def rpc(self, channel: str, type: str, request, timeout=1) -> dict:
        response_topic = f"rpc-rep-{channel}".encode("ascii")
        assert response_topic in self.zmq_client.subscribed_topics, (
            "you have to list the rpc channels you want to use beforehand. please set:\n"
            f'  > rpc_channels = ["{channel}"] in your test class '
        )

        rpc_id = str(uuid4())
        rpc_request = _TestRPCRequest(name="testclient", type=type, rpc_id=rpc_id, request=request)
        self.zmq_client.send(f"rpc-req-{channel}".encode("ascii"), rpc_request)
        _, response = self.zmq_client.wait_for_message(
            filter=lambda topic, message: topic == response_topic and message.get("rpc_id") == rpc_id,
            timeout=timeout
        )
        return response

    def assertRPCFailure(self, response: dict, expected_status="error"):
        self.assertEqual(expected_status, response.get("response", {}).get("status"))

    def assertRPCSuccess(self, response: dict):
        self.assertEqual("ok", response.get("response", {}).get("status"))

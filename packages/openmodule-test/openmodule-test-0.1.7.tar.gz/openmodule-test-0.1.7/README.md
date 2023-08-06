# Openmodule Test SDK

## ZMQ Messages

Our zmq stack requires a broker. For testcases a mixin exists, which starts a simple broker on `setUp(...)` and shuts it
down on `tearDown(...)`. Furthermore the mixin takes care of the slow joiner issue, by testing connectivity with each
topic it has subscribed to.

### Context

The `ZMQTextMixin` has some useful functions:

* `zmq_context()` returns the ZMQ Context of the broker. This context has to be used in order to utilize the `inproc://`
  transport.
* `zmq_config()` returns a config object with `BROKER_SUB` and `BROKER_PUB` set to the correct binds.

### Subscribing

The mixin automatically subscribes to all topics listed in the `topics` list, and all rpc response channels for the
rpc's listed in `rpc_channels`.

```python 
class MyTestCase(ZMQTestMixin, TestCase):
    topics = ["health"]
    rpc_channels = ["controller"]
```

For dynamically subscribing you *must* use the provided subscribe function. It again takes care of the slow joiner issue
by sending to the requested topic and waiting for a response.

```python 
class MyTestCase(ZMQTestMixin, TestCase):
    def test_something(self):
      ...
      self.zmq_client.subscribe("my-topic", "some-more-topics")
      ...
```

### Sending

In order to send, you have to specify the topic in the `topics` list of the testcase. You can then send by passing a
dict to the send function, or by passing keyword arguments.

```python 
class MyTestCase(ZMQTestMixin, TestCase):
    topics = ["test"]
    
    def test_something(self):
        self.zmq_client.send("test", type="test", some="data", even_more="data")
```

You can also pass a model instance directly and send it:

```python
class MyModel(OpenModuleModel):
    data: str


zmq_client.send("test", MyModel(some="data"))
```

### Receiving

Next message on a specific topic:

```python
topic, message = self.zmq_client.wait_for_message_on_topic(b"test")
```

Next message which matches a filter:

```python
rpc_id = ...
topic, message = self.zmq_client.wait_for_message(
    filter=lambda topic, message: message.get("rpc_id") == rpc_id
)
```

## RPC Servers

When testing RPC servers we again have to combat the slow joiner issue. In order to avoid it, a utility function exists
which waits until a passed RPC server has booted up compeltely. The method `wait_for_rpc_server(...)` registers a dummy
handler in each of the rpc server's channels, and calls it repeatetly until it receives an answer.

```python
class MyTestCase(RPCServerTestMixin, TestCase):
    rpc_channels = ["controller"]

    def test_my_server(self):
        my_server = my_code.get_server()
        self.wait_for_rpc_server(my_server)
```

#### Channels and dynamic registering of handlers

All RPC channels have to be listed in the `ZMQTestMixin.rpc_channels` of the testcase.

When registering RPC channels on the go, the function needs to be called again, to ensure that the rpc server is
properly listening on the new channels.
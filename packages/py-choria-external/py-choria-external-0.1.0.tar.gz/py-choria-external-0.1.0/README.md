# py-mco-agent

## Overview

`py-choria-external` implements the Choria External communications' protocol so that External Choria functions can be
written in the Python language.

## Installation

This library is typically pulled in as a dependency by other packages and is not useful on its own.

    pip install py-choria-external
    
This library requires a version of Choria with external agent support (0.12.1+)

## Related projects

For real-world usages of this library, see also:

* [py-mco-agent](https://github.com/optiz0r/py-mco-agent)
  Implements [Choria External Agent](https://choria.io/docs/development/mcorpc/externalagents/)
* [py-choria-discovery](https://github.com/optiz0r/py-choria-discovery)
  Implements [Choria External Discovery](https://choria.io/docs/concepts/discovery/#external)
    
## Implementing new Choria External functionality using this library

To implement support for a new Choria External function of type "Example"
create a python package with the following directory layout

```
choria_example/
├──schemas/
│  ├── io.choria.choria.example.v1.external_request.json
│  └── io.choria.choria.example.v1.external_reply.json
├── __init__.py
├── example.py
└── protocol.py
```

### Schemas

These are copies of the relevant [Choria Schema files](https://github.com/choria-io/schemas/tree/master/choria).

### protocol.py

The classes in this file implement the message handling. The `Request` class is populated with the
schema-validated data from an incoming RPC request. The `Reply` class encapsulates the response which
is validated against the reply schema before being sent back.

```python
import json
from choria_external.protocol import ProtocolMessage, Reply


@ProtocolMessage.register_protocol()
class ExampleRequest(ProtocolMessage):
  """ """
  _protocol = 'io.choria.choria.example.v1.external_request'

  @staticmethod
  def create_reply():
    return ExampleReply()


class ExampleReply(Reply):
  """ Describes the response to an Example Choria External request
      Handles serialisation of the response object
  """
  _protocol = 'io.choria.choria.example.v1.external_reply'
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # The following instance variables contain the data that will be returned
    # in the reply, as defined by the reply schema
    self.statuscode = 0
    self.data = {}

  def to_json(self):
    """ Serialises this reply object into JSON format to be sent back to Choria
    
        The return value of this method is validated against the reply schema and must
        be well formed for the reply to be sent back correctly. Malformed responses will
        result in an error being presented back to the client.
    """
    return json.dumps({
      'data': self.data,
      'statuscode': self.statuscode,
    })

  def fail(self):
    """ Marks the reply as failed.
        
        How that looks depends on the schema in use. Typically this sets an `error`
        field to a non-empty string, or sets a statuscode field to a non-zero number
    """
    self.statuscode = 1

  def successful(self):
    """ Exposes whether this request was successful or not
    """
    return self.statuscode == 0

```

### example.py

This file defined the base class for any concrete implementations of the Example external function.
In the simplest case, this might be an empty class. See [py-mco-agent](https://github.com/optiz0r/py-mco-agent)
for a more complex example.

```python
# Ensure the Protocol Messages are loaded and registered
import choria_example.protocol

from choria_external.base import ChoriaExternal


class Example(ChoriaExternal):
  """ Base class for implementations of the Example Choria External function
  """
  def example(self):
    """ Implement the example action
        This method should be overridden by subclasses
    """
    pass

  def execute(self):
    self.example()
```

### Concrete Implementation

This is an example concrete implementation. This script is what choria itself would be configured to execute.

```python
from choria_external.dispatcher import dispatch
from choria_example.example import Example


class SimpleExample(Example):

  def example(self):
    self.reply.data = {"hello": "world"}
    

if __name__ == '__main__':
  dispatch(SimpleExample)
```


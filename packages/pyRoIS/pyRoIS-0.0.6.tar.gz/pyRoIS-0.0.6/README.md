# pyrois

This software is an implementation of RoIS framework.
This software is released under the MIT License, see LICENSE.

## Overview

pyrois is an implementation of RoIS framework with python3.

## Abstract classes

### pyrois.RoIS_Comm
```python
class Command:
class Query:
class Event:
```
These are abstract classes for RoIS Components.

### pyrois.RoIS_HRI
```python
class SystemIF:
class CommandIF:
class QueryIF:
class EnventIF:
```
These are abstract classes for RoIS HRI Engine.

### pyrois.RoIS_Service
```python
class Service_Application_Base:
```
These are abstract classes for Service Application.

### Implementation with XML-RPC

* HRI_Engine_client, HRI_Engine_example
* Service_Application_IF, Service_Application_Base
* Person_Detection_client, Person_Detection

## Unit test

```
$ python -m pyrois.unittest -v

test_IF (__main__.TestHRIEngineIF)
test_IF ... ok
test_IF (__main__.TestHRIEngineIF_integrated)
test_IF ... ok
test_IF (__main__.TestPD)
test_IF ... ok
test_IF (__main__.TestServericeApplicationIF)
test_IF ... ok

----------------------------------------------------------------------
Ran 4 tests in 3.810s

OK
```

The four communication test are conducted on localhost.

1. HRI Engine separated interface between a Service Application and a HRI Engine
1. HRI Engine integrated interface between a Service Application and a HRI Engine
1. Service Application interface between a Service Application and a HRI Engine
1. HRI Component interface between a HRI Engine and a HRI Component

## References

1. RoIS Framework

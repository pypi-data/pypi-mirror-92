# Person_Detection.py
#
# Copyright 2018 Eiichi Inohira
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python3
# For HRI Component

"""Person_Detection
"""

import sys
import queue
import time
import threading
import xmlrpc.client

from . import RoIS_Common, RoIS_HRI, IF_server


class Command(RoIS_Common.Command):
    """Command
    """
    def __init__(self, c):
        self._component = c

    def start(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status

    def stop(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status

    def suspend(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status

    def resume(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        return status


class Query(RoIS_Common.Query):
    """Query
    """
    def __init__(self, c):
        self._component = c

    def component_status(self):
        status = RoIS_HRI.ReturnCode_t.OK.value
        c_status = RoIS_Common.Component_Status.UNINITIALIZED.value
        return (status, c_status)


class Event(RoIS_Common.Event):
    """Event
    """
    def __init__(self, c):
        self._component = c
        self.event_queue = queue.Queue()

    def poll_event(self):
        """poll_event
        """
        msg = self.event_queue.get()
        return msg

    def person_detected(self, timestamp, number):
        """person_detected
        """
        msg = xmlrpc.client.dumps((timestamp, number), 'person_detected')
        self.event_queue.put(msg)


class Person_Detection(Event, Command, Query):
    """Person_Detection
    """
    pass


class component:
    """component
    """
    def __init__(self):
        self._state = False

if __name__ == '__main__':
    pass

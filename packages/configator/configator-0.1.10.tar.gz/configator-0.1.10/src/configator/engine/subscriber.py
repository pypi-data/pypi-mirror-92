#!/usr/bin/env python3

import logging
import threading
import traceback, sys
import redis

from configator.engine.connector import RedisClient
from configator.engine.container import SettingCapsule
from configator.utils.function_util import assure_not_null, match_by_label, extract_parameters, transform_json_data
from typing import Any, Callable, List, Tuple, Dict, Optional

LOG = logging.getLogger(__name__)

class SettingSubscriber(object):
    #
    def __init__(self, *args, connector=None, **kwargs):
        if isinstance(connector, RedisClient):
            self.__use_shared_connector = True
            self.__connector = connector
        else:
            self.__use_shared_connector = False
            self.__connector = RedisClient(**kwargs)
        #
        self.__transformer = transform_json_data
        #
        self.CHANNEL_PATTERN = self.__connector.CHANNEL_GROUP + '*'
        #
        super(SettingSubscriber, self).__init__()
    #
    ##
    @property
    def connector(self):
        return self.__connector
    #
    ##
    @property
    def pubsub(self):
        ps = assure_not_null(self.__connector.connect()).pubsub()
        ps.psubscribe(**{self.CHANNEL_PATTERN: self.__process_event})
        return ps
    #
    ##
    __pubsub_thread = None
    __pubsub_lock = threading.RLock()
    #
    def start(self):
        with self.__pubsub_lock:
            if self.__pubsub_thread is None:
                self.__pubsub_thread = self.__run_in_thread(sleep_time=0.001)
                if LOG.isEnabledFor(logging.DEBUG):
                    LOG.log(logging.DEBUG, "SettingSubscriber has started")
            return self.__pubsub_thread
    #
    def stop(self):
        return self.close()
    #
    def close(self):
        with self.__pubsub_lock:
            if self.__pubsub_thread is not None:
                self.__pubsub_thread.stop()
            #
            if not self.__use_shared_connector:
                self.__connector.close()
            #
            if self.__pubsub_thread is not None:
                self.__pubsub_thread.join()
                self.__pubsub_thread = None
            #
            if LOG.isEnabledFor(logging.DEBUG):
                LOG.log(logging.DEBUG, "SettingSubscriber has stopped")
    #
    #
    def __run_in_thread(self, auto_start=True, sleep_time=0, daemon=False):
        thread = PubSubWorkerThread(self, sleep_time, daemon=daemon)
        if auto_start:
            thread.start()
        return thread
    #
    ##
    __transformer: Optional[Callable[[Dict], Tuple[Dict, Any]]] = None
    #
    def set_transformer(self, transformer: Callable[[Dict], Tuple[Dict, Any]]):
        if callable(transformer):
            self.__transformer = transformer
        return self
    #
    ##
    __event_mappings: Optional[Dict[Callable[[Dict, Any], bool], Tuple[Callable[[Dict, Any], None],...]]] = None
    #
    def add_event_handler(self, match: Callable[[Dict, Any], bool], *reset: Callable[[Dict, Any], None]):
        if self.__event_mappings is None:
            self.__event_mappings = dict()
        if not callable(match):
            raise ValueError('[match] must be callable')
        if not reset:
            raise ValueError('[reset] list must not be empty')
        for i, func in enumerate(reset):
            if not callable(func):
                raise ValueError('function#{0} must be callable'.format(i))
        self.__event_mappings[match] = reset
        return self
    #
    def __process_event(self, message):
        if self.__event_mappings is None:
            if LOG.isEnabledFor(logging.DEBUG):
                LOG.log(logging.DEBUG, "handler_mappings is empty (no service has been registered yet)")
            return
        #
        if self.__transformer is not None:
            msg, err = self.__transformer(message)
        else:
            msg, err = (message, None)
        #
        for match, reaction in self.__event_mappings.items():
            if match(msg, err):
                if LOG.isEnabledFor(logging.DEBUG):
                    LOG.log(logging.DEBUG, "the matching function [{0}] is matched".format(match.__name__))
                for reset in reaction:
                    if callable(reset):
                        if LOG.isEnabledFor(logging.DEBUG):
                            LOG.log(logging.DEBUG, "the handler [{0}] is triggered".format(reset.__name__))
                        reset(msg, err)
    #
    #
    def register_receiver(self, capsule: SettingCapsule):
        def wrap_capsule_reset(message, err):
            return capsule.reset(parameters=extract_parameters(message, err))
        if isinstance(capsule, SettingCapsule):
            self.add_event_handler(match_by_label(capsule.label), wrap_capsule_reset)
        return capsule


class PubSubWorkerThread(threading.Thread):
    def __init__(self, subscriber, sleep_time, daemon=False):
        super(PubSubWorkerThread, self).__init__()
        self.daemon = daemon
        #
        self._subscriber = subscriber
        self._sleep_time = sleep_time
        #
        self._running = threading.Event()
    #
    #
    def run(self):
        if self._running.is_set():
            return
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "PubSubWorkerThread is starting")
        self._running.set()
        while self._running.is_set():
            try:
                pubsub = self._subscriber.pubsub
                while self._running.is_set():
                    pubsub.get_message(ignore_subscribe_messages=True, timeout=self._sleep_time)
                pubsub.close()
            except redis.ConnectionError:
                self._subscriber.connector.reconnect()
            except Exception as err:
                if LOG.isEnabledFor(logging.ERROR):
                    LOG.log(logging.ERROR, err)
                traceback.print_exc(file=sys.stdout)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "PubSubWorkerThread has stopped")
    #
    #
    def stop(self):
        self._running.clear()

"""
TODO doc 
"""

import os
import sys
import threading
import time
import uuid

__all__=["HarvesterConfig"]

class HarvesterConfig(object):

    def __init__(self, config, namespace):
        self._config = config
        self._namespace = namespace

    def get(self, key, default=None):
        rst = self._config.get(key, default=None)
        rst = rst or self._config.get(key, namespace=self._namespace, default=default)
        return rst

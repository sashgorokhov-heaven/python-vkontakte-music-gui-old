import requests
from PySide import QtCore
from vkontakte_music.utils.multithreading import BaseThread
import logging

logger = logging.getLogger(__name__)


class AsyncRequest(BaseThread):
    on_success = QtCore.Signal(requests.Response)

    def __init__(self, url, query=None, on_success=None):
        super(AsyncRequest, self).__init__()
        if on_success:
            self.on_success.connect(on_success)
        self.url = url
        self.query = query

    def run(self):
        logger.debug('Request %s q=%s', self.url, self.query)
        response = requests.get(url=self.url, params=self.query, timeout=20)
        self.on_response(response)

    def on_response(self, response):
        """
        :param requests.Response response:
        """
        # logger.debug('Response: %s', response.text)
        self.on_success.emit(response)


class AsyncJsonRequest(AsyncRequest):
    on_success = QtCore.Signal(dict)

    def on_response(self, response):
        logger.debug('Response: %s', response.text)
        self.on_success.emit(response.json())
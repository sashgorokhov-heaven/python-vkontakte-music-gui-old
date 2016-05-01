from PySide import QtCore

import pyvkontakte

from vkontakte_music.utils.networking import AsyncJsonRequest


class AsyncVkontakteApi(pyvkontakte.VkontakteApi):
    def call(self, method, callback_slot=None, **kwargs):
        """
        :rtype: vkontakte_music.utils.networking.AsyncJsonRequest
        """
        if callback_slot is None:
            return super(AsyncVkontakteApi, self).call(method, **kwargs)
        params = self._params_encode(**kwargs)
        url = self.base_url + method
        thread = AsyncJsonRequest(url, params)
        thread.on_success.connect(callback_slot)
        return thread

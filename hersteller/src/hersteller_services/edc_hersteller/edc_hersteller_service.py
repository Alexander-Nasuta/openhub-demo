"""
This file has just been created automatically.
This is the file where you can write you own service.
Currently, the is code provides a basic producer and an basic consumer.
In order for your code to work, you must delete the code that you are not using and add your own application logic.
"""

import asyncio
import logging
import random

from fastiot.core import FastIoTService, Subject, subscribe, loop
from fastiot.core.core_uuid import get_uuid
from fastiot.core.time import get_time_now
from fastiot.msg.thing import Thing

from hersteller.logging.KIOptiPack_banner import KIOptiPack_banner
from hersteller.logging.wzl_banner import wzl_banner
from hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade import request_get_prediction

from quart import Quart, jsonify, request
import random

from hypercorn.asyncio import serve
from hypercorn.config import Config


class EdcHerstellerService(FastIoTService):
    """
    EDC Hersteller Service

    :param args: Positional arguments passed to the superclass or internal use.

    :param kwargs: Arbitrary keyword arguments, allowing \
                   for extensibility or forwarding to the\
                    superclass constructor or other components.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = Quart(__name__)
        self.app.add_url_rule('/edc/hersteller/dataplane/pred/', 'pred',
                              self.get_prediction, methods=['POST'])

    async def _start(self):
        print(wzl_banner)
        print(KIOptiPack_banner)
        self._logger.info("EDC Service (Hersteller) started.")
        self._logger.info(
            "EDC dataplane endpoint: 'http://0.0.0.0:5001/edc/hersteller/dataplane/pred/'")
        await self.run_app()

    async def get_prediction(self):
        """
        Requests an EDC prediction

        :return: The prediction
        :rtype: quart.Response

        """
        self._logger.info("POST /edc/hersteller/dataplane/pred/")
        data = await request.get_json()  # Access the JSON body of the POST request
        predictions = await request_get_prediction(fiot_service=self, data=data)
        return jsonify(predictions)

    async def run_app(self):
        """
        Starts the application

        """
        config = Config()
        config.bind = ["0.0.0.0:5001"]
        await serve(self.app, config)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    EdcHerstellerService.main()

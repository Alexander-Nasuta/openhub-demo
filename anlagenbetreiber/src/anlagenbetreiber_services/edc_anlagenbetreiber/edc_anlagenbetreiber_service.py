"""
This file has just been created automatically.
This is the file where you can write you own service.
Currently, the is code provides a basic producer and an basic consumer.
In order for your code to work, you must delete the code that you are not using and add your own application logic.
"""

import asyncio
import logging

from fastiot.core import FastIoTService, Subject, subscribe, loop, reply
from fastiot.core.core_uuid import get_uuid
from fastiot.core.time import get_time_now
from fastiot.msg.thing import Thing

from anlagenbetreiber.dataset.inital_annotated_dataset import raw_data
from anlagenbetreiber.logging.KIOptiPack_banner import KIOptiPack_banner
from anlagenbetreiber.logging.wzl_banner import wzl_banner

from quart import Quart, jsonify
import random

from hypercorn.asyncio import serve
from hypercorn.config import Config

from anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade import request_get_labeled_dataset, \
    error_response_thing, ok_response_thing, request_edc_prediction
from anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name import ML_EDC_SUBJECT


class EdcAnlagenbetreiberService(FastIoTService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = Quart(__name__)
        self.app.add_url_rule('/edc/anlagenbetreiber/dataplane/labeled-dataset/', 'labeled-dataset',
                              self.get_labeled_data, methods=['GET'])

    async def _start(self):
        print(wzl_banner)
        print(KIOptiPack_banner)

        self._logger.info("EDC (Anlagenbetreiber)  started.")
        self._logger.info(
            "EDC dataplane endpoint: 'http://0.0.0.0:5000/edc/anlagenbetreiber/dataplane/labeled-dataset/'")
        await self.run_app()

    async def get_labeled_data(self):
        self._logger.info("GET /edc/anlagenbetreiber/dataplane/labeled-dataset/")
        labeled_dataset: list[dict] = await request_get_labeled_dataset(fiot_service=self)
        return jsonify(labeled_dataset)

    async def run_app(self):
        config = Config()
        config.bind = ["0.0.0.0:5000"]
        await serve(self.app, config)

    @reply(ML_EDC_SUBJECT)
    async def get_prediction(self, _: str, msg: Thing) -> Thing:
        self._logger.info("Received request to get prediction.")

        if not isinstance(msg.value, list):
            self._logger.error(f"Payload (the 'value' field of the msg Thing) must be of type list, "
                               f"but received: {type(msg.value)}")
            e = ValueError("Payload must be a list of processed data points")
            return error_response_thing(exception=e, fiot_service=self)

        try:
            import requests
            url = 'http://0.0.0.0:5001/edc/hersteller/dataplane/pred/'
            predictions = requests.post(url, json=msg.value)
            self._logger.info(f"fowarding predictions: {predictions.json()}")
            res = predictions.json()


        except Exception as e:
            self._logger.error(f"Error while fetching labeled data over the edc: {e}")
            return error_response_thing(exception=e, fiot_service=self)

        return ok_response_thing(payload=res, fiot_service=self)


if __name__ == '__main__':
    # Change this to reduce verbosity or remove completely to use `FASTIOT_LOG_LEVEL` environment variable to configure
    # logging.
    logging.basicConfig(level=logging.DEBUG)
    EdcAnlagenbetreiberService.main()

"""
This file has just been created automatically.
This is the file where you can write you own service.
Currently, the is code provides a basic producer and an basic consumer.
In order for your code to work, you must delete the code that you are not using and add your own application logic.
"""

import asyncio
import logging
import random

from fastiot.core import FastIoTService, Subject, subscribe, loop, reply
from fastiot.core.core_uuid import get_uuid
from fastiot.core.time import get_time_now
from fastiot.msg.thing import Thing

from anlagenbetreiber.logging.KIOptiPack_banner import KIOptiPack_banner
from anlagenbetreiber.logging.wzl_banner import wzl_banner

import requests

from dienstleister.ml_lifecycle_utils.edc_endpoints import dataset_edc_endpoint
from dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade import error_response_thing, ok_response_thing
from dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name import DB_GET_EDC_LABELED_DATASET_SUBJECT


def edc_fetch_dict_list(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()  # Convert JSON response to Python data structure
    return data


class EdcDienstleisterService(FastIoTService):

    async def _start(self):
        print(wzl_banner)
        print(KIOptiPack_banner)
        self._logger.info("Edc (Dienstleister) started.")

    @reply(DB_GET_EDC_LABELED_DATASET_SUBJECT)
    async def get_labeled_dataset(self, _: str, __: Thing) -> Thing:
        self._logger.info("Received request to get labeled dataset over the edc.")

        try:
            labeled_dataset = edc_fetch_dict_list(dataset_edc_endpoint)

        except Exception as e:
            self._logger.error(f"Error while fetching labeled data over the edc: {e}")
            return error_response_thing(exception=e, fiot_service=self)

        return ok_response_thing(payload=labeled_dataset, fiot_service=self)



if __name__ == '__main__':
    # Change this to reduce verbosity or remove completely to use `FASTIOT_LOG_LEVEL` environment variable to configure
    # logging.
    logging.basicConfig(level=logging.DEBUG)
    EdcDienstleisterService.main()

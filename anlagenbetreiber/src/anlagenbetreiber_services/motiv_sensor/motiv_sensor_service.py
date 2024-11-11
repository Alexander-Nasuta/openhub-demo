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

from flask import Flask, jsonify
import random

from anlagenbetreiber.logging.KIOptiPack_banner import KIOptiPack_banner
from anlagenbetreiber.logging.wzl_banner import wzl_banner
from anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade import request_get_labeled_dataset, \
    request_save_many_raw_data_points


class MotivSensorService(FastIoTService):

    async def _start(self):
        print(wzl_banner)
        print(KIOptiPack_banner)
        self._logger.info("MotivSensorService started.")

    @loop
    async def produce(self):
        """ Creating some dummy data and publish it """
        data = [{
            'sensor_name': f'motiv_sensor_{random.randint(1, 5)}',
            'value': random.randint(20, 30)
        }, {
            'sensor_name': f'motiv_sensor_{random.randint(1, 5)}',
            'value': random.randint(20, 30)
        }]
        self._logger.info(f"Publishing: {data}")
        try:
            response =await request_save_many_raw_data_points(fiot_service=self, data=data)
            self._logger.info(f"received response from db-service: {response}")
        except Exception as e:
            self._logger.error(f"Error occurred: {e}.")
            self._logger.error(f"Check if the database service is running.")

        return asyncio.sleep(5)



if __name__ == '__main__':
    # Change this to reduce verbosity or remove completely to use `FASTIOT_LOG_LEVEL` environment variable to configure
    # logging.
    logging.basicConfig(level=logging.DEBUG)
    MotivSensorService.main()

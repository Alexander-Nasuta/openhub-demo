"""
This file has just been created automatically.
This is the file where you can write you own service.
Currently, the is code provides a basic producer and an basic consumer.
In order for your code to work, you must delete the code that you are not using and add your own application logic.
"""

import asyncio
import logging
import random
import pprint

from fastiot.core import FastIoTService, Subject, subscribe, loop
from fastiot.core.core_uuid import get_uuid
from fastiot.core.time import get_time_now
from fastiot.msg.thing import Thing

from anlagenbetreiber.logging.KIOptiPack_banner import KIOptiPack_banner
from anlagenbetreiber.logging.wzl_banner import wzl_banner
from anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade import request_edc_prediction


class MachinenParametrierungService(FastIoTService):
    """
    Machinen Parametrierung Service
    """

    async def _start(self):
        """

        Returns
        -------

        """
        print(wzl_banner)
        print(KIOptiPack_banner)
        self._logger.info("Machinen Parametrierung Service (Anlagenbetreiber)  started.")

    @loop
    async def produce(self):
        """

        Returns
        -------

        """
        try:
            input_data = [self.generate_random_datapoint() for _ in range(2)]
            self._logger.info(f"Producing data: \n{pprint.pformat(input_data)}")

            predictions = await request_edc_prediction(fiot_service=self, data=input_data)

            self._logger.info(f"Received predictions: \n{pprint.pformat(predictions)}")
        except Exception as e:
            self._logger.error(e)

        return asyncio.sleep(5*60)

    @staticmethod
    def generate_random_datapoint() -> dict:
        """

        Returns
        -------

        """
        return {
            "ListeKomponenten": ["K000055", "K000057"],  # id or material name
            "Massenanteile": [0.75, 0.25],  # unit g/g
            "Flächenanteilmodifiziert": 0,  # unit %
            "Geometrie": "Quader",  # unit: list of types
            "Kopfraumatmosphäre": None,  # unit list of (pa)
            "Masse": None,  # unit g
            "Verpackungstyp": "Folie",  # type
            "CAD": None,  # link to CAD file
            "RauheitRa": 0.08966666666666667,  # unit µm
            "RauheitRz": 0.7366666666666667,  # unit µm
            "Trübung": 176.6,  # unit HLog
            "Glanz": 39,  # unit GE
            "Dicke": 769.6666666666666,  # unit µm
            "Emodul": 878.7979886112262,  # unit MPa
            "MaximaleZugspannung": 37.156951742990245,  # unit MPa
            "MaximaleLängenänderung": 19.73276680651324,  # unit %
            # Quality Labels
            "Ausformung": random.randint(1, 6),
            "Kaltverfo": random.randint(1, 3),
        }


if __name__ == '__main__':
    # Change this to reduce verbosity or remove completely to use `FASTIOT_LOG_LEVEL` environment variable to configure
    # logging.
    logging.basicConfig(level=logging.DEBUG)
    MachinenParametrierungService.main()

"""
This file has just been created automatically.
This is the file where you can write you own service.
Currently, the is code provides a basic producer and an basic consumer.
In order for your code to work, you must delete the code that you are not using and add your own application logic.
"""

import asyncio
import logging
import pandas as pd
import random

from fastiot.core import FastIoTService, Subject, subscribe, loop, reply
from fastiot.core.core_uuid import get_uuid
from fastiot.core.time import get_time_now
from fastiot.msg.thing import Thing
from sklearn.pipeline import Pipeline

from dienstleister.data_processing.pipeline_operations import OneHotEncodePd, NormalizeCols, MultiOneHotEncodePd, \
    ColumnDropper
from dienstleister.logging.KIOptiPack_banner import KIOptiPack_banner
from dienstleister.logging.wzl_banner import wzl_banner
from dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade import error_response_thing, ok_response_thing
from dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name import DATA_PROCESSING_PROCESS_RAW_DATA_SUBJECT


class DataProcessingService(FastIoTService):
    _preprocessor = Pipeline(
        verbose=False,
        steps=[
            (
                "Drop irrelevant columns",
                # CAS is always None,
                # Verpackungstyp is always 'Folie'
                # Masse is always None
                # Geometrie is always 'Quader'
                # Kopfraumatmosphäre is always None
                # Flächenanteilmodifiziert is always 0
                # therefore these fields do not provide any information
                ColumnDropper(["CAD", "Verpackungstyp", "Masse", "Geometrie", "Massenanteile", "Kopfraumatmosphäre",
                               "Flächenanteilmodifiziert", "_id"]),
            ), (
                "One-hot encode ListeKomponenten",
                MultiOneHotEncodePd(
                    target="ListeKomponenten",
                    prefix="Komponente",
                    sep="_",
                    required_columns=[
                        "Komponente_K000034",
                        "Komponente_K000035",
                        "Komponente_K000055",
                        "Komponente_K000057",
                        "Komponente_K000141"
                    ]
                )
            ),
            ("Normalise RauheitRa", NormalizeCols(
                target="RauheitRa",
                column_range=(0.05933333333333333, 0.729),
                feature_range=(0, 1)
            )),
            ("Normalise RauheitRz", NormalizeCols(
                target="RauheitRz",
                column_range=(0.39666666666666667, 3.33),
                feature_range=(0, 1)
            )),
            ("Normalise Trübung", NormalizeCols(
                target="Trübung",
                column_range=(63.9, 450.7),
                feature_range=(0, 1))
             ),
            ("Normalise Glanz", NormalizeCols(
                target="Glanz",
                column_range=(27, 67),
                feature_range=(0, 1)
            )),
            ("Normalise Dicke", NormalizeCols(
                target="Dicke",
                column_range=(727.6666666666666, 794.6666666666666),
                feature_range=(0, 1)
            )),
            ("Normalise Emodul", NormalizeCols(
                target="Emodul",
                column_range=(775.2626646454261, 923.5297844703941),
                feature_range=(0, 1)
            )),
            ("Normalise MaximaleZugspannung",
             NormalizeCols(
                 target="MaximaleZugspannung",
                 column_range=(29.682633925969455, 39.27389962516748),
                 feature_range=(0, 1)
             )),
            ("Normalise MaximaleLängenänderung", NormalizeCols(
                target="MaximaleLängenänderung",
                column_range=(12.61880576560562, 75.62994222943517),
                feature_range=(0, 1)
            )),
            ("Normalise Temp", NormalizeCols(
                target="Temp",
                column_range=(0, 500),
                feature_range=(0, 1)
            )),
            ("Normalise Druck", NormalizeCols(
                target="Druck",
                column_range=(0, 6),
                feature_range=(0, 1)
            )),
            ("Normalise Zeit", NormalizeCols(
                target="Zeit",
                column_range=(0, 40),
                feature_range=(0, 1)
            )),
            (
                "One-hot encode Ausformung",
                OneHotEncodePd(
                    target="Ausformung",
                    prefix="Ausformung",
                    sep="_",
                    required_columns=[
                        "Ausformung_1",
                        "Ausformung_1.0",
                        "Ausformung_1.5",
                        "Ausformung_2",
                        "Ausformung_2.0",
                        "Ausformung_2.5",
                        "Ausformung_3",
                        "Ausformung_3.0",
                        "Ausformung_3.5",
                        "Ausformung_4",
                        "Ausformung_4.0",
                        "Ausformung_4.5",
                        "Ausformung_5",
                        "Ausformung_5.0",
                        "Ausformung_5.5",
                        "Ausformung_6",
                        "Ausformung_6.0",
                        "Ausformung_6.5",
                    ]
                )
            ),
            (
                "One-hot encode Kaltverfo",
                OneHotEncodePd(
                    target="Kaltverfo",
                    prefix="Kaltverfo",
                    sep="_",
                    required_columns=[
                        "Kaltverfo_1",
                        "Kaltverfo_1.0",
                        "Kaltverfo_1.5",
                        "Kaltverfo_2",
                        "Kaltverfo_2.0",
                        "Kaltverfo_2.5",
                        "Kaltverfo_3",
                        "Kaltverfo_3.0",
                        "Kaltverfo_3.5",
                    ]
                )
            ),
        ])

    async def _start(self):
        print(wzl_banner)
        print(KIOptiPack_banner)
        self._logger.info("ML Data Processing Service (Dienstleister) started.")

    @reply(DATA_PROCESSING_PROCESS_RAW_DATA_SUBJECT)
    async def get_labeled_dataset(self, _: str, msg: Thing) -> Thing:
        self._logger.info("Received request to get labeled dataset over the edc.")

        if not isinstance(msg.value, list):
            self._logger.error(f"Payload (the 'value' field of the msg Thing) must be of type list, "
                               f"but received: {type(msg.value)}")
            e = ValueError("Payload must be a list of processed data points")
            return error_response_thing(exception=e, fiot_service=self)

        try:
            data_to_process = msg.value

            df = pd.DataFrame(data_to_process)
            self._logger.info(f"Received {len(df)} data points to process.")
            print(df.head())

            df = self._preprocessor.fit_transform(df)

            # convert df to a list of dicts
            processed_data = df.to_dict(orient="records")
            self._logger.info(f"Processed data points:")
            print(df.head())

        except Exception as e:
            self._logger.error(f"Error while fetching labeled data over the edc: {e}")
            return error_response_thing(exception=e, fiot_service=self)

        return ok_response_thing(payload=processed_data, fiot_service=self)


if __name__ == '__main__':
    # Change this to reduce verbosity or remove completely to use `FASTIOT_LOG_LEVEL` environment variable to configure
    # logging.
    logging.basicConfig(level=logging.DEBUG)
    DataProcessingService.main()

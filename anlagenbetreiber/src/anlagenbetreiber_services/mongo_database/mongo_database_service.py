"""
This file has just been created automatically.
This is the file where you can write you own service.
Currently, the is code provides a basic producer and an basic consumer.
In order for your code to work, you must delete the code that you are not using and add your own application logic.
"""

import asyncio
import logging
import random
import uuid

from fastiot.core import FastIoTService, Subject, subscribe, loop, reply
from fastiot.core.core_uuid import get_uuid
from fastiot.core.time import get_time_now
from fastiot.msg.thing import Thing

import pymongo
from pymongo import UpdateOne, MongoClient
from pymongo.results import InsertManyResult, BulkWriteResult

from anlagenbetreiber.logging.KIOptiPack_banner import KIOptiPack_banner
from anlagenbetreiber.logging.wzl_banner import wzl_banner
from anlagenbetreiber.dataset.inital_annotated_dataset import raw_data
from anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade import error_response_thing, ok_response_thing
from anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name import DB_GET_LABELED_DATASET_SUBJECT, \
    DB_SAVE_MANY_RAW_DATAPOINTS_SUBJECT


class MongoDatabaseService(FastIoTService):
    """
    MongoDB Database Service
    """
    _db_username = 'fiot'
    _db_password = 'fiotdev123'
    _db_port = '27017'
    _db_host = 'localhost'

    _DB_NAME = "mongodb"
    _MONGO_DB = "anlagenbetreiber"
    _MONGO_RAW_DATA_COLLECTION = "sensor_data_raw"
    _MONGO_LABELED_DATA_COLLECTION = "labeled_data"

    _mongodb_client: MongoClient = None
    _db: pymongo.synchronous.database.Database = None
    _raw_data_collection: pymongo.synchronous.collection.Collection = None

    def __init__(self, *args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs

        """
        super().__init__(*args, **kwargs)
        connection_string = f"mongodb://{self._db_username}:{self._db_password}@{self._db_host}:{self._db_port}/?authMechanism=SCRAM-SHA-1"
        self._mongodb_client = MongoClient(connection_string)
        self._db = self._mongodb_client[self._MONGO_DB]
        self._raw_data_collection = self._db[self._MONGO_RAW_DATA_COLLECTION]
        self._labeled_data_collection = self._db[self._MONGO_LABELED_DATA_COLLECTION]

    async def _start(self):
        """

        """
        print(wzl_banner)
        print(KIOptiPack_banner)
        self._logger.info("MongoDatabaseService started.")
        await self.setup_labeled_dataset()

    async def setup_labeled_dataset(self):
        """

        """
        # check if the labeled data collection is empty
        if self._labeled_data_collection.count_documents({}) > 0:
            return

        self._logger.info("Setting up annotated dataset.")
        labeled_dataset: list[dict] = raw_data
        self._labeled_data_collection.insert_many(labeled_dataset)
        self._logger.info(f"Inserted {len(labeled_dataset)} labeled data entries to the database.")

    @reply(DB_GET_LABELED_DATASET_SUBJECT)
    async def get_labeled_dataset(self, _: str, __: Thing) -> Thing:
        """

        """
        self._logger.info("Received request to get labeled dataset.")

        try:
            labeled_data_entries = self._labeled_data_collection.find()
            labeled_data_entries = [dict(data) for data in labeled_data_entries]

            # the native mongo ID is not serializable to json
            # so we convert it to a string
            for data in labeled_data_entries:
                data["_id"] = str(data["_id"])

        except Exception as e:
            self._logger.error(f"Error while counting processed data points in mongodb: {e}")
            return error_response_thing(exception=e, fiot_service=self)

        return ok_response_thing(payload=labeled_data_entries, fiot_service=self)

    @reply(DB_SAVE_MANY_RAW_DATAPOINTS_SUBJECT)
    async def db_save_many_raw_datapoints(self, _: str, msg: Thing) -> Thing:
        """
        Saves many raw data points to the database.

        :param _: The topic of the message. This is not used in this method.
        :type _: str
        :param msg: The message that contains the raw data points to be saved to the database.
        :return: A Thing object that contains the result of the operation. This is either an acknowledgement or an error.
                Acknowledgements contain the number of raw data points that were saved to the database.
        :rtype: Thing

        """
        if not isinstance(msg.value, list):
            self._logger.error(f"Payload (the 'value' field of the msg Thing) must be of type list, "
                               f"but received: {type(msg.value)}")
            raise ValueError("Payload must be a list of raw data points")

        data_points: list[dict] = msg.value
        self._logger.info(f"Received {len(data_points)} raw data points to be inserted into mongodb")

        # add uuids to data points
        for data_point in data_points:
            data_point["_id"] = str(uuid.uuid4())

        self._logger.info(f"Insering data points into mongodb")
        res: InsertManyResult = self._raw_data_collection.insert_many(data_points)
        self._logger.info(f"DB transaction result: {res.acknowledged}")

        self._logger.info(f"Inserted {len(res.inserted_ids)} raw data points into mongodb")

        # feel free to include whatever information you want to return here.
        db_specific_info = {
            "acknowledged": True,
            "db": "MongoDB",
        }

        # in principle one does not need to return information here.
        # However, some infos are return here, so that the requesting service can log the information.
        return ok_response_thing(payload=db_specific_info, fiot_service=self)


if __name__ == '__main__':
    # Change this to reduce verbosity or remove completely to use `FASTIOT_LOG_LEVEL` environment variable to configure
    # logging.
    logging.basicConfig(level=logging.DEBUG)
    MongoDatabaseService.main()

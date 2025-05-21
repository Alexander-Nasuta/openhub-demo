from asyncio import Future

from fastiot.core import FastIoTService, ReplySubject
from fastiot.msg import Thing

from datetime import datetime

from anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name import _SAVE_MANY_RAW_DATA_SUBJECT_NAME, \
    _GET_ALL_RAW_DATA_SUBJECT_NAME, _UPSERT_MANY_PROCESSED_DATA_SUBJECT_NAME, DB_GET_PROCESSED_DATA_COUNT_SUBJECT, \
    _GET_PROCESSED_DATA_COUNT_SUBJECT_NAME, DB_GET_PROCESSED_DATA_PAGE_SUBJECT, _GET_PROCESSED_DATA_PAGE_SUBJECT_NAME, \
    _PROCESS_RAW_DATA_SUBJECT_NAME, _PREDICT_SUBJECT_NAME, _GET_LABELED_DATASET_SUBJECT_NAME, _PREDICT_EDC_SUBJECT_NAME

import logging

log = logging.getLogger('BrokerFacade')


def ok_response_thing(payload: dict | list, fiot_service: FastIoTService) -> Thing:
    """
    Creates a Thing object with the payload and the name of the service that created it.

    :param payload: The payload to be sent.
    :type payload: dict | list

    :param fiot_service: The service that created the payload.
    :type fiot_service: FastIoTService

    :return: A Thing object with the payload and the name of the service that created it.
    :rtype: Thing
    """
    return Thing(
        machine=f'{fiot_service.__class__.__name__}',
        name="",
        value=payload,
        timestamp=datetime.now()
    )


def error_response_thing(exception: Exception, fiot_service: FastIoTService) -> Thing:
    """
    Creates a Thing object with the error information and the name of the service that created it.

    :param exception: The exception that was raised.
    :type exception: Exception

    :param fiot_service: The service that raised the exception.
    :type fiot_service: FastIoTService

    :return: A Thing object with the error information and the name of the service that created it.
    :rtype: Thing
    """
    error_info_dict = {
        "__error_occured__": True,
        "error_type": type(exception).__name__,
        "error_msg": str(exception),
        "error_args": exception.args,
    }
    return Thing(
        machine=f'{fiot_service.__class__.__name__}',
        name="",
        value=error_info_dict,
        timestamp=datetime.now()
    )


async def request_replysubject_thing_wrapper(fiot_service: FastIoTService, data: dict | list[dict],
                                             subject: str, timeout: float) -> Future[
    dict | list[dict] | int | float | str | None]:
    """
    This function wraps the request to the broker and handles the response.

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: dict

    :param subject: The subject to which the request is sent.
    :type subject: str

    :param timeout: Seconds to wait for a response.
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    if not isinstance(data, dict) and not isinstance(data, list):
        raise TypeError("The data parameter has to be a dict or a list of dicts.")

    payload = Thing(
        machine=f'{fiot_service.__class__.__name__}',
        name="",
        value=data,
        timestamp=datetime.now()
    )
    # subject = ReplySubject(name="reply", msg_cls=Thing, reply_cls=Thing)
    subject = ReplySubject(name=subject, msg_cls=Thing, reply_cls=Thing)

    log.debug(f"Sending reply-subject request to broker (subject={subject.name}, requesting service={payload.machine})")
    # asyncio.ensure_future does not work here. It has to be awaited.
    response_thing = await fiot_service.broker_connection.request(subject=subject, msg=payload, timeout=timeout)

    if isinstance(response_thing.value, dict) and "__error_occured__" in response_thing.value.keys():
        log.error(f"Error occured while requesting service: {response_thing.value}")
        error_type = response_thing.value["error_type"]
        error_args = response_thing.value["error_args"]
        raise globals()[error_type](*error_args) from None
    return response_thing.value


async def request_save_many_raw_data_points(fiot_service: FastIoTService, data: list[dict],
                                            timeout: float = 10) -> Future[dict | list[dict]]:
    """
    This function sends a request to the broker under the \
    :py:data:`DB_SAVE_MANY_RAW_DATAPOINTS_SUBJECT <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_SAVE_MANY_RAW_DATAPOINTS_SUBJECT>` \
    subject to save raw datapoints to the database utilizing the :func:`request_replysubject_thing_wrapper <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper>`

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: list[dict]

    :param timeout: Seconds to wait for a response
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    if not isinstance(data, list):
        raise TypeError("The data parameter has to be a list of dicts.")
    # asyncio.ensure_future does not work here. It has to be awaited.
    return await request_replysubject_thing_wrapper(
        fiot_service=fiot_service,
        data=data,
        subject=_SAVE_MANY_RAW_DATA_SUBJECT_NAME,  # same as the string "save-many-raw-datapoints"
        timeout=timeout,  # default is 10
    )


async def request_upsert_many_processed_data_points(fiot_service: FastIoTService, data: list[dict],
                                                    timeout: float = 10) -> Future[dict | list[dict]]:
    """
    This function sends a request to the broker under the \
    :data:`DB_UPSERT_MANY_PROCESSED_DATAPOINTS_SUBJECT <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_UPSERT_MANY_PROCESSED_DATAPOINTS_SUBJECT>` \
    subject to update processed datapoints in the database utilizing the :func:`request_replysubject_thing_wrapper <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper>`

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: list[dict]

    :param timeout: Seconds to wait for a response
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    if not isinstance(data, list):
        raise TypeError("The data parameter has to be a list of dicts.")
    # asyncio.ensure_future does not work here. It has to be awaited.
    return await request_replysubject_thing_wrapper(
        fiot_service=fiot_service,
        data=data,
        subject=_UPSERT_MANY_PROCESSED_DATA_SUBJECT_NAME,  # same as the string "save-many-raw-datapoints"
        timeout=timeout,  # default is 10
    )


async def request_get_all_raw_data_points(fiot_service: FastIoTService,
                                          timeout: float = 10) -> Future[dict | list[dict]]:
    """
    This function sends a request to the broker under the \
    :data:`DB_GET_ALL_RAW_DATA_SUBJECT <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_ALL_RAW_DATA_SUBJECT>` \
    for all raw datapoints in the database utilizing the :func:`request_replysubject_thing_wrapper <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper>`

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: list[dict]

    :param timeout: Seconds to wait for a response
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    return await request_replysubject_thing_wrapper(
        fiot_service=fiot_service,
        data={},
        subject=_GET_ALL_RAW_DATA_SUBJECT_NAME,  # same as the string "get-all-raw-datapoints"
        timeout=timeout,  # default is 10
    )


async def request_get_all_processed_data_points(fiot_service: FastIoTService,
                                                timeout: float = 10) -> Future[dict | list[dict]]:
    """
    This function sends a request to the broker under the \
    :data:`DB_GET_ALL_PROCESSED_DATA_SUBJECT <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_ALL_PROCESSED_DATA_SUBJECT>` \
    for all processed datapoints in the database utilizing the \
    :func:`request_replysubject_thing_wrapper <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper>`

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: list[dict]

    :param timeout: Seconds to wait for a response
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    return await request_replysubject_thing_wrapper(
        fiot_service=fiot_service,
        data={},
        subject=_GET_ALL_RAW_DATA_SUBJECT_NAME,  # same as the string "get-all-raw-datapoints"
        timeout=timeout,  # default is 10
    )


# pagination requests
async def request_get_processed_data_points_count(fiot_service: FastIoTService,
                                                  timeout: float = 10) -> Future[int]:
    """
    This function sends a request to the broker under the \
    :data:`DB_GET_PROCESSED_DATA_POINTS_COUNT_SUBJECT <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_POINTS_COUNT_SUBJECT>` \
    for the processed datapoints count in the database utilizing the \
    :func:`request_replysubject_thing_wrapper <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper>`

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: list[dict]

    :param timeout: Seconds to wait for a response
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    return await request_replysubject_thing_wrapper(
        fiot_service=fiot_service,
        data={},
        subject=_GET_PROCESSED_DATA_COUNT_SUBJECT_NAME,  # same as the string "get-all-raw-datapoints"
        timeout=timeout,  # default is 10
    )


async def request_get_processed_data_points_page(fiot_service: FastIoTService, page: int = 0, page_size: int = 10,
                                                 timeout: float = 10) -> Future[list[dict]]:
    """
    This function sends a request to the broker under the \
    :data:`DB_GET_PROCESSED_DATA_PAGE_SUBJECT <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_PAGE_SUBJECT>` \
    for a page of processed datapoints in the database utilizing the \
    :func:`request_replysubject_thing_wrapper <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper>`

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: list[dict]

    :param timeout: Seconds to wait for a response
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    return await request_replysubject_thing_wrapper(
        fiot_service=fiot_service,
        data={
            "page": page,
            "page_size": page_size,
        },
        subject=_GET_PROCESSED_DATA_PAGE_SUBJECT_NAME,  # same as the string "get-all-raw-datapoints"
        timeout=timeout,  # default is 10
    )


async def request_get_processed_data_points_from_raw_data(fiot_service: FastIoTService, data: dict,
                                                          timeout: float = 10) -> Future[list[dict]]:
    """
    This function sends a request to the broker under the \
    :data:`DATA_PROCESSING_PROCESS_RAW_DATA_SUBJECT <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DATA_PROCESSING_PROCESS_RAW_DATA_SUBJECT>` \
    for a set of raw data to be processed and handed back to \
    the requesting service utilizing the \
    :func:`request_replysubject_thing_wrapper <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper>`

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: list[dict]

    :param timeout: Seconds to wait for a response
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    return await request_replysubject_thing_wrapper(
        fiot_service=fiot_service,
        data=data,
        subject=_PROCESS_RAW_DATA_SUBJECT_NAME,  # same as the string "get-all-raw-datapoints"
        timeout=timeout,  # default is 10
    )


async def request_get_prediction(fiot_service: FastIoTService, data: dict,
                                 timeout: float = 10) -> Future[list[dict]]:
    """
    This function sends a request to the broker under the \
    :data:`ML_SERVING_SUBJECT <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.ML_SERVING_SUBJECT>` \
    for a prediction utilizing the \
    :func:`request_replysubject_thing_wrapper <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper>`

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: list[dict]

    :param timeout: Seconds to wait for a response
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    return await request_replysubject_thing_wrapper(
        fiot_service=fiot_service,
        data=data,
        subject=_PREDICT_SUBJECT_NAME,  # same as the string "get-all-raw-datapoints"
        timeout=timeout,  # default is 10
    )


async def request_get_labeled_dataset(fiot_service: FastIoTService, data: dict = {},
                                      timeout: float = 10) -> Future[list[dict]]:
    """
    This function sends a request to the broker under the \
    :data:`DB_GET_LABELED_DATASET_SUBJECT <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_LABELED_DATASET_SUBJECT>` \
    for a labeled dataset from the database utilizing the \
    :func:`request_replysubject_thing_wrapper <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper>`

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: list[dict]

    :param timeout: Seconds to wait for a response
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    return await request_replysubject_thing_wrapper(
        fiot_service=fiot_service,
        data=data,
        subject=_GET_LABELED_DATASET_SUBJECT_NAME,  # same as the string "get-all-raw-datapoints"
        timeout=timeout,  # default is 10
    )


async def request_edc_prediction(fiot_service: FastIoTService, data: list[dict],
                                 timeout: float = 10) -> Future[list[dict]]:
    """
    This function sends a request to the broker under the \
    :data:`ML_EDC_SUBJECT <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.ML_EDC_SUBJECT>` \
    for an EDC prediction utilizing the \
    :func:`request_replysubject_thing_wrapper <anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper>`

    :param fiot_service: The FastIoTService instance that is used to send the request.
    :type fiot_service: FastIoTService

    :param data: The data to be sent to the broker.
    :type data: list[dict]

    :param timeout: Seconds to wait for a response
    :type timeout: float

    :return: Future placeholder for the awaited Reply
    :rtype: Future[dict | list[dict] | int | float | str | None]
    """
    return await request_replysubject_thing_wrapper(
        fiot_service=fiot_service,
        data=data,
        subject=_PREDICT_EDC_SUBJECT_NAME,  # same as the string "get-all-raw-datapoints"
        timeout=timeout,  # default is 10
    )

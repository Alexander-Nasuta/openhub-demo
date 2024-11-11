from fastiot.core import ReplySubject
from fastiot.msg import Thing


_GET_LABELED_DATASET_SUBJECT_NAME = "get-labeled-dataset"
DB_GET_LABELED_DATASET_SUBJECT = ReplySubject(name=_GET_LABELED_DATASET_SUBJECT_NAME, msg_cls=Thing, reply_cls=Thing)

_SAVE_MANY_RAW_DATA_SUBJECT_NAME = "save-many-raw-datapoints"
DB_SAVE_MANY_RAW_DATAPOINTS_SUBJECT = ReplySubject(name=_SAVE_MANY_RAW_DATA_SUBJECT_NAME, msg_cls=Thing, reply_cls=Thing)

_GET_ALL_RAW_DATA_SUBJECT_NAME = "get-all-raw-datapoints"
DB_GET_ALL_RAW_DATA_SUBJECT = ReplySubject(name=_GET_ALL_RAW_DATA_SUBJECT_NAME, msg_cls=Thing, reply_cls=Thing)

_GET_ALL_PROCESSED_DATA_SUBJECT_NAME = "get-all-processed-datapoints"
DB_GET_ALL_PROCESSED_DATA_SUBJECT = ReplySubject(name=_GET_ALL_PROCESSED_DATA_SUBJECT_NAME, msg_cls=Thing, reply_cls=Thing)

_GET_PROCESSED_DATA_POINTS_COUNT = "get-processed-datapoints-count"
DB_GET_PROCESSED_DATA_POINTS_COUNT_SUBJECT = ReplySubject(name=_GET_PROCESSED_DATA_POINTS_COUNT, msg_cls=Thing, reply_cls=Thing)

_UPSERT_MANY_PROCESSED_DATA_SUBJECT_NAME = "upsert-many-processed-datapoints"
DB_UPSERT_MANY_PROCESSED_DATAPOINTS_SUBJECT = ReplySubject(name=_UPSERT_MANY_PROCESSED_DATA_SUBJECT_NAME, msg_cls=Thing, reply_cls=Thing)

# Pagination for datasets for ml

_GET_PROCESSED_DATA_COUNT_SUBJECT_NAME = "get-processed-data-count"
DB_GET_PROCESSED_DATA_COUNT_SUBJECT = ReplySubject(name=_GET_PROCESSED_DATA_COUNT_SUBJECT_NAME, msg_cls=Thing, reply_cls=Thing)

_GET_PROCESSED_DATA_PAGE_SUBJECT_NAME = "get-processed-data-page"
DB_GET_PROCESSED_DATA_PAGE_SUBJECT = ReplySubject(name=_GET_PROCESSED_DATA_PAGE_SUBJECT_NAME, msg_cls=Thing, reply_cls=Thing)

# Process raw datapoints
_PROCESS_RAW_DATA_SUBJECT_NAME = "process-raw-datapoints"
DATA_PROCESSING_PROCESS_RAW_DATA_SUBJECT = ReplySubject(name=_PROCESS_RAW_DATA_SUBJECT_NAME, msg_cls=Thing, reply_cls=Thing)

# Predict with model
_PREDICT_SUBJECT_NAME = "get-prediction"
ML_SERVING_SUBJECT = ReplySubject(name=_PREDICT_SUBJECT_NAME, msg_cls=Thing, reply_cls=Thing)


_GET_EDC_LABELED_DATASET_SUBJECT_NAME = "get-edc-labeled-dataset"
DB_GET_EDC_LABELED_DATASET_SUBJECT = ReplySubject(name=_GET_EDC_LABELED_DATASET_SUBJECT_NAME, msg_cls=Thing, reply_cls=Thing)

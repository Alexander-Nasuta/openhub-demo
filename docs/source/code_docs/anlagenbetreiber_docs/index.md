# Machine Operator

This documentation provides an overview of the Machine Operator (german: Anlagenbetreiber) module.

## Services
This section provides an overview of the services available in the Anlagenbetreiber (Machine Operator) module. Each service is responsible for a specific functionality within the FastIoT ecosystem.

### MotivSensorService
```{eval-rst}
.. autoclass:: motiv_sensor.motiv_sensor_service.MotivSensorService
    :show-inheritance:
    :members:
```

### MongoDatabaseService
```{eval-rst}
.. autoclass:: mongo_database.mongo_database_service.MongoDatabaseService
    :show-inheritance:
    :members:
```

### EdcAnlagenbetreiberService
```{eval-rst}
.. autoclass:: edc_anlagenbetreiber.edc_anlagenbetreiber_service.EdcAnlagenbetreiberService
    :show-inheritance:
    :members:
```

### MachinenParametrierungService
```{eval-rst}
.. autoclass:: machinen_parametrierung.machinen_parametrierung_service.MachinenParametrierungService
    :show-inheritance:
    :members:
```




## Broker Facade

The following functions are used to interact with the ML Lifecycle Broker. They provide a simple interface to send requests and receive responses from the broker.
They are located in the `anlagenbetreiber/ml_lifecycle_utils/ml_lifecycle_broker_facade.py` file.

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.ok_response_thing
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.error_response_thing
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_save_many_raw_data_points
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_upsert_many_processed_data_points
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_all_raw_data_points
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_all_processed_data_points
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_processed_data_points_count
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_processed_data_points_page
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_processed_data_points_from_raw_data
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_prediction
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_labeled_dataset
```

```{eval-rst}
.. autofunction:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_edc_prediction
```

## Broker Lifecycle Topics

```{eval-rst}
.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_LABELED_DATASET_SUBJECT

.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_SAVE_MANY_RAW_DATAPOINTS_SUBJECT

.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_ALL_RAW_DATA_SUBJECT

.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_ALL_PROCESSED_DATA_SUBJECT

.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_POINTS_COUNT_SUBJECT

.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_UPSERT_MANY_PROCESSED_DATAPOINTS_SUBJECT

.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_COUNT_SUBJECT

.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_PAGE_SUBJECT

.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.DATA_PROCESSING_PROCESS_RAW_DATA_SUBJECT

.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.ML_SERVING_SUBJECT

.. autodata:: anlagenbetreiber.ml_lifecycle_utils.ml_lifecycle_subjects_name.ML_EDC_SUBJECT

```

## Dataset 

Contains the inital dataset in a list of dictionaries.
```{eval-rst}
.. literalinclude:: ../../../../anlagenbetreiber/src/anlagenbetreiber/dataset/inital_annotated_dataset.py
   :language: python
   :linenos:

```

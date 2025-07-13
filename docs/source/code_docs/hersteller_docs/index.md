# Machine Manufacturer 
This documentation provides an overview of the Machine Manufacturer (german: Hersteller) module within the FastIoT ecosystem.

## Services
This section provides an overview of the services available in the Hersteller (Manufacturer) module. Each service is responsible for a specific functionality within the FastIoT ecosystem.

### EdcHerstellerService 
```{eval-rst}
.. autoclass:: edc_hersteller.edc_hersteller_service.EdcHerstellerService
    :show-inheritance:
    :members:
```

### MlServingService
```{eval-rst}
.. autoclass:: ml_serving.ml_serving_service.MlServingService
    :show-inheritance:
    :members:
```

## Broker Facade

```{eval-rst}
.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.ok_response_thing

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.error_response_thing

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_save_many_raw_data_points

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_upsert_many_processed_data_points

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_all_raw_data_points

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_all_processed_data_points

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_processed_data_points_count

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_processed_data_points_page

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_processed_data_points_from_raw_data

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_prediction

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_labeled_dataset

.. autofunction:: hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_edc_labeled_dataset
```


## Broker Lifecycle Topics

```{eval-rst}
.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_LABELED_DATASET_SUBJECT

.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_SAVE_MANY_RAW_DATAPOINTS_SUBJECT

.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_ALL_RAW_DATA_SUBJECT

.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_ALL_PROCESSED_DATA_SUBJECT

.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_POINTS_COUNT_SUBJECT

.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_UPSERT_MANY_PROCESSED_DATAPOINTS_SUBJECT

.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_COUNT_SUBJECT

.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_PAGE_SUBJECT

.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.DATA_PROCESSING_PROCESS_RAW_DATA_SUBJECT

.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.ML_SERVING_SUBJECT

.. autodata:: hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_EDC_LABELED_DATASET_SUBJECT

```
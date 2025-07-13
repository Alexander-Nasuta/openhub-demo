# ML Service Provider
This documentation provides an overview of the ML Service Provider (german: Dienstleister ) module within the FastIoT ecosystem.
 
## Services
This section provides an overview of the services available in the Dienstleister (Service Provider) module. Each service is responsible for a specific functionality within the FastIoT ecosystem.

### DataProcessingService
```{eval-rst}
.. autoclass:: dienstleister_services.data_processing.data_processing_service.DataProcessingService
    :show-inheritance:
    :members:
```

### EdcDienstleisterService
```{eval-rst}
.. autofunction:: dienstleister_services.edc_dienstleister.edc_dienstleister_service.edc_fetch_dict_list
.. autoclass:: dienstleister_services.edc_dienstleister.edc_dienstleister_service.EdcDienstleisterService
    :show-inheritance:
    :members:
```

### MLTrainingService 
```{eval-rst}
.. autoclass:: dienstleister_services.ml_training.ml_training_service.MlTrainingService
    :show-inheritance:
    :members:
```

## Data Processing Utils
This section includes utility classes and functions used for data processing within the Dienstleister module. These utilities are designed to facilitate common data manipulation tasks such as column dropping, type setting, and encoding.

```{eval-rst}
.. autoclass :: dienstleister.data_processing.pipeline_operations.ColumnDropper
    :show-inheritance:
    :members: fit, transform

.. autoclass :: dienstleister.data_processing.pipeline_operations.ColumnTypeSetter
    :show-inheritance:
    :members: fit, transform

.. autoclass :: dienstleister.data_processing.pipeline_operations.OneHotEncodePd
    :show-inheritance:
    :members: fit, transform
    
.. autoclass :: dienstleister.data_processing.pipeline_operations.MultiOneHotEncodePd
    :show-inheritance:
    :members: fit, transform

.. autoclass :: dienstleister.data_processing.pipeline_operations.NormalizeCols
    :show-inheritance:
    :members: fit, transform
```


## ML Training Utils
This section provides utility classes and functions for machine learning training tasks, including dataset handling and neural network definitions.

```{eval-rst}
.. autoclass:: dienstleister.ml_training.pytorch_utils.MyDataset
    :show-inheritance:
    :members:
    :special-members: __getitem__, __len__

.. autoclass:: dienstleister.ml_training.pytorch_utils.DemonstratorNeuralNet
    :show-inheritance:
    :members:
```

## Broker Facade

```{eval-rst}
.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.ok_response_thing

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.error_response_thing

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_replysubject_thing_wrapper

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_save_many_raw_data_points

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_upsert_many_processed_data_points

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_all_raw_data_points

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_all_processed_data_points

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_processed_data_points_count

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_processed_data_points_page

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_processed_data_points_from_raw_data

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_prediction

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_labeled_dataset

.. autofunction:: dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade.request_get_edc_labeled_dataset
```

## Broker Lifecycle Topics

```{eval-rst}
.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_LABELED_DATASET_SUBJECT

.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_SAVE_MANY_RAW_DATAPOINTS_SUBJECT

.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_ALL_RAW_DATA_SUBJECT

.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_ALL_PROCESSED_DATA_SUBJECT

.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_POINTS_COUNT_SUBJECT

.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_UPSERT_MANY_PROCESSED_DATAPOINTS_SUBJECT

.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_COUNT_SUBJECT

.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_PROCESSED_DATA_PAGE_SUBJECT

.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.DATA_PROCESSING_PROCESS_RAW_DATA_SUBJECT

.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.ML_SERVING_SUBJECT

.. autodata:: dienstleister.ml_lifecycle_utils.ml_lifecycle_subjects_name.DB_GET_EDC_LABELED_DATASET_SUBJECT
```

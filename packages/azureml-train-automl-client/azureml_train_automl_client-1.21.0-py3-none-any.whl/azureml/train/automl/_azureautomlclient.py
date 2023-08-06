# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""AutoML object in charge of orchestrating various AutoML runs for predicting models."""
import json
import logging
import os
import os.path
import warnings
from typing import Any, cast, List, Optional, Dict, Union

from azureml._common._error_definition import AzureMLError
from azureml._common.exceptions import AzureMLException
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core import dataprep_utilities, dataset_utilities, package_utilities
from azureml.automl.core.shared import import_utilities, logging_utilities
from azureml.train.automl._experiment_drivers import driver_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternal,
    ExecutionFailure,
    InvalidArgumentType,
    InvalidArgumentWithSupportedValues,
    RuntimeModuleDependencyMissing,
    SnapshotLimitExceeded
)
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.exceptions import (
    AutoMLException,
    ClientException,
    ConfigException,
    ValidationException
)
from azureml.core import Experiment, Run
from azureml.core.compute_target import AbstractComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.exceptions import ServiceException as AzureMLServiceException, SnapshotException
from . import constants, _logging
from ._azure_experiment_state import AzureExperimentState
from ._local_managed_utils import local_managed
from ._constants_azureml import Properties
from .constants import Framework
from ._remote_console_interface import RemoteConsoleInterface
from .run import AutoMLRun
from .utilities import _InternalComputeTypes
from ._experiment_drivers.remote_experiment_driver import RemoteExperimentDriver

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)


class AzureAutoMLClient:
    """Client to run AutoML experiments on Azure Machine Learning platform."""

    def __init__(self, experiment_state: AzureExperimentState):
        """
        Create an AzureAutoMLClient.
        """
        self.experiment_state = experiment_state

        self._check_create_folders(self.experiment_state.automl_settings.path)

        if not self.experiment_state.automl_settings.show_warnings:
            # sklearn forces warnings, so we disable them here
            warnings.simplefilter("ignore", DeprecationWarning)
            warnings.simplefilter("ignore", RuntimeWarning)
            warnings.simplefilter("ignore", UserWarning)
            warnings.simplefilter("ignore", FutureWarning)

    def cancel(self):
        """
        Cancel the ongoing local run.

        :return: None
        """
        pass

    def fit(self,
            run_configuration: Optional[RunConfiguration] = None,
            compute_target: Optional[Union[AbstractComputeTarget, str]] = None,
            X: Optional[Any] = None,
            y: Optional[Any] = None,
            sample_weight: Optional[Any] = None,
            X_valid: Optional[Any] = None,
            y_valid: Optional[Any] = None,
            sample_weight_valid: Optional[Any] = None,
            cv_splits_indices: Optional[List[Any]] = None,
            show_output: bool = False,
            existing_run: bool = False,
            training_data: Optional[Any] = None,
            validation_data: Optional[Any] = None,
            test_data: Optional[Any] = None,
            _script_run: Optional[Run] = None,
            parent_run_id: Optional[Any] = None,
            is_managed: bool = False,
            kwargs: Optional[Dict[str, Any]] = None) -> AutoMLRun:
        """
        Start a new AutoML execution on the specified compute target.

        :param run_configuration: The run confiuguration used by AutoML, should contain a compute target for remote
        :type run_configuration: Azureml.core RunConfiguration
        :param compute_target: The AzureML compute node to run this experiment on
        :type compute_target: azureml.core.compute.AbstractComputeTarget
        :param X: Training features
        :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow or
                 azureml.core.Dataset, azureml.data.dataset_definition.DatasetDefinition
                 or azureml.data.TabularDataset
        :param y: Training labels
        :type y: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow or
                 azureml.core.Dataset, azureml.data.dataset_definition.DatasetDefinition
                 or azureml.data.TabularDataset
        :param sample_weight:
        :type sample_weight: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
                or azureml.data.TabularDataset
        :param X_valid: validation features
        :type X_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow or
                   azureml.core.Dataset, azureml.data.dataset_definition.DatasetDefinition
                   or azureml.data.TabularDataset
        :param y_valid: validation labels
        :type y_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow or
                   azureml.core.Dataset, azureml.data.dataset_definition.DatasetDefinition
                   or azureml.data.TabularDataset
        :param sample_weight_valid: validation set sample weights
        :type sample_weight_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
                or azureml.data.TabularDataset
        :param cv_splits_indices: Indices where to split training data for cross validation
        :type cv_splits_indices: list(int), or list(Dataflow) in which each Dataflow represent a train-valid set
                                 where 1 indicates record for training and 0 indicates record for validation
        :param show_output: Flag whether to print output to console
        :type show_output: bool
        :param existing_run: Flag whether this is a continuation of a previously completed experiment
        :type existing_run: bool
        :param _script_run: Run to associate with parent run id
        :type _script_run: azureml.core.Run
        :return: AutoML parent run
        :rtype: azureml.train.automl.AutoMLRun
        """
        # Save these params for local managed
        data_params = {
            'training_data': training_data,
            'validation_data': validation_data,
            'X': X,
            'y': y,
            'sample_weight': sample_weight,
            'X_valid': X_valid,
            'y_valid': y_valid,
            'sample_weight_valid': sample_weight_valid,
            'cv_splits_indices': cv_splits_indices}

        self.experiment_state.console_writer.show_output = show_output

        if run_configuration is None:
            run_configuration = RunConfiguration()
            if compute_target is not None:
                run_configuration.target = compute_target  # this will handle str or compute_target
                self.experiment_state.console_writer.println(
                    "No run_configuration provided, running on {0} with default configuration".format(
                        run_configuration.target
                    )
                )
            else:
                self.experiment_state.console_writer.println(
                    "No run_configuration provided, running locally with default configuration"
                )
            if run_configuration.target != "local":
                run_configuration.environment.docker.enabled = True
        if run_configuration.framework.lower() not in list(Framework.FULL_SET):
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentWithSupportedValues, target="run_configuration",
                    arguments=run_configuration.framework,
                    supported_values=list(Framework.FULL_SET)
                )
            )

        self.experiment_state.automl_settings.compute_target = run_configuration.target

        self.experiment_state.automl_settings.azure_service = _InternalComputeTypes.identify_compute_type(
            compute_target=self.experiment_state.automl_settings.compute_target,
            azure_service=self.experiment_state.automl_settings.azure_service,
        )

        # Save the Dataset to Workspace so that its saved id will be logged for telemetry and lineage
        dataset_utilities.ensure_saved(
            self.experiment_state.experiment.workspace,
            X=X,
            y=y,
            sample_weight=sample_weight,
            X_valid=X_valid,
            y_valid=y_valid,
            sample_weight_valid=sample_weight_valid,
            training_data=training_data,
            validation_data=validation_data,
            test_data=test_data,
        )

        dataset_utilities.collect_usage_telemetry(
            compute=run_configuration.target,
            spark_context=self.experiment_state.automl_settings.spark_context,
            X=X,
            y=y,
            sample_weight=sample_weight,
            X_valid=X_valid,
            y_valid=y_valid,
            sample_weight_valid=sample_weight_valid,
            training_data=training_data,
            validation_data=validation_data,
            test_data=test_data,
        )

        X, y, sample_weight, X_valid, y_valid, sample_weight_valid = dataset_utilities.convert_inputs(
            X, y, sample_weight, X_valid,
            y_valid, sample_weight_valid
        )

        training_data, validation_data, test_data = dataset_utilities.convert_inputs_dataset(
            training_data,
            validation_data,
            test_data
        )

        try:
            if self.experiment_state.automl_settings.spark_context:
                try:
                    from azureml.train.automl.runtime._experiment_drivers.spark_experiment_driver import \
                        SparkExperimentDriver

                    spark_exp_driver = SparkExperimentDriver(self.experiment_state)
                    spark_exp_driver.start(
                        run_configuration=run_configuration,
                        X=X,
                        y=y,
                        sample_weight=sample_weight,
                        X_valid=X_valid,
                        y_valid=y_valid,
                        sample_weight_valid=sample_weight_valid,
                        cv_splits_indices=cv_splits_indices,
                        training_data=training_data,
                        validation_data=validation_data)
                except Exception:
                    raise
            elif is_managed:
                self.experiment_state.current_run = local_managed(
                    self.experiment_state.experiment,
                    run_configuration,
                    self.experiment_state.automl_settings,
                    data_params,
                    show_output,
                )
            elif run_configuration.target == "local":
                name = run_configuration._name if run_configuration._name else "local"
                run_configuration.save(self.experiment_state.automl_settings.path, name)
                self.experiment_state.console_writer.println("Running on local machine")
                if not show_output:
                    logging.warning('Running on local machine. Note that local runs always run synchronously '
                                    'even if you use the parameter \'show_output=False\'')

                driver_utilities.check_package_compatibilities(
                    self.experiment_state, is_managed_run=_script_run is not None)
                try:
                    from azureml.train.automl.runtime import _runtime_client
                except ImportError as e:
                    raise ConfigException._with_error(
                        AzureMLError.create(
                            RuntimeModuleDependencyMissing, target="compute_target", module_name=e.name),
                        inner_exception=e
                    ) from e

                runtime_client = _runtime_client.RuntimeClient(self.experiment_state)

                runtime_client._fit_local(
                    X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid,
                    cv_splits_indices=cv_splits_indices,
                    existing_run=existing_run, sample_weight_valid=sample_weight_valid,
                    training_data=training_data, validation_data=validation_data, _script_run=_script_run,
                    parent_run_id=parent_run_id)
            else:
                self.experiment_state.console_writer.println(
                    "Running on remote compute: " + str(run_configuration.target)
                )
                self.experiment_state.automl_settings.debug_log = "azureml_automl.log"
                remote_experiment_driver = RemoteExperimentDriver(self.experiment_state)
                remote_experiment_driver.start(
                    run_configuration=run_configuration,
                    X=X,
                    y=y,
                    sample_weight=sample_weight,
                    X_valid=X_valid,
                    y_valid=y_valid,
                    sample_weight_valid=sample_weight_valid,
                    cv_splits_indices=cv_splits_indices,
                    training_data=training_data,
                    validation_data=validation_data,
                    test_data=test_data,
                )
        except Exception as e:
            driver_utilities.fail_parent_run(self.experiment_state,
                                             error_details=e, is_aml_compute=run_configuration.target != "local")
            raise
        assert self.experiment_state.current_run is not None
        return self.experiment_state.current_run

    def _create_parent_run_for_local_managed(
            self, data_params: Dict[str, Any], parent_run_id: Optional[Any] = None) -> AutoMLRun:
        """
        Create parent run in Run History containing AutoML experiment information for a local docker or conda run.
        Local managed runs will go through typical _create_parent_run_for_local workflow which will do the validation
        steps.

        :return: AutoML parent run
        :rtype: azureml.train.automl.AutoMLRun
        """
        parent_run_dto = driver_utilities.create_and_validate_parent_run_dto(
            self.experiment_state, target=constants.ComputeTargets.LOCAL, parent_run_id=parent_run_id, **data_params
        )

        try:
            logger.info("Start creating parent run")
            self.experiment_state.parent_run_id = self.experiment_state.jasmine_client.post_parent_run(parent_run_dto)

            Contract.assert_value(self.experiment_state.parent_run_id, "parent_run_id")

            logger.info("Successfully created a parent run with ID: {}".format(self.experiment_state.parent_run_id))

            _logging.set_run_custom_dimensions(
                automl_settings=self.experiment_state.automl_settings,
                parent_run_id=self.experiment_state.parent_run_id,
                child_run_id=None,
            )
        except (AutoMLException, AzureMLException, AzureMLServiceException):
            raise
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            raise ClientException.from_exception(e, target="_create_parent_run_for_local_managed").with_generic_msg(
                "Error when trying to create parent run in automl service."
            )

        logger.info("Setting Run {} status to: {}".format(
            str(self.experiment_state.parent_run_id), constants.RunState.PREPARE_RUN))
        self.experiment_state.jasmine_client.set_parent_run_status(
            self.experiment_state.parent_run_id, constants.RunState.PREPARE_RUN
        )

        self.experiment_state.current_run = AutoMLRun(
            self.experiment_state.experiment, self.experiment_state.parent_run_id)

        return self.experiment_state.current_run

    def _check_create_folders(self, path):
        if path is None:
            path = os.getcwd()
        # Expand out the path because os.makedirs can't handle '..' properly
        aml_config_path = os.path.abspath(os.path.join(path, '.azureml'))
        os.makedirs(aml_config_path, exist_ok=True)

    @staticmethod
    def _is_tensorflow_module_present():
        try:
            from azureml.automl.runtime.shared import pipeline_spec
            return pipeline_spec.tf_wrappers.tf_found
        except Exception:
            return False

    @staticmethod
    def _is_xgboost_module_present():
        try:
            from azureml.automl.runtime.shared import model_wrappers
            return model_wrappers.xgboost_present
        except Exception:
            return False

    @staticmethod
    def _is_fbprophet_module_present():
        fbprophet = import_utilities.import_fbprophet(raise_on_fail=False)
        return fbprophet is not None

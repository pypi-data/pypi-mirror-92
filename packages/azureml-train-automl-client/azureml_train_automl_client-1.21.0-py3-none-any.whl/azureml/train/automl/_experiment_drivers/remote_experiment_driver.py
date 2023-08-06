# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, cast, Dict, List, Optional, Union
import logging

from azureml.core import Run
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core._run.types import RunType
from azureml.core.runconfig import RunConfiguration
from azureml.automl.core._experiment_drivers.base_experiment_driver import BaseExperimentDriver
from .._azure_experiment_state import AzureExperimentState
from .._remote_console_interface import RemoteConsoleInterface
from . import driver_utilities
from ..run import AutoMLRun


logger = logging.getLogger(__name__)


class RemoteExperimentDriver(BaseExperimentDriver):
    def __init__(self,
                 experiment_state: AzureExperimentState) -> None:
        self.experiment_state = experiment_state

    def start(
            self,
            run_configuration: Optional[RunConfiguration] = None,
            X: Optional[Any] = None,
            y: Optional[Any] = None,
            sample_weight: Optional[Any] = None,
            X_valid: Optional[Any] = None,
            y_valid: Optional[Any] = None,
            sample_weight_valid: Optional[Any] = None,
            cv_splits_indices: Optional[List[Any]] = None,
            existing_run: bool = False,
            training_data: Optional[Any] = None,
            validation_data: Optional[Any] = None,
            test_data: Optional[Any] = None,
            _script_run: Optional[Run] = None,
            parent_run_id: Optional[Any] = None,
            kwargs: Optional[Dict[str, Any]] = None
    ) -> RunType:
        driver_utilities.fit_remote_core(
            self.experiment_state,
            run_configuration, X=X, y=y, sample_weight=sample_weight, X_valid=X_valid,
            y_valid=y_valid, sample_weight_valid=sample_weight_valid,
            cv_splits_indices=cv_splits_indices, training_data=training_data,
            validation_data=validation_data, test_data=test_data)

        if self.experiment_state.console_writer.show_output:
            RemoteConsoleInterface._show_output(
                cast(AutoMLRun, self.experiment_state.current_run),
                self.experiment_state.console_writer,
                logger,
                self.experiment_state.automl_settings.primary_metric,
            )

        assert self.experiment_state.current_run
        return self.experiment_state.current_run

    def cancel(self):
        run_lifecycle_utilities.cancel_run()

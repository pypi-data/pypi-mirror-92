# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, List, Optional, Union

from azureml.core import Run
from azureml.core.runconfig import RunConfiguration
from azureml.automl.core._run.types import RunType
from azureml.automl.core._experiment_drivers.base_experiment_driver import BaseExperimentDriver
from azureml.train.automl._azure_experiment_state import AzureExperimentState
from azureml.train.automl.runtime._runtime_client import RuntimeClient


class LocalExperimentDriver(BaseExperimentDriver):
    def __init__(self,
                 experiment_state: AzureExperimentState) -> None:
        self.experiment_state = experiment_state

        self._runtime_client = None     # type: Optional[RuntimeClient]

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
        self._runtime_client = RuntimeClient(self.experiment_state)

        self._runtime_client._fit_local(
            X=X, y=y, sample_weight=sample_weight, X_valid=X_valid, y_valid=y_valid,
            cv_splits_indices=cv_splits_indices,
            existing_run=existing_run, sample_weight_valid=sample_weight_valid,
            training_data=training_data, validation_data=validation_data, _script_run=_script_run,
            parent_run_id=parent_run_id)

        assert self.experiment_state.current_run
        return self.experiment_state.current_run

    def cancel(self):
        if self._runtime_client:
            self._runtime_client.cancel()

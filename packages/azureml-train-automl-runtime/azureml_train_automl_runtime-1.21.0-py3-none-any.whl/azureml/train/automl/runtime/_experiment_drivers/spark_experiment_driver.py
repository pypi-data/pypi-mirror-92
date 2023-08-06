# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, List, Optional, Union
import logging
import json

from azureml.core import Run
from azureml.core.runconfig import RunConfiguration
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core._run.types import RunType
from azureml.automl.core import dataprep_utilities, dataset_utilities
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core._experiment_drivers.base_experiment_driver import BaseExperimentDriver
from azureml.train.automl._azure_experiment_state import AzureExperimentState
from azureml.train.automl.runtime._entrypoints import spark_worker_node_entrypoint
from azureml.train.automl.automl_adb_run import AutoMLADBRun
from azureml.train.automl._remote_console_interface import RemoteConsoleInterface
from azureml._restclient.service_context import ServiceContext
from azureml.train.automl._experiment_drivers import driver_utilities
from .._adb_driver_node import _AdbDriverNode


logger = logging.getLogger(__name__)


class SparkExperimentDriver(BaseExperimentDriver):
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
        self._init_adb_driver_run(
            run_configuration,
            X,
            y,
            sample_weight,
            X_valid,
            y_valid,
            sample_weight_valid,
            cv_splits_indices,
            training_data,
            validation_data,
            existing_run
        )
        assert self.experiment_state.current_run
        return self.experiment_state.current_run

    def cancel(self):
        run_lifecycle_utilities.cancel_run()

    def _init_adb_driver_run(
            self,
            run_configuration=None,
            X=None,
            y=None,
            sample_weight=None,
            X_valid=None,
            y_valid=None,
            sample_weight_valid=None,
            cv_splits_indices=None,
            training_data=None,
            validation_data=None,
            show_output=False,
            existing_run=False,
    ):

        self.experiment_state.console_writer.println(
            "Running an experiment on spark cluster: {0}.\n".format(self.experiment_state.experiment.name)
        )

        driver_utilities.check_package_compatibilities(self.experiment_state, is_managed_run=False)

        try:
            if not existing_run:
                driver_utilities.fit_remote_core(
                    self.experiment_state,
                    run_configuration,
                    X=X,
                    y=y,
                    sample_weight=sample_weight,
                    X_valid=X_valid,
                    y_valid=y_valid,
                    sample_weight_valid=sample_weight_valid,
                    cv_splits_indices=cv_splits_indices,
                    training_data=training_data,
                    validation_data=validation_data,
                )
            # This should be refactored to have RunHistoryClient and make call on it to get token
            # use Experiment object to get name and other parameters
            token_res = self.experiment_state.experiment_client._client.run.get_token(
                experiment_name=self.experiment_state.experiment.name,
                resource_group_name=self.experiment_state.experiment.workspace.resource_group,
                subscription_id=self.experiment_state.experiment.workspace.subscription_id,
                workspace_name=self.experiment_state.experiment.workspace.name,
                run_id=self.experiment_state.current_run.run_id,
            )
            aml_token = token_res.token
            aml_token_expiry = token_res.expiry_time_utc

            service_context = ServiceContext(
                subscription_id=self.experiment_state.experiment.workspace.subscription_id,
                resource_group_name=self.experiment_state.experiment.workspace.resource_group,
                workspace_name=self.experiment_state.experiment.workspace.name,
                workspace_id=self.experiment_state.experiment.workspace._workspace_id,
                workspace_discovery_url=self.experiment_state.experiment.workspace.discovery_url,
                authentication=self.experiment_state.experiment.workspace._auth_object,
            )

            run_history_url = service_context._get_run_history_url()
            fn_script = None
            if self.experiment_state.automl_settings.data_script:
                with open(self.experiment_state.automl_settings.data_script, "r") as f:
                    fn_script = f.read()

            if training_data is None and validation_data is None:
                dataprep_json = dataprep_utilities.get_dataprep_json(
                    X=X,
                    y=y,
                    sample_weight=sample_weight,
                    X_valid=X_valid,
                    y_valid=y_valid,
                    sample_weight_valid=sample_weight_valid,
                    cv_splits_indices=cv_splits_indices,
                )
            else:
                dataprep_json = dataprep_utilities.get_dataprep_json_dataset(
                    training_data=training_data, validation_data=validation_data
                )

            # Remove path when creating the DTO
            settings_dict = self.experiment_state.automl_settings.as_serializable_dict()
            settings_dict["path"] = None

            # build dictionary of context
            run_context = {
                "subscription_id": self.experiment_state.experiment.workspace.subscription_id,
                "resource_group": self.experiment_state.experiment.workspace.resource_group,
                "location": self.experiment_state.experiment.workspace.location,
                "workspace_name": self.experiment_state.experiment.workspace.name,
                "experiment_name": self.experiment_state.experiment.name,
                "experiment_id": self.experiment_state.experiment.id,
                "parent_run_id": self.experiment_state.current_run.run_id,
                "aml_token": aml_token,
                "aml_token_expiry": aml_token_expiry,
                "service_url": run_history_url,
                "discovery_url": service_context._get_discovery_url(),
                "automl_settings_str": json.dumps(settings_dict),
                "dataprep_json": dataprep_json,
                "get_data_content": fn_script,
            }
            adb_automl_context = [
                (index, run_context)
                for index in range(0, self.experiment_state.automl_settings.max_concurrent_iterations)
            ]

            if not hasattr(self.experiment_state.automl_settings, "is_run_from_test"):
                adb_thread = _AdbDriverNode(
                    "AutoML on Spark Experiment: {0}".format(self.experiment_state.experiment.name),
                    adb_automl_context,
                    self.experiment_state.automl_settings.spark_context,
                    self.experiment_state.automl_settings.max_concurrent_iterations,
                    self.experiment_state.current_run.run_id,
                )
                adb_thread.start()
                self.experiment_state.current_run = AutoMLADBRun(
                    self.experiment_state.experiment, self.experiment_state.parent_run_id, adb_thread
                )
            else:
                automlRDD = self.experiment_state.automl_settings. \
                    spark_context.parallelize(adb_automl_context,
                                              self.experiment_state.automl_settings.max_concurrent_iterations)
                automlRDD.map(spark_worker_node_entrypoint.adb_run_experiment).collect()

            if show_output:
                RemoteConsoleInterface._show_output(
                    self.experiment_state.current_run,
                    self.experiment_state.console_writer,
                    logger,
                    self.experiment_state.automl_settings.primary_metric,
                )
        except Exception as ex:
            logging_utilities.log_traceback(ex, logger)
            raise

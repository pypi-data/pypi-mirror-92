# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base class for various experiment drivers."""
from typing import Any, Dict, List, Optional, Union
from abc import abstractmethod

from azureml.core import Run
from azureml.core.runconfig import RunConfiguration
from azureml.automl.core._run.types import RunType


class BaseExperimentDriver:

    @abstractmethod
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
        raise NotImplementedError()

    @abstractmethod
    def cancel(self):
        raise NotImplementedError()

# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Principles of MLEngine
1) Composable set of APIs that define the various stages of a machine learning experiment
2) APIs are azure service and azureML SDK independent - (except for AzureML dataset package)
3) APIs are ML package concept independent - ie they should NOT project the concepts from ML packages directly
4) APIs are distributed infra independent - APIs hide distributed-infra used however are take "distributed/not" flag
5) APIs are AutoML concept and automl workflow independent - ie they need to work beyond AutoML context
6) APIs params are explicit - ie they explicitly accept params it expects and wont depend on external state, storage
7) APIs are friendly to AML pipelining - ie we expect these APIs to be orchestratable using AML pipelines

Terminology
1) Pipeline: Assembled set of featurizer(s) and trainer. It is a pre training concept.
2) Model: The thing that comes out of fitting/training. It is a post training concept.
        FeaturizedModel: The thing that comes out fitting a featurizers. Can transform but cant predict.
        ClassificationModel/RegressionModel/ForecastingModel: Can transform(optionally) and predict/forecast.
3) Algorithm: Captures the logic used to train - such as LightGBM or LinearRegressor


Pending APIs
1) prepare
2) detect column_purpose
3) featurizer_fit
4) featurizer_transform
5) predict
6) predict_proba
7) ensemble
8) explain
9) convert_to_onnx
10) forecast
11) evaluate_forecaster
12) evaluate_regressor

"""

import logging
from typing import Dict, Optional, Any, Union, List, Tuple

import numpy as np
import pandas as pd
from scipy import sparse
from skl2onnx.proto import onnx_proto  # noqa: E402
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline

from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.runtime._data_definition import RawExperimentData
from azureml.automl.runtime._ml_engine.validation import RawExperimentDataValidator
from azureml.automl.runtime.featurization import AutoMLTransformer
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.shared.types import DataInputType


def validate(raw_experiment_data: RawExperimentData, automl_settings: AutoMLBaseSettings) -> None:
    """
    Checks whether data is ready for a Classification / Regression machine learning task

    :param raw_experiment_data: Object which provides access to the training (and/or validation) dataset(s).
    :param automl_settings: The settings for the experiment.
    :return: None
    """
    experiment_data_validator = RawExperimentDataValidator(automl_settings)
    experiment_data_validator.validate(raw_experiment_data)


def featurize(
        x: DataInputType, y: DataInputType, transformer: AutoMLTransformer
) -> Union[pd.DataFrame, np.ndarray, sparse.spmatrix]:
    """
    Featurize the data so it could be used for final model training

    :param x: The data to transform.
    :param y: The target column to predict.
    :param transformer: The transformer to use to featurize the dataset
    :return:
    """
    return transformer.fit_transform(x, y)


def convert_to_onnx(
    trained_model: Pipeline,
    metadata_dict: Optional[Dict[str, Any]],
    enable_split_onnx_models: bool = False,
    model_name: str = '',
    model_desc: Optional[Dict[Any, Any]] = None,
) -> Tuple[Optional[onnx_proto.ModelProto],
           Optional[onnx_proto.ModelProto],
           Optional[onnx_proto.ModelProto],
           Dict[Any, Any],
           Optional[Dict[str, Any]]]:
    """
    Convert a regular model to an ONNX model

    :param trained_model: A trained model returned by the "train" method.
    :param metadata_dict: Metadata of the training data returned by the "get_onnx_metadata" method.
    :param enable_split_onnx_models: Enables returns of separate model for the featurizer and estimator.
    :param model_name: The ONNX model name.
    :param model_desc: The ONNX model description.

    :return: A tuple containing:
                 The ONNX model for the whole pipeline
                 Optionally the ONNX model for the featurizer.
                 Optionally the ONNX model for the estimator
    """
    onnx_cvt = OnnxConverter(is_onnx_compatible=True,
                             enable_split_onnx_featurizer_estimator_models=enable_split_onnx_models)

    onnx_cvt.initialize_with_metadata(metadata_dict=metadata_dict)

    onnx_model, featurizer_onnx_model, estimator_onnx_model, err = \
        onnx_cvt.convert(trained_model, model_name, model_desc)

    model_resource = onnx_cvt.get_converted_onnx_model_resource()

    return onnx_model, featurizer_onnx_model, estimator_onnx_model, model_resource, err

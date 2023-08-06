from freelpipe.steps.compute import SparkJobStep, ShortComputeTask
from freelpipe.steps.ml import MLTrainingJob, MLModel, MLEndpointConfig, MLEndpoint, MLProcessingJob


class BuildStates():
    
    SPARK_JOB_STEP = ("SparkJobStep", SparkJobStep)
    SHORT_COMPUTE_TASK = ("ShortComputeTask", ShortComputeTask)
    ML_TRAINING_JOB = ("MLTrainingJob", MLTrainingJob)
    ML_MODEL = ("MLModel", MLModel)
    ML_ENDPOINT_CONFIG = ("MLEndpointConfig", MLEndpointConfig)
    ML_ENDPOINT = ("MLEndpoint", MLEndpoint)
    ML_PROCESSING_JOB = ("MLProcessingJob", MLProcessingJob)
    
    @classmethod
    def get_classes(cls):
        return [SparkJobStep, ShortComputeTask, MLTrainingJob, MLModel, MLEndpointConfig, MLEndpoint, MLProcessingJob]
    
    @classmethod
    def get_name(cls):
        return ["SparkJobStep", "ShortComputeTask", "MLTrainingJob", "MLModel", "MLEndpointConfig", "MLEndpoint", "MLProcessingJob"]

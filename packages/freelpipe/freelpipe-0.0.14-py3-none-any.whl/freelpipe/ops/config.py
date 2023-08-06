import boto3
from botocore.config import Config
import yaml
import os
from freelpipe.steps import BuildStates
import uuid

class MLConfig():
    
    AWS_SERVICES = ["s3", "lambda", "glue", "sagemaker"]
    
    def __init__(self, project, version="dev", version_number=0, config_location=None, aws_account_id=None, aws_region=None, artifact_bucket=None, aws_client_configs=Config()):
        
        self.aws_account_id = aws_account_id
        self.aws_region = aws_region
        self.artifact_bucket = artifact_bucket
        self.project = os.environ.get("REPO_NAME", project).replace("_", "-")
        self.version = os.environ.get("BRANCH_NAME", version)
        self.version_number = os.environ.get('BUILD_NUMBER', version_number)
        
        variables = self._load_config(config_location, aws_client_configs)
        self.config = self._extract_env_variables(variables, version)
        self.account = self._account_config()
        self.aws_clients = self._aws_clients(aws_client_configs)
    
        self.service_configs = {
            BuildStates.SPARK_JOB_STEP[1]: self._spark_job_config(),
            BuildStates.SHORT_COMPUTE_TASK[1]: self._short_compute_config(),
            BuildStates.ML_TRAINING_JOB[1]: self._ml_training_config(),
            BuildStates.ML_ENDPOINT_CONFIG[1]: self._ml_endpoint_config(),
        }
        self.estimator_config = self._estimator_config()
    
        
    def _load_config(self, config_location, aws_client_configs):
        config_location = os.environ.get("FREELPIPE_CONFIG_LOCATION", config_location)
        if config_location is None:
            return {}
        if self._is_s3_file(config_location):
            config_location = self._download_file(config_location, aws_client_configs=aws_client_configs)
        if not os.path.exists(config_location) or not os.path.isfile(config_location):
            raise FileNotFoundError(f"{config_location} is missing")
        with open(config_location, "r") as f:
            return yaml.safe_load(f)
        
    def _extract_env_variables(self, variables, env):
        if env not in variables and "_default" not in variables:
            return {}
        if env not in variables:
            return variables["_default"]
        return variables[env]
    
    def _download_file(self, config_location, s3_client=None, aws_client_configs=Config()):
        bucket = config_location.split("/")[2]
        key = "/".join(config_location.split("/")[3:])
        if s3_client is None:
            s3_client = self._get_client("s3", aws_client_configs)
        destination = "/tmp/"+uuid.uuid1().hex + key.split(".")[-1]
        s3_client.download_file(bucket, key, destination)
        return destination

    def _is_s3_file(self, filename):
        return filename.startswith("s3://")
    
    def _aws_clients(self, aws_client_configs):
        clients = {}
        creds = {}
        if self.account['DeploymentRoleArn']:
            creds = self._get_credentials(self.account['DeploymentRoleArn'], aws_client_configs)
        for service in self.AWS_SERVICES:
            clients[service] = self._get_client(service, aws_client_configs, creds)
        return clients
    
    def _get_credentials(self, sts_role_arn, aws_client_configs=Config()):
        sts = self._get_client("sts", aws_client_configs)
        creds = sts.assume_role(role_arn=sts_role_arn, role_session_name="tmp")
        return {
            "aws_access_key_id": creds["Credentials"]["AccessKeyId"],
            "aws_secret_access_key": creds["Credentials"]["SecretAccessKey"],
            "aws_session_token": creds["Credentials"]["SessionToken"],
        }
            
    def _get_client(self, service, config=Config(), creds={}):
        return boto3.client(service, config=Config(), **creds)
    
    def _account_config(self):
        settings = self.config.get("Account", {})
        if "AccountId" not in settings:
            settings["AccountId"] = self.aws_account_id
        if "Region" not in settings:
            settings["Region"] = self.aws_region
        if "ArtifactBucket" not in settings:
            settings["ArtifactBucket"] = self.artifact_bucket
        self.artifact_bucket = settings["ArtifactBucket"]
        self.aws_account_id = settings["AccountId"]
        self.aws_region = settings["Region"]
        return AccountConfig.get(settings)
    
    def _spark_job_config(self):
        settings = self.config.get("SparkJob", {})
        return SparkJobConfig.get(settings)
    
    def _short_compute_config(self):
        settings = self.config.get("ShortRunningCompute", {})
        return ShortComputeConfig.get(settings)
    
    def _ml_training_config(self):
        return {}
    
    def _ml_endpoint_config(self):
        return {}
    
    def _estimator_config(self):
        settings = self.config.get("MLEstimator", {})
        return MLEstimatorConfig.get(settings)
    
    def get_role_arn(self, role_name):
        account_id = self.account.get("AccountId", self.aws_account_id)
        return f"arn:aws:iam::{account_id}:role/{role_name}"
    
    def get_ecr_registry(self, repository_name, image_name):
        ecr_registry = self.estimator_config.get("EcrRegistry", None)
        if ecr_registry:
            return ecr_registry
        account_id = self.account.get("AccountId", self.aws_account_id)
        region_name = self.account.get("Region", self.aws_account_id)
        return f"{account_id}.dkr.ecr.{region_name}.amazonaws.com/{repository_name}:{image_name}"

    def get_artifact_path(self, code_location):
        filename = code_location.split("/")[-1]
        if filename == "":
            filename = code_location.split("/")[-2] + "/"
        key = f"artifacts/{self.project}/{self.version}/{self.version_number}/{filename}"
        self.aws_clients["s3"].put_object(Bucket=self.artifact_bucket, Key=key, Body=open(code_location).read())
        return f"s3://{self.artifact_bucket}/{key}"

    def get_settings(self, class_name):
        return self.service_configs.get(class_name, {})
        

class AccountConfig():
    
    @classmethod
    def get(cls, config):
        settings = {
            "AccountId": str(config.get("AccountId", "")),
            "Region": config.get("Region", None),
            "DeploymentRoleArn": config.get("DeploymentRoleArn", None),
            "ArtifactBucket": config.get("ArtifactBucket", None)
        }
        if cls._valid(settings):
            return settings
        else:
            raise ValueError("AccountConfig is invalid.")
        
    @classmethod
    def _valid(cls, settings):
        return (
            cls._valid_account_id(settings["AccountId"])
            and settings["Region"] is not None
            and settings["ArtifactBucket"] is not None
        )
    
    @classmethod
    def _valid_account_id(cls, account_id):
        if len(account_id) != 12:
            return False
        for c in account_id:
            if c not in "0123456789":
                return False
        return True
    
class SparkJobConfig():
    
    @classmethod
    def get(cls, config):
        settings = {
            "SecurityConfiguration" : config.get("SecurityConfiguration", None),
            "EnableMetrics": config.get("EnableMetrics", "true"),
            "SparkUILogging": config.get("SparkUILogging", "true")
        }
        if cls._valid(settings):
            return settings
        else:
            raise ValueError("SparkJobConfig is invalid.")
        
    @classmethod
    def _valid(cls, settings):
        return (
            (settings["SecurityConfiguration"] is None or isinstance(settings["SecurityConfiguration"], str))
            and isinstance(settings["EnableMetrics"], str)
            and isinstance(settings["SparkUILogging"], str)
        )
    
class ShortComputeConfig():
    
    @classmethod
    def get(cls, config):
        settings = {
            "KmsKeyArn": config.get("KmsKeyArn", None),
            "TracingConfig": config.get("TracingConfig", None),
            "VpcConfig": config.get("VpcConfig", None)
        }
        if cls._valid(settings):
            return settings
        else:
            raise ValueError("ShortRunningComputeConfig is invalid.")
        
    @classmethod
    def _valid(cls, settings):
        return (
            (settings["KmsKeyArn"] is None or isinstance(settings["KmsKeyArn"], str))
            and cls._valid_tracing_config(settings["TracingConfig"])
            and cls._valid_vpc_config(settings["VpcConfig"])
        )
    
    @classmethod
    def _valid_tracing_config(cls, config):
        return (
            config is None
            or (
                isinstance(config, dict)
                and "Mode" in config
                and config["Mode"] in ["Active", "PassThrough"]
            )
        )
    
    @classmethod
    def _valid_vpc_config(cls, config):
        return (
            config is None
            or (
                isinstance(config, dict)
                and "SecurityGroupIds" in config
                and cls._is_string_array(config["SecurityGroupIds"])
                and "SubnetIds" in config
                and cls._is_string_array(config["SecurityGroupIds"])
            )
        )
        
    @classmethod
    def _is_string_array(cls, lst):
        if not isinstance(lst, list):
            return False
        for s in lst:
            if not isinstance(s, str):
                return False
        return True
    
    
class MLEstimatorConfig():
    
    @classmethod
    def get(cls, config):
        settings = {
            "SageMakerDefaultBucket": config.get("SageMakerDefaultBucket", None),
            "VolumeKmsKey": config.get("VolumeKmsKey", None),
            "EnforceStorageKmsKey": config.get("EnforceStorageKmsKey", False),
            "OutputKmsKey": config.get("OutputKmsKey", None),
            "MaxTimeout": config.get("MaxTimeout", 86400),
            "MaxSpotInstanceWait": config.get("MaxSpotInstanceWait", 86400),
            "Subnets": config.get("Subnets", None),
            "SecurityGroupIds": config.get("SecurityGroupIds", None),
            "EncryptInterContainerTraffic": config.get("EncryptInterContainerTraffic", False),
            "EnforceSpotInstances": config.get("EncryptInterContainerTraffic", True),
            "EnableSagemakerMetrics": config.get("EncryptInterContainerTraffic", True),
            "EnableNetworkIsolation": config.get("EncryptInterContainerTraffic", False),
            "EcrRegistry": config.get("EcrRegistry", None),
            "Tags": config.get("Tags", {})
        }
        if cls._valid(settings):
            return settings
        else:
            raise ValueError("MLEstimatorConfig is invalid.")
        
    @classmethod
    def _valid(cls, settings):
        return (
            (settings["VolumeKmsKey"] is None or isinstance(settings["VolumeKmsKey"], str))
            and (settings["OutputKmsKey"] is None or isinstance(settings["OutputKmsKey"], str))
            and isinstance(settings["MaxTimeout"], int)
            and (settings["Subnets"] is None or cls._is_string_array(settings["Subnets"]))
            and (settings["SecurityGroupIds"] is None or cls._is_string_array(settings["SecurityGroupIds"]))
        )
    
    @classmethod
    def _is_string_array(cls, lst):
        if not isinstance(lst, list):
            return False
        for s in lst:
            if not isinstance(s, str):
                return False
        return True

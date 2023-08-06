import os
import logging
from subprocess import call
import sagemaker

BUILD_DOCKER_COMMANDS = """
    registry_id=$(aws ecr describe-repositories --repository-name {repository_name} --query 'repositories[0].registryId' --output text)
    echo '### registry_id '$registry_id
    echo '### docker login'
    aws ecr get-login-password | docker login --username AWS --password-stdin {ecr_account}
    echo '### docker login finished'

    echo '### Starting build of docker images'
    if docker pull {ecr_account}/{repository_name}:{image_tag}; then
        docker build -f {folder}'/Dockerfile' -t {ecr_account}/{repository_name}:{image_tag} --cache-from {ecr_account}/{repository_name}:{image_tag} .
    else
        docker build -f {folder}'/Dockerfile' -t {ecr_account}/{repository_name}:{image_tag} .
    fi
    echo "### Pushing the Docker image... ###"
    docker push {ecr_account}/{repository_name}:{image_tag}
"""

class MLProcessor(sagemaker.processing.Processor):
    
    def __init__(self,
        role,
        mlops_config,
        image_uri=None,
        dockerfile_path=None,
        docker_registry=None,
        repository_name=None,
        image_tag_name=None,
        build_image=True,
        tags = {},
        **kwargs):
        

        self.mlops_config = mlops_config   
        self.role = role
        self.image_uri = image_uri
        
        if dockerfile_path:
            self.image_uri = self.build_container(dockerfile_path, docker_registry, repository_name, image_tag_name, mlops_config, build_image)
        
        if image_uri is None and dockerfile_path is None:
            raise ValueError("You must specify either image_uri or dockerfile_path.")
        
        kwargs = self._inject_mlops_config(kwargs, mlops_config, tags)
        
        print(kwargs)
        
        super(MLProcessor, self).__init__(self.image_uri, role,  **kwargs)
         
        
    def _inject_mlops_config(self, settings, mlops_config, tags):
        print(mlops_config)
        ml_config = mlops_config.estimator_config
        
        if 'volume_kms_key' not in settings:
            settings["volume_kms_key"] = ml_config.get("VolumeKmsKey", None)
        if settings["volume_kms_key"] is None and ml_config["EnforceStorageKmsKey"]:
            raise ValueError("You must set parameter volume_kms_key to your estimator")
            
        if 'max_runtime_in_seconds' not in settings:
            settings['max_runtime_in_seconds'] = ml_config.get("MaxTimeout", 86400)
            
        if 'output_kms_key' not in settings:
            settings["output_kms_key"] = ml_config.get("OutputKmsKey", None)
        if settings["output_kms_key"] is None and ml_config["EnforceStorageKmsKey"]:
            raise ValueError("You must set parameter output_kms_key to your estimator")
            
        settings['base_job_name'] = self._get_base_name(mlops_config)

        default_sagemaker_bucket = settings.get("default_bucket", ml_config.get("SageMakerDefaultBucket", None))
        if default_sagemaker_bucket is None:
            settings['sagemaker_session'] = sagemaker.Session(sagemaker_client=mlops_config.aws_clients['sagemaker'])
        else:
            settings['sagemaker_session'] = sagemaker.Session(sagemaker_client=mlops_config.aws_clients['sagemaker'], default_bucket=default_sagemaker_bucket)
                
        tags = {**tags, **ml_config.get("Tags", {})}
        settings['tags'] = [{ "Key": key, "Value": val} for key, val in tags.items()]
        
        if "network_config" not in settings:
            network = {}
        
            if ml_config['Subnets']:
                network['subnets'] = ml_config['Subnets']

            if ml_config['SecurityGroupIds']:
                network['security_group_ids'] = ml_config['SecurityGroupIds']

            if ml_config['EncryptInterContainerTraffic']:
                network['encrypt_inter_container_traffic'] = ml_config['EncryptInterContainerTraffic']
                
            if ml_config['EnableNetworkIsolation']:
                network['enable_network_isolation'] = True
            
            settings['network_config'] = sagemaker.network.NetworkConfig(**network)
            
        return settings
            
    def _get_base_name(self, mlops_config):
        name = mlops_config.project
        if mlops_config.version: name += f"-{mlops_config.version}"
        if mlops_config.version_number: name += f"-{mlops_config.version_number}"
        return name + "-"    
    
    def build_container(self, dockerfile_path, ecr_account, repository_name, image_tag, mlops_config, build_image=True):
        if not os.path.isfile(dockerfile_path):
            raise FileNotFoundError(f"Dockerfile must be in your source directory {dockerfile_path}")    
        
        image_tag = self._get_image_tag(image_tag, mlops_config.version, mlops_config.version_number)
        ml_config = mlops_config.estimator_config
        
        if ecr_account is None:
            ecr_account = ml_config.get('EcrRegistry', None)
        if ecr_account is None:
            raise Exception("Set your ecr account")

        bash_script = BUILD_DOCKER_COMMANDS.format(
            folder="/".join(dockerfile_path.split("/")[:-1]),
            ecr_account=ecr_account,
            repository_name=repository_name, 
            image_tag=image_tag,
        )
        logging.info("Building container...")
        if build_image:
            call(bash_script, shell=True)

        return ecr_account+"/"+repository_name+":"+image_tag
    
    def _get_image_tag(self, image_tag, version, version_number):
        if image_tag is None:
            return f"{version}-{version_number}"
        if len(image_tag.split(":")) == 1:
            image_tag = image_tag+ ":" + version
        if version_number:
            image_tag += f"-{version_number}"
        return image_tag



class SKLearnMLProcessor(sagemaker.sklearn.SKLearnProcessor):
    
    def __init__(self,
        framework_version,
        role,
        mlops_config,
        tags = {},
        **kwargs):
        

        self.mlops_config = mlops_config   
        self.role = role        
        
        kwargs = self._inject_mlops_config(kwargs, mlops_config, tags)
        
        print(kwargs)
        
        super(SKLearnMLProcessor, self).__init__(framework_version=framework_version, role=role,  **kwargs)
         
        
    def _inject_mlops_config(self, settings, mlops_config, tags):
        print(mlops_config)
        ml_config = mlops_config.estimator_config
        
        if 'volume_kms_key' not in settings:
            settings["volume_kms_key"] = ml_config.get("VolumeKmsKey", None)
        if settings["volume_kms_key"] is None and ml_config["EnforceStorageKmsKey"]:
            raise ValueError("You must set parameter volume_kms_key to your estimator")
            
        if 'max_runtime_in_seconds' not in settings:
            settings['max_runtime_in_seconds'] = ml_config.get("MaxTimeout", 86400)
            
        if 'output_kms_key' not in settings:
            settings["output_kms_key"] = ml_config.get("OutputKmsKey", None)
        if settings["output_kms_key"] is None and ml_config["EnforceStorageKmsKey"]:
            raise ValueError("You must set parameter output_kms_key to your estimator")
            
        settings['base_job_name'] = self._get_base_name(mlops_config)
        settings['sagemaker_session'] = sagemaker.Session(sagemaker_client=mlops_config.aws_clients['sagemaker'])
        
        tags = {**tags, **ml_config.get("Tags", {})}
        settings['tags'] = [{ "Key": key, "Value": val} for key, val in tags.items()]
        
        if "network_config" not in settings:
            network = {}
        
            if ml_config['Subnets']:
                network['subnets'] = ml_config['Subnets']

            if ml_config['SecurityGroupIds']:
                network['security_group_ids'] = ml_config['SecurityGroupIds']

            if ml_config['EncryptInterContainerTraffic']:
                network['encrypt_inter_container_traffic'] = ml_config['EncryptInterContainerTraffic']
                
            if ml_config['EnableNetworkIsolation']:
                network['enable_network_isolation'] = True
            
            settings['network_config'] = sagemaker.network.NetworkConfig(**network)
            
        return settings
            
    def _get_base_name(self, mlops_config):
        name = mlops_config.project
        if mlops_config.version: name += f"-{mlops_config.version}"
        if mlops_config.version_number: name += f"-{mlops_config.version_number}"
        return name + "-"    
    
    
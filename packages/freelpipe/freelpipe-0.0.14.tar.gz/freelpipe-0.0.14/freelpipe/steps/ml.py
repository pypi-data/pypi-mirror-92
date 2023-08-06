from stepfunctions.inputs import ExecutionInput
from stepfunctions import steps


class MLTrainingJob(steps.TrainingStep):
    
    def __init__(self, state_id, estimator, job_name, **kwargs):
        
        self.training_job_name = job_name
        
        dummy = ExecutionInput(schema={ 'TrainingJobName': str })
        
        super(MLTrainingJob, self).__init__(state_id, estimator, dummy['TrainingJobName'], **kwargs)
        
    def create(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_job_name(project, version, version_number)
        
    def update(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_job_name(project, version, version_number)
        
    def _set_job_name(self, project, version, version_number):
        name = project.replace('_', '-')
        if version: name += f"-{version}"
        if version_number: name += f"-{version_number}"
        name = f"{name}-{self.training_job_name}".lower()
        if len(name) > 28:
            name = name[:28]
        self.parameters['TrainingJobName.$'] = "States.Format('{}-{}', '"+name+"', $$.Execution.Name)"
        self.update_parameters(self.parameters)
        
    def get_cloudformation_template(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_job_name(project, version, version_number)
        return None, None
        
        
class MLTransform(steps.TransformStep):
    
    def __init__(self, state_id, transformer, model_name, data, **kwargs):
        
        self.model_name = model_name
        
        super(MLTransform, self).__init__(state_id, transformer, model_name, model_name, data, **kwargs)
        
    def create(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_model_name(project, version, version_number)
        
    def update(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_model_name(project, version, version_number)
        
    def _set_model_name(self, project, version, version_number):
        name = project.replace('_', '-')
        if version: name += f"-{version}"
        if version_number: name += f"-{version_number}"
        name = f"{name}-{self.model_name}".lower()
        if len(name) > 28:
            name = name[:28]
        if 'TransformJobName' in self.parameters:
            del self.parameters['TransformJobName']
        self.parameters['TransformJobName.$'] = "States.Format('{}-{}', '"+name+"', $$.Execution.Name)"
        if 'ModelName' in self.parameters:
            del self.parameters['ModelName']
        self.parameters['ModelName.$'] = "States.Format('{}-{}', '"+name+"', $$.Execution.Name)"
        self.update_parameters(self.parameters)
        
    def get_cloudformation_template(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_model_name(project, version, version_number)
        return None, None
         
        
class MLModel(steps.ModelStep):
    
    def __init__(self, state_id, model, model_name, **kwargs):
        
        self.model_name = model_name
        
        super(MLModel, self).__init__(state_id, model, **kwargs)
        
    def create(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_model_name(project, version, version_number)
        
    def update(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_model_name(project, version, version_number)
        
    def _set_model_name(self, project, version, version_number):
        name = project.replace('_', '-')
        if version: name += f"-{version}"
        if version_number: name += f"-{version_number}"
        name = f"{name}-{self.model_name}".lower()
        if len(name) > 28:
            name = name[:28]
        self.parameters['ModelName.$'] = "States.Format('{}-{}', '"+name+"', $$.Execution.Name)"
        self.update_parameters(self.parameters)
        
    def get_cloudformation_template(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_model_name(project, version, version_number)
        return None, None
            
            
class MLEndpointConfig(steps.EndpointConfigStep):
    
    def __init__(self, state_id, model_name, initial_instance_count, instance_type, **kwargs):
        
        self.model_name = model_name
        
        super(MLEndpointConfig, self).__init__(state_id, model_name, model_name, initial_instance_count, instance_type, **kwargs)
        
    def create(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_model_name(project, version, version_number)
        
    def update(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_model_name(project, version, version_number)
        
    def _set_model_name(self, project, version, version_number):
        name = project.replace('_', '-')
        if version: name += f"-{version}"
        if version_number: name += f"-{version_number}"
        name = f"{name}-{self.model_name}".lower()
        if len(name) > 28:
            name = name[:28]
        if 'EndpointConfigName' in self.parameters:
            del self.parameters['EndpointConfigName']
        self.parameters['EndpointConfigName.$'] = "States.Format('{}-{}', '"+name+"', $$.Execution.Name)"
        if 'ModelName' in self.parameters['ProductionVariants'][0]:
            del self.parameters['ProductionVariants'][0]['ModelName']
        self.parameters['ProductionVariants'][0]['ModelName.$'] = "States.Format('{}-{}', '"+name+"', $$.Execution.Name)"
        self.update_parameters(self.parameters)
        
    def get_cloudformation_template(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_model_name(project, version, version_number)
        return None, None
        

class MLEndpoint(steps.EndpointStep):
    
    def __init__(self, state_id, model_name, **kwargs):
        
        self.model_name = model_name
        
        super(MLEndpoint, self).__init__(state_id, model_name, model_name, **kwargs)
        
    def create(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_config_endpoint_name(project, version, version_number)
        self._set_endpoint_name(project, version, version_number)
        self.update_parameters(self.parameters)
        
    def update(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_config_endpoint_name(project, version, version_number)
        self._set_endpoint_name(project, version, version_number)
        self.update_parameters(self.parameters)
        
    def _set_config_endpoint_name(self, project, version, version_number):
        name = project.replace('_', '-')
        if version: name += f"-{version}"
        if version_number: name += f"-{version_number}"
        name = f"{name}-{self.model_name}".lower()
        if len(name) > 28:
            name = name[:28]
        if 'EndpointConfigName' in self.parameters:
            del self.parameters['EndpointConfigName']
        self.parameters['EndpointConfigName.$'] = "States.Format('{}-{}', '"+name+"', $$.Execution.Name)"
        
    def _set_endpoint_name(self, project, version, version_number):
        name = project.replace('_', '-')
        if version: name += f"-{version}"
        if version_number: name += f"-{version_number}"
        name = f"{name}-{self.model_name}".lower()
        self.parameters['EndpointName'] = name
        
    def get_cloudformation_template(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_config_endpoint_name(project, version, version_number)
        self._set_endpoint_name(project, version, version_number)
        return None, None
        

class MLInference(steps.Chain):
    
    def __init__(self, model_name, initial_instance_count, instance_type, update=False, **kwargs):
        
        endpoint_config_step = MLEndpointConfig(
            "Create Model Endpoint Config",
            model_name=model_name,
            initial_instance_count=initial_instance_count,
            instance_type=instance_type
        )

        endpoint_step = MLEndpoint(
            'Update Model Endpoint',
            model_name=model_name,
            update=update
        )
        
        super(MLInference , self).__init__([
            endpoint_config_step,
            endpoint_step
        ])
        

class MLProcessingJob(steps.ProcessingStep):
    
    def __init__(self, state_id, processor, job_name, code_location=None, **kwargs):
        
        self.processing_job_name = job_name
        self.code_location = code_location
        
        dummy = ExecutionInput(schema={ 'ProcessingJobName': str })
        
        super(MLProcessingJob, self).__init__(state_id, processor, dummy['ProcessingJobName'], **kwargs)
        
    def create(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_job_name(project, version, version_number)
        if self.code_location:
            self._upload_script(project, artifact_bucket, version, version_number, aws_clients["s3"])
        
    def update(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_job_name(project, version, version_number)
        if self.code_location:
            self._upload_script(project, artifact_bucket, version, version_number, aws_clients["s3"])
        
    def _set_job_name(self, project, version, version_number):
        name = project.replace('_', '-')
        if version: name += f"-{version}"
        if version_number: name += f"-{version_number}"
        name = f"{name}-{self.processing_job_name}".lower()
        if len(name) > 28:
            name = name[:28]
        self.parameters['ProcessingJobName.$'] = "States.Format('{}-{}', '"+name+"', $$.Execution.Name)"
        self.update_parameters(self.parameters)

    def _upload_script(self, project, artifact_bucket, version, version_number, s3_client):
        filename = self.code_location.split("/")[-1]
        key = f"artifacts/{project}/{version}/{version_number}/{filename}"
        s3_client.put_object(Bucket=artifact_bucket, Key=key, Body=open(self.code_location).read())
        return f"s3://{artifact_bucket}/{key}"
        
    def get_cloudformation_template(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        self._set_job_name(project, version, version_number)
        return None, None
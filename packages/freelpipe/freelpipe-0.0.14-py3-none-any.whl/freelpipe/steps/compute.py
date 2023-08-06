from stepfunctions import steps
import os
import boto3
import sagemaker
import logging
from subprocess import call
from stepfunctions.steps.fields import Field


class SparkJobStep(steps.GlueStartJobRunStep):


    def __init__(self, 
                 state_id,
                 job_name,
                 role_arn, 
                 script_location,
                 arguments={},
                 timeout=2880,
                 libraries=[],
                 max_concurrent_runs=2,
                 number_of_workers=2,
                 max_retries=0,
                 glue_version="2.0",
                 worker_type="Standard",
                 python_version="3",
                 security_configuration=None,
                 connections=[],
                 tags={},
                 **kwargs):
        
        self.job_name = job_name #Validate with regex
        self.timeout = timeout
        self.libraries = libraries
        self.max_concurrent_runs = max_concurrent_runs
        self.number_of_workers = number_of_workers
        self.max_retries = max_retries
        self.glue_version = glue_version
        self.worker_type = worker_type
        self.role_arn = role_arn
        self.connections = connections
        self.python_version = python_version
        self.security_configuration = security_configuration
        self.connections = connections
        self.tags = tags
        
        if not os.path.exists(script_location) or not os.path.isfile(script_location):
            raise FileNotFoundError(f"{script_location} is missing")
            
        self.script_location = script_location
        
        self.parameters = {
            "Arguments": arguments
        }
        
        super(SparkJobStep, self).__init__(state_id, **kwargs)

    
    def get_cloudformation_template(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        if aws_clients["s3"] is None:
            aws_clients["s3"] = boto3.client('s3')
        print("here")
        job_name = self.get_job_name(project, version, version_number)
        script_location = self._upload_script(project, artifact_bucket, version, version_number, aws_clients["s3"])
        template = {
            "Type": "AWS::Glue::Job",
            "Properties": self._get_job_properties(job_name, script_location, project, artifact_bucket, version, version_number, service_config)
        }
        template["Properties"]["Name"] = job_name
        
        resource_name = "".join([x.title() for x in job_name.split("_")])
        return resource_name, template
        
    def get_job_name(self, project, version="dev", version_number=0):
        name = project.replace('-', '_')
        if version: name += f"_{version}"
        if version_number: name += f"_{version_number}"
        name = f"{name}_{self.job_name}".lower()
        self._update_job_name(name)
        return name
            
    def create(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        if aws_clients["s3"] is None:
            aws_clients["s3"] = boto3.client('s3')
        if aws_clients["glue"] is None:
            aws_clients["glue"] = boto3.client('glue')
        job_name = self.get_job_name(project, version, version_number)
        if self._exists(aws_clients["glue"], job_name):
            return self.update(project, artifact_bucket, version, version_number, service_config, aws_clients)
        logging.info(f"Creating Glue job {job_name}")
        script_location = self._upload_script(project, artifact_bucket, version, version_number, aws_clients["s3"])
        return self._create(job_name, script_location, project, artifact_bucket, version, version_number, service_config, aws_clients["glue"])
        
    def _create(self, job_name, script_location, project, artifact_bucket, version, version_number, service_config, glue_client):
        properties = self._get_job_properties(job_name, script_location, project, artifact_bucket, version, version_number, service_config)
        properties["Name"] = job_name
        return glue_client.create_job(**properties)
    
    def _exists(self, glue_client, job_name):
        try:
            glue_client.get_job(
                JobName=job_name
            )
            return True
        except Exception:
            return False
        
    def update(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        if aws_clients["s3"] is None:
            aws_clients["s3"] = boto3.client('s3')
        if aws_clients["glue"] is None:
            aws_clients["glue"] = boto3.client('glue')
        job_name = self.get_job_name(project, version, version_number)
        if not self._exists(aws_clients["glue"], job_name):
            self.create(project, artifact_bucket, version, version_number, service_config, aws_clients)
        logging.info(f"Updating Glue job {job_name}")
        script_location = self._upload_script(project, artifact_bucket, version, version_number, aws_clients["s3"])
        return self._update(job_name, script_location, project, artifact_bucket, version, version_number, service_config, aws_clients["glue"])
    
    def _update(self, job_name, script_location, project, artifact_bucket, version, version_number, service_config, glue_client):
        updates = self._get_job_properties(job_name, script_location, project, artifact_bucket, version, version_number, service_config)
        del updates['Tags']
        properties = {
            "JobName": job_name,
            "JobUpdate": updates
        }
        return glue_client.update_job(**properties)
    
    def _get_job_properties(self, job_name, script_location, project, artifact_bucket, version, version_number, service_config):
        properties = {
            "DefaultArguments": self._set_args(job_name, project, artifact_bucket, version, version_number, service_config),
            "Command": {
                'Name': 'glueetl',
                'ScriptLocation': script_location,
                'PythonVersion': self.python_version
            },
            "Description": f"Project: {project}",
            "ExecutionProperty": {
                "MaxConcurrentRuns": self.max_concurrent_runs
            },
            "GlueVersion": self.glue_version,
            "MaxRetries": self.max_retries,
            "NumberOfWorkers": self.number_of_workers,
            "Role": self.role_arn,
            "Tags": self._set_tags(project),
            "Timeout": self.timeout,
            "WorkerType": self.worker_type
        }
        if self.connections:
            properties["Connections"] = self.connections
        if self.security_configuration:
            properties["SecurityConfiguration"] = self.security_configuration
        elif service_config.get("SecurityConfiguration", None):
            properties["SecurityConfiguration"] = service_config["SecurityConfiguration"]
        return properties
    
    def delete(self, project, artifact_bucket, version=None, version_number=0, aws_clients={}):
        if aws_clients["glue"] is None:
            aws_clients["glue"] = boto3.client('glue')
        job_name = self.get_job_name(project, version, version_number)
        if not self._exists(aws_clients["glue"], job_name):
            raise RuntimeError("Glue job doesn't exists")
        logging.info(f"Deleting Glue job {job_name}")
        return aws_clients["glue"].delete_job(
            JobName=job_name
        )
    
    def _update_job_name(self, job_name):
        self.parameters['JobName'] = job_name
        self.update_parameters(self.parameters)
    
    def _set_args(self, job_name, project, artifact_bucket, version, version_number, service_config={}):
        args = {
            '--job-language': 'python',
            "--enable-metrics": service_config.get("EnableMetrics", "true"), 
            "--enable-spark-ui": service_config.get("SparkUILogging", "true"),
            "--spark-event-logs-path": f"s3://{artifact_bucket}/artifacts/{project}/{version}/{version_number}/_logs/{job_name}/"
        }
        if len(self.libraries) > 0:
            args["--extra-py-files"] = ",".join(self.libraries)
        return args
    
    def _set_tags(self, project):
        return { "App": project, **self.tags }
    
    def _upload_script(self, project, artifact_bucket, version, version_number, s3_client):
        filename = self.script_location.split("/")[-1]
        key = f"artifacts/{project}/{version}/{version_number}/{filename}"
        s3_client.put_object(Bucket=artifact_bucket, Key=key, Body=open(self.script_location).read())
        return f"s3://{artifact_bucket}/{key}"
        
        

PACKAGE_COMMAND = """
    MAIN_FOLDER=$(pwd);
    rm -f "{output_location}{package_name}";
    cd {folder};
    echo {folder}
    echo "{output_location}{package_name}"
    zip -r9 "{output_location}{package_name}" . -x \*.git\* -x \*.pyc\* -x \*__pycache__\*;
    if [ -f "requirements.txt" ]; then
        mkdir ../packages
        pip3 install -r requirements.txt --target ../packages
        cd ../packages
        zip -g -r "{output_location}{package_name}" . -x \*.git\* -x \*.pyc\* -x \*__pycache__\*
    fi
"""
        
class ShortComputeTask(steps.LambdaStep):
    
    def __init__(self, 
                 state_id, 
                 function_name, 
                 scripts_location, 
                 entry_point, 
                 role_arn,
                 wait_for_callback=False, 
                 timeout=15, 
                 memory=128, 
                 runtime='python3.8',
                 environment={},
                 tags={},
                 reserved_concurrent_executions=0,
                 **kwargs):
        
        self.function_name = function_name
        self.scripts_location = scripts_location
        self.role_arn = role_arn
        self.runtime = runtime
        self.entry_point = entry_point
        self.timeout = timeout
        self.memory = memory
        self.environment = environment
        self.reserved_concurrent_executions = reserved_concurrent_executions
        self.tags = tags
        
        if not os.path.exists(self.scripts_location) or not os.path.isdir(self.scripts_location):
            raise FileNotFoundError(f"{self.scripts_location} is missing or is not a directory")
            
        if wait_for_callback:
            kwargs[Field.Resource.value] = 'arn:aws:states:::lambda:invoke.waitForTaskToken'
        else:
            kwargs[Field.Resource.value] = 'arn:aws:states:::lambda:invoke'
                    
        super(ShortComputeTask, self).__init__(state_id, **kwargs)
        
    def _get_function_properties(self, function_name, project, code_location=None, version=None, version_number=None, service_config={}):
        properties = {
            "Description": f"Project: {project}",
            "Environment": {
                "Variables": self._set_env_variables(project, version, version_number)
            },
            "FunctionName": function_name,
            "Handler": self.entry_point,
            #"ImageConfig"
            "MemorySize": self.memory,
            "Role": self.role_arn,
            "Runtime": self.runtime,
            "Tags": self._set_tags(project, cfn=True),
            "Timeout": self.timeout
        }
        if code_location:
            properties["Code"] = {
                "S3Bucket": code_location["S3Bucket"],
                "S3Key": code_location["S3Key"]
            }
        if service_config.get("KmsKeyArn", None):
            properties["KmsKeyArn"] = service_config["KmsKeyArn"]
        if self.reserved_concurrent_executions:
            properties["ReservedConcurrentExecutions"] = self.reserved_concurrent_executions
        if service_config.get("TracingConfig", None):
            properties["TracingConfig"] = service_config["TracingConfig"]
        if service_config.get("VpcConfig", None):
            properties["VpcConfig"] = service_config["VpcConfig"]
        return properties

    def _set_env_variables(self, project, version="dev", version_number=0):
        envs = { "PROJECT": project }
        if version: envs['VERSION'] = version
        if version_number: envs['VERSION_NUMBER'] = version_number
        return {
            **envs,
            **self.environment
        }
    
    def get_cloudformation_template(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        if aws_clients["s3"] is None:
            aws_clients["s3"] = boto3.client('s3')
        package_location = self._package_scripts()
        code_location = self._upload_package(package_location, project, artifact_bucket, version, version_number, aws_clients["s3"])
        function_name = self.get_function_name(project, version, version_number)
        template = {
            "Type": "AWS::Lambda::Function",
            "Properties": self._get_function_properties(function_name, project, code_location, version, version_number, service_config)
        }
        
        resource_name = "".join([x.title() for x in function_name.split("-")])
        return resource_name, template
    
    def get_function_name(self, project, version="dev", version_number=0):
        name = project.replace('_', '-')
        if version: name += f"-{version}"
        if version_number: name += f"-{version_number}"
        name = f"{name}-{self.function_name}".lower()
        self._update_function_name(name)
        return name
    
    def _update_function_name(self, function_name):
        self.parameters['FunctionName'] = function_name
        print(self.parameters)
        self.update_parameters(self.parameters)
    
    def create(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        if aws_clients["s3"] is None:
            aws_clients["s3"] = boto3.client('s3')
        if aws_clients["lambda"] is None:
            aws_clients["lambda"] = boto3.client('lambda')
        function_name = self.get_function_name(project, version, version_number)
        if self._exists(aws_clients["lambda"], function_name):
            return self.update(project, artifact_bucket, version, version_number, service_config, aws_clients)
        logging.info(f"Creating Lambda function {function_name}")
        package_location = self._package_scripts()
        code_location = self._upload_package(package_location, project, artifact_bucket, version, version_number, aws_clients["s3"])
        return self._create(function_name, code_location, project, version, version_number, service_config, aws_clients["lambda"])
    
    def _create(self, function_name, code_location, project, version, version_number, service_config, lambda_client):
        properties = self._get_function_properties(function_name, project, code_location, version, version_number, service_config)
        return lambda_client.create_function(**properties)
    
    def update(self, project, artifact_bucket, version=None, version_number=0, service_config={}, aws_clients={}):
        if aws_clients["s3"] is None:
            aws_clients["s3"] = boto3.client('s3')
        if aws_clients["lambda"] is None:
            aws_clients["lambda"] = boto3.client('lambda')
        function_name = self.get_function_name(project, version, version_number)
        if not self._exists(aws_clients["lambda"], function_name):
            return self.create(project, artifact_bucket, version, version_number, service_config, aws_clients)
        logging.info(f"Updating Lambda function {function_name}")
        package_location = self._package_scripts()
        code_location = self._upload_package(package_location, project, artifact_bucket, version, version_number, aws_clients["s3"])
        return self._update(function_name, code_location, project, version, version_number, service_config, aws_clients["lambda"])
    
    def _update(self, function_name, code_location, project, version, version_number, service_config, lambda_client):
        properties = self._get_function_properties(function_name, project, version=version, version_number=version_number, service_config=service_config)
        del properties['Tags']
        lambda_client.update_function_configuration(**properties)
        return lambda_client.update_function_code(
            FunctionName=function_name,
            S3Bucket=code_location['S3Bucket'],
            S3Key=code_location['S3Key']
        )
    
    def delete(self, project, artifact_bucket, version=None, version_number=0, lambda_client=None):
        if lambda_client is None:
            lambda_client = boto3.client('lambda')
        function_name = self.get_function_name(project, version, version_number)
        if not self._exists(lambda_client, function_name):
            raise RuntimeError("Function doesn't exists")
        return lambda_client.delete_function(
            FunctionName=function_name
        )
    
    
    def _exists(self, lambda_client, function_name):
        try:
            lambda_client.get_function(
                FunctionName=function_name
            )
            return True
        except Exception:
            return False
        
    def _package_scripts(self, output_location=None):
        package_name = f"{self.scripts_location.split('/')[-1] if self.scripts_location[-1] != '/' else self.scripts_location.split('/')[-2]}.zip"
        output_location, output_location_script = self._format_output_location(output_location)
        bash_script = PACKAGE_COMMAND.format(output_location=output_location_script, folder=self.scripts_location, package_name=package_name)
        call(bash_script, shell=True)
        if not os.path.isfile(output_location+package_name):
            raise RuntimeError("Lambda package hasn't been created")
        return output_location+package_name
    
    def _format_output_location(self, output_location):
        if output_location is None:
            output_location = "/tmp/"
        if output_location.startswith("./"):
            output_location = output_location[2:]
        output_location_script = output_location
        if not output_location_script.startswith("/"):
            output_location_script = "$MAIN_FOLDER/" + output_location_script
        return output_location, output_location_script
        
    def _upload_package(self, package_location, project, artifact_bucket, version, version_number, s3_client):
        filename = package_location.split("/")[-1]
        key = f"artifacts/{project}/{version}/{version_number}/{filename}"
        s3_client.put_object(Bucket=artifact_bucket, Key=key, Body=open(package_location, 'rb').read())
        os.remove(package_location)
        return { "S3Bucket": artifact_bucket, "S3Key": key }
    
    def _set_tags(self, project, cfn=False):
        if not cfn:
            self.tags['App'] = project
            return self.tags
        else:
            return [{ "Key": "App", "Value": project}]
    
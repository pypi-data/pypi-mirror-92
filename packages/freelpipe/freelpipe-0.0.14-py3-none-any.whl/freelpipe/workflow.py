from stepfunctions.workflow import Workflow
from freelpipe.steps import BuildStates
from stepfunctions.steps import Graph
import uuid
import json
import yaml
import logging

logger = logging.getLogger('stepfunctions')

def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)

yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str
yaml.add_representer(dict, lambda self, data: yaml.representer.SafeRepresenter.represent_dict(self, data.items()), Dumper=yaml.SafeDumper)
yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)


CLOUDFORMATION_BASE_TEMPLATE = {
    "AWSTemplateFormatVersion": '2010-09-09',
    "Description": "Resource stack",
    "Resources": {
    }
}


class AWSWorkflow(Workflow):
    
    def __init__(self, name, definition, role, mlops_config, include_version_number=False, **kwargs):
        
        self.initial_name = name
        self.project = mlops_config.project
        self.artifact_bucket = mlops_config.artifact_bucket
        self.version_number = mlops_config.version_number
        self.include_version_number = include_version_number
        self.workflow_name = self.get_cloudformation_name()
        
        self.mlops_config = mlops_config
        
        self.role = role
        self.states = definition
        
        super(AWSWorkflow, self).__init__(self.workflow_name, definition, role, **kwargs)
        
    def create(self):
        
        for state in self.states:
            if type(state) in BuildStates.get_classes():
                state.create(self.project, self.artifact_bucket, self.mlops_config.version, self.version_number, service_config=self.mlops_config.get_settings(type(state)), aws_clients=self.mlops_config.aws_clients)
                
        if self.states:
            if isinstance(self.states, Graph):
                self.definition = self.states
            else:
                self.definition = Graph(
                    self.states,
                    timeout_seconds=self.timeout_seconds,
                    comment=self.comment,
                    version=self.mlops_config.version
                )
        
        super(AWSWorkflow, self).create()
        
    def update(self, definition=None, role=None):
        
        for state in self.definition.states:
            if type(state) in BuildStates.get_classes():
                state.create(self.project, self.artifact_bucket, self.mlops_config.version self.version_number, service_config=self.mlops_config.get_settings(type(state)), aws_clients=self.mlops_config.aws_clients)
        
        super(AWSWorkflow, self).update(definition, role)
        
    def execute(self, name=None, inputs=None):
        
        name = uuid.uuid1().hex if name is None else name
        
        super(AWSWorkflow, self).execute(name, inputs)
    
    
    def delete(self, include_components=True):
        
        if include_components:
            for state in self.definition.states:
                if type(state) in BuildStates.get_classes():
                    state.delete(self.project, self.artifact_bucket, self.mlops_config.version, self.version_number, service_config=self.mlops_config.get_settings(type(state)), aws_clients=self.mlops_config.aws_clients)

        super(AWSWorkflow, self).delete()
        
    
    def get_cloudformation_template(self):
        
        resources_template = CLOUDFORMATION_BASE_TEMPLATE.copy()


        has_resource = False
        for state in self.states:
            if type(state) in BuildStates.get_classes():
                resource_name, template = state.get_cloudformation_template(self.project, self.artifact_bucket, self.mlops_config.version, self.version_number, service_config=self.mlops_config.get_settings(type(state)), aws_clients=self.mlops_config.aws_clients)
                if resource_name:
                    has_resource = True
                    resources_template["Resources"][resource_name] = template
        
        if has_resource:
            resources_template = yaml.safe_dump(resources_template, default_flow_style=False)
        else:
            resources_template = None

        self.definition = Graph(
            self.states,
            timeout_seconds=self.timeout_seconds,
            comment=self.comment,
            version=self.mlops_config.version
        )
        workflow_template = super().get_cloudformation_template()

        return (workflow_template, resources_template)


    def get_freeldep_config(self, output_filename=None):
        workflow_template, resources_template = self.get_cloudformation_template()
        workflow_file = self._save_template(workflow_template)
        resource_file = self._save_template(resources_template)

        conf = []
        if workflow_file:
            conf += self._freeldep(self.get_cloudformation_name(suffix="workflow"), workflow_file)
        if resource_file:
            conf += self._freeldep(self.get_cloudformation_name(suffix="resources"), resource_file)

        if output_filename:
            with open(output_filename, "w+") as f:
                yaml.dump(conf, f)
        return conf


    
    def _save_template(self, template, filename=None):
        if template is None:
            return None

        if filename is None:
            filename = uuid.uuid1().hex + ".yaml"

        with open(filename, "w+") as f:
            f.write(template)

        return filename

    def _freeldep(self, template_name, template_filename):
        account = self.mlops_config.account
        return [{
            "aws": {
                "region": account.get("Region", None),
                "account-id":  account.get("AccountId", None),
                "deployment-role":  account.get("DeploymentRoleArn", None),
            },
            "location": template_filename,
            "template": {
                "name": template_name,
                "parameters": {},
            },
            "functions": [],
        }]

    def get_cloudformation_name(self, suffix=None):
        name = f"{self.project}-{self.mlops_config.version}-"
        if suffix == "resources" and self.version_number:
            name += f"{self.version_number}-"
        elif self.include_version_number:
            name += f"{self.version_number}-"
        name += f"{self.initial_name}".lower()
        if suffix:
            name += f"-{suffix}"
        return name.lower()
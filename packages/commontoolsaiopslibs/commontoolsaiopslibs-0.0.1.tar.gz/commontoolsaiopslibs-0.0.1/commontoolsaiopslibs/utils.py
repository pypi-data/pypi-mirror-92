import csv
import pickle
import os
from azureml.core.compute import AmlCompute, ComputeTarget, RemoteCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core.datastore import Datastore
from msrest.exceptions import HttpOperationError
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import ntpath
from azureml.pipeline.core import Schedule
from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig, Model
from azureml.pipeline.core import PipelineEndpoint
from azureml.exceptions import WebserviceException
import requests
import json
from azure.storage.blob import BlobClient
import asyncio
import urllib, json
import urllib.request
from urllib.error import URLError, HTTPError
from os import listdir
from os.path import isfile, join
import shutil
import yaml
import sys
import time
import numpy as np
import joblib
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
import seaborn as sns
import matplotlib.pyplot as plt
import yaml
import uuid
import string
import random
import glob
import re
import logging
import time
import xml.etree.ElementTree as ET
from functools import wraps
sns.set(color_codes=True)

def timer(logger):
    def d_timer(func):
        """time the running time of the passed in function"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time() - t1
            print('{} ran in: {} sec'.format(func.__name__, t2))
            logger.warning('{} ran in: {} sec'.format(func.__name__, t2))
            return result
        
        return wrapper
    return d_timer

def azureml_timer(logger, run):
    def d_timer(func):
        """time the running time of the passed in function"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time() - t1
            if run.parent:
                custom_dimensions = {
                                    "parent_run_id": run.parent.id,
                                    "step_id": run.id,
                                    "step_name": run.name,
                                    "experiment_name": run.experiment.name,
                                    "run_url": run.parent.get_portal_url(),
                                    "duration_in_sec": t2,
                                    "method_name":func.__name__
                                    }
            else:
                custom_dimensions = {"duration_in_sec": t2, "method_name":func.__name__}

            logger.warning('{} ran in: {} sec'.format(func.__name__, t2), custom_dimensions)
            return result
        
        return wrapper
    return d_timer

class JoblibUtilities:
    @staticmethod
    def load_file_from_txt(file_content):
        temp = "./temp"
        FolderUtilities.make_dir(temp)
        
        temp_file = os.path.join(temp, str(uuid.uuid4()))

        joblib.dump(file_content, temp_file)
        result = joblib.load(file_content)
        shutil.rmtree(temp_file, ignore_errors=True)
        return result

class PickleUtilities:

    @staticmethod
    def load_file(path_file):
        """allows to load a file recorded by the pickle library

        Arguments:
            path_file {str} -- recorded pickle file path

        Returns:
            [type] -- pickle object
        """

        file = open(path_file,'rb')
        object_file = pickle.load(file)
        file.close()
        return object_file
    
    @staticmethod
    def write_file(path_file, data):
        """Allows to write data to new pickle file.

        Arguments:
            path_file {str} -- pickle path file  
            data {array} -- data content
        """
        print("write_file.path_file : ", path_file)
        os.makedirs(os.path.dirname(os.path.abspath(path_file)), exist_ok=True)
        
        with open(path_file, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

class FileUtilities:
    @staticmethod
    def create_file_with_content(file_name, content):
        """creates a file and manages closing connection even in case of an exception

        Arguments:
            file_name {str} -- file path
            content {str} -- file content

        Raises:
            Exception: [description]
        """
        try:
            file = open(file_name, "w")
            file.write(content)
        except Exception as e:
            raise Exception('an error occured during writing file operation : {}'.format(e))
        finally:
            #delete temp directory
            file.close() 
    
    @staticmethod
    def list_recursive_files(path):
        for dirpath, dirs, files in os.walk(path):
            for filename in files:
                fname = os.path.join(dirpath,filename)
                print(fname)
    
    @staticmethod
    def direct_download_file(url, download_path):
        donloaded = False
        try:
            r = requests.get(url, allow_redirects=True)
            open(download_path, 'wb').write(r.content)
            donloaded = True
        except HTTPError as e:
            # do something
            print('Error code: ', e.code)
        except URLError as e:
            # do something
            print('Reason: ', e.reason)
        except Exception as e:
            # do something
            print('Reason: ', e)
        return donloaded
        
class FolderUtilities:
    @staticmethod
    def make_missing_dir_from_file(file_path):
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    @staticmethod 
    def make_dir(folder_path):
        os.makedirs(folder_path, exist_ok=True)

class ComputeTargetConfig:
    @staticmethod
    def config_create(ws,cluster_name, vm_type, min_nodes, max_nodes,idle_seconds ):
        #Create or Attach existing compute resource
        # choose a name for your cluster
        compute_name = os.environ.get("AML_COMPUTE_CLUSTER_NAME", cluster_name)
        compute_min_nodes = os.environ.get("AML_COMPUTE_CLUSTER_MIN_NODES", min_nodes)
        compute_max_nodes = os.environ.get("AML_COMPUTE_CLUSTER_MAX_NODES", max_nodes)

        # This example uses CPU VM. For using GPU VM, set SKU to STANDARD_NC6
        vm_size = os.environ.get("AML_COMPUTE_CLUSTER_SKU", vm_type)

        print("#### vm_type : ", vm_type)
        if compute_name in ws.compute_targets:
            compute_target = ws.compute_targets[compute_name]
            if compute_target and type(compute_target) is AmlCompute:
                print("found compute target: " + compute_name)
        else:
            print("creating new compute target...")
            provisioning_config = AmlCompute.provisioning_configuration(vm_size = vm_size,
                                                                        min_nodes = compute_min_nodes, 
                                                                        max_nodes = compute_max_nodes,
                                                                        idle_seconds_before_scaledown = idle_seconds)
            # create the cluster
            compute_target = ComputeTarget.create(ws, compute_name.strip(), provisioning_config)
            
            # can poll for a minimum number of nodes and for a specific timeout. 
            # if no min node count is provided it will use the scale settings for the cluster
            compute_target.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)
            
            # For a more detailed view of current AmlCompute status, use get_status()
            print(compute_target.get_status().serialize())
        
        return compute_target

    @staticmethod
    def config_attach(ws,compute_target_name, resource_id,username, password):
        try:
            attached_dsvm_compute = RemoteCompute(workspace=ws, name=compute_target_name)
            print('found existing:', attached_dsvm_compute.name)
        except ComputeTargetException:
            # Attaching a virtual machine using the public IP address of the VM is no longer supported.
            # Instead, use resourceId of the VM.
            # The resourceId of the VM can be constructed using the following string format:
            # /subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Compute/virtualMachines/<vm_name>.
            # You can also use subscription_id, resource_group and vm_name without constructing resourceId.
            
            attach_config = RemoteCompute.attach_configuration(resource_id=resource_id,
                                                                ssh_port=22,
                                                                username=username,
                                                                password=password)
            attached_dsvm_compute = ComputeTarget.attach(ws, compute_target_name.strip(), attach_config)
            attached_dsvm_compute.wait_for_completion(show_output=True)

        return attached_dsvm_compute
       
class DataStoreConfig:
    @staticmethod
    def config(ws, blob_datastore_name,account_name,container_name,account_key):
        
        try:
            blob_datastore = Datastore.get(ws, blob_datastore_name)
            print("Found Blob Datastore with name: %s" % blob_datastore_name)
        except HttpOperationError:
            blob_datastore = Datastore.register_azure_blob_container(
                workspace=ws,
                datastore_name=blob_datastore_name,
                account_name=account_name, # Storage account name
                container_name=container_name, # Name of Azure blob container
                account_key=account_key) # Storage account key
            print("Registered blob datastore with name: %s" % blob_datastore_name)
        
        return blob_datastore

class RunConfigurationProvider:
    @staticmethod
    def get_run_config(ws,compute_target, packages):
        huml_env = Environment("huml-pipeline-env")
        huml_env.python.user_managed_dependencies = False # Let Azure ML manage dependencies
        huml_env.docker.enabled = True # Use a docker container
        # Set Docker base image to the default CPU-based image
        #DOCKER_ARGUMENTS = ["all"]
        #huml_env.docker.arguments = DOCKER_ARGUMENTS
        #huml_env.docker.base_image = "mcr.microsoft.com/azureml/onnxruntime:latest-cuda"

        # Add the dependencies to the environment
        huml_env.python.conda_dependencies = packages

        # Register the environment (just in case you want to use it again)
        huml_env.register(workspace=ws)
        #registered_env = Environment.get(ws, 'huml-pipeline-env')

        # Create a new runconfig object for the pipeline
        pipeline_run_config = RunConfiguration()
        #run_config_user_managed.environment.python.user_managed_dependencies = True

        # Use the compute you created above. 
        pipeline_run_config.target = compute_target

        # Assign the environment to the run configuration
        pipeline_run_config.environment = huml_env

        return pipeline_run_config

class Helper:
    @staticmethod
    def generate(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

class BlobStorageAPIUtilities:
    def __init__(self, base_url = "https://humlstorage.blob.core.windows.net"):
        self.base_url = base_url
    
    def is_file(self, blob_container, blob_name):

        temp = os.path.join(os.getcwd(), "blob_api_temp_555")
        FolderUtilities.make_dir(temp)
        data_downloaded_file = os.path.join(temp, blob_name)
        
        remote_file = "{0}/{1}/{2}".format(self.base_url, blob_container, blob_name)
        
        is_data_file_downloaded =  FileUtilities.direct_download_file(remote_file,data_downloaded_file)
        
        if is_data_file_downloaded == False:
            return False
        
        xx = self._is_blob_not_found(data_downloaded_file)
        
        result = not self._is_blob_not_found(data_downloaded_file)
        
        shutil.rmtree(temp, ignore_errors=True)

        return result


    def download_file(self, blob_container, blob_name, data_downloaded_file):
        #Helper
        #temp = os.path.join(os.getcwd(), Helper.id_generator())
        FolderUtilities.make_dir(os.path.dirname(data_downloaded_file))
        #local_data_downloaded_file = os.path.join(temp, blob_name)
        remote_file = "{0}/{1}/{2}".format(self.base_url, blob_container, blob_name)
        is_data_file_downloaded =  FileUtilities.direct_download_file(remote_file,data_downloaded_file)
        return is_data_file_downloaded


    def _is_blob_not_found(self, file_path):
        file = open(file_path,'r')
        root = None
        try:
            root = ET.fromstring(file.read())
        except Exception as e:
            print("Impossible to parse XML fle.", e)
        finally:
            file.close()
        
        if not root:
            return False
        
        if root[0].text == "BlobNotFound":
            return True
        return False

class BlobStorageManager:
    def __init__(self, connection_string):
        
        self.connection_string = connection_string
        # Create the BlobServiceClient object which will be used to create a container client
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def upload(self,blob_container,  file_path, overwrite_v = False):
        """Upload the file to the Blob Storage 

        Arguments:
            blob_container {str} -- container (or folder) in blob storage 
            file_path {str} -- local file path

        Keyword Arguments:
            overwrite_v {bool} -- whether or not to overwrite the existing file on the blob storage (default: {False})
        """

        file_name = ntpath.basename(file_path)
                
        # Create a blob client using the local file name as the name for the blob
        blob_client = self.blob_service_client.get_blob_client(container=blob_container, blob=file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + file_name)

        # Upload the created file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data,overwrite=overwrite_v)
        
    def delete(self,blob_container,  file_path):
        """deletes the file from the blob storage

        Arguments:
            blob_container {str} -- container (or folder) in blob storage 
            file_path {str} -- [description]
        """

        if os.path.isabs(file_path):
            file_name = ntpath.basename(file_path)
        else:
            file_name = file_path
        # Create a blob client using the local file name as the name for the blob
        blob_client = self.blob_service_client.get_blob_client(container=blob_container, blob=file_name)

        print("\Deleting from Azure Storage:\n\t" + file_name)

        # Upload the created file
        blob_client.delete_blob()
    
    def download_text_by_url(self, file_path):
        """download the file from the http link

        Arguments:
            file_path {str} -- http link

        Returns:
            str -- downloaded file content
        """
        data = None
        try:
            response = urllib.request.urlopen(file_path)
            data = response.read().decode('utf-8')
        except HTTPError as e:
            # do something
            print('Error code: ', e.code)
        except URLError as e:
            # do something
            print('Reason: ', e.reason)
        except Exception as e:
            # do something
            print('Reason: ', e)

        return data

    def download_json_by_url(self, file_path):
        data = {}
        try:
            response = urllib.request.urlopen(file_path)
            data = json.loads(response.read())
        except HTTPError as e:
            # do something
            print('Error code: ', e.code)
        except URLError as e:
            # do something
            print('Reason: ', e.reason)

        return data

    def download_blob2(self, blob_container, blob_name, dest_file):
        blob = BlobClient.from_connection_string(conn_str=self.connection_string, 
                                                    container_name=blob_container, 
                                                    blob_name=blob_name)
        with open(dest_file, "wb") as my_blob:
            blob_data = blob.download_blob()
            print(blob_data)
            #my_blob.writelines(blob_data.content_as_bytes())
            blob_data.readinto(my_blob)

        #dest_content = None
        
        return  my_blob

    

    """
    def download_blob4(self):
        block_blob_service = BlockBlobService(account_name="", account_key="")
        return block_blob_service
    """

class PipelinePublisher:
    def __init__(self, ws):
        self.ws = ws
    
    def publish(self, experiment_name,pipeline_name):
        """Publish an experiment from name and the last Run that has just performed

        Arguments:
            experiment_name {str} -- The name of the experiment in the workspace...
            pipeline_name {str} --The name of the published pipeline

        Returns:
            str --pipeline id published, str --endpoint : http address through which the pipeline can be called
        """
        
        pipeline_experiment = self.ws.experiments.get(experiment_name)
        run = list(pipeline_experiment.get_runs())[0]
       
        published_pipeline = run.publish_pipeline(name = pipeline_name, description='pipelines', version="2.1")

        #return published_pipeline.id, published_pipeline.endpoint
        return published_pipeline

class EndpointPipelinePublisher:
    def __init__(self, ws):
        self.ws = ws
    
    def publish(self, experiment_name,pipeline, pipeline_name,pipeline_endpoint_name):
        pipeline_endpoint = None
        try:
            pipeline_endpoint = PipelineEndpoint.get(workspace=self.ws, name=pipeline_endpoint_name)
        except Exception as e:
            s = str(e)
            if not "BadRequest" in s:
                raise Exception(e)

        if not pipeline_endpoint:
            pipeline_endpoint = PipelineEndpoint.publish(workspace=self.ws,
                                                        name=pipeline_endpoint_name,
                                                        pipeline=pipeline,
                                                        description="New Pipeline Endpoint for {0}".format(pipeline_endpoint_name))
            published_endpoint = pipeline_endpoint.endpoint
            
        else:
            publisher = PipelinePublisher(self.ws)
            published_pipeline = publisher.publish(experiment_name, pipeline_name)
            
            pipeline_endpoint.add_default(published_pipeline)
            published_endpoint = published_pipeline.endpoint
            
        return published_endpoint

class LogicAppPipelineConfigManager:
    def __init__(self, config):
        """Initializing class with the config object.
            
        Arguments:
            config {object} -- Object containing all the information in the yaml configuration file
        """

        # BlobStorageManager object is created from the connectionstring coming from config object.
        self.blobManager = BlobStorageManager(config.BLOB_STORAGE_CONNECTION_STRING)
        # declaration of file name that will contain the endpoint that has just been published.
        #self.REMOTE_FILE_NAME = "published_pipeline.json"
        # declaration of container (or folder) which will contain the json file
        self.BLOB_CONTAINER = "{0}/configs".format(config.CONTAINER_NAME)
        #http link where the json file will be deposited
        #self.file_url = "https://humlstorage.blob.core.windows.net/{0}/{1}".format(self.BLOB_CONTAINER,self.REMOTE_FILE_NAME)
    
    def update(self, pipelineid, pipeline_endpoint, pipeline_file_name):
        """ Create or update json file of the pipeline in the blob storage

        Arguments:
            pipelineid {str} -- pipeline id published
            pipeline_endpoint {str} --endpoint : http address through which the pipeline can be called
        """
        
        file_url = "https://humlstorage.blob.core.windows.net/{0}/{1}".format(self.BLOB_CONTAINER, pipeline_file_name)

        data = self.blobManager.download_json_by_url(file_url)

        data["pipelineid"] = pipelineid
        data["published_pipeline_endpoint"] = pipeline_endpoint

        temp = "./temp"
        FolderUtilities.make_dir(temp)

        temp_file = os.path.join(temp, pipeline_file_name)

        with open(temp_file, 'w') as outfile:
            json.dump(data, outfile)

        print("update remote file")
        self.blobManager.upload(self.BLOB_CONTAINER, temp_file, overwrite_v = True)

        shutil.rmtree(temp_file, ignore_errors=True)

class FilesProviders:
    @staticmethod
    def get_path_files(root, exclude_files=[]):
        """[summary]

        Arguments:
            root {[type]} -- [description]

        Keyword Arguments:
            exclude_files {list} -- [description] (default: {[]})

        Returns:
            [type] -- [description]
        """
        result = []
        for root, _, files in os.walk(root):
            for filename in files:
                filepath = join(root, filename)
                dirname = os.path.basename(filepath)
                if dirname in exclude_files:
                    continue
                if filename in exclude_files:
                    continue
                result.append(filepath)

        return result

class WorkspaceProvider:
    def __init__(self, config):
        """Initializing WorkspaceProvider's class from config object

        Arguments:
            config {object} -- Object containing all the invalidations of the yaml config file
        """
        self.config = config
    
    def get_ws(self):
        """Creates the Workspace (ws) using information from config object.

        Returns:
            Workspace -- Defines an Azure Machine Learning resource for managing training and deployment artifacts.
        """
        print("tenant_id:", self.config.SPA_TENANTID)
        print("service_principal_id:", self.config.SPA_APPLICATIONID)
        print("service_principal_password:", self.config.SPA_PASSWORD)
        print("subscription_id:", self.config.SPA_TENANTID)
        print("service_principal_id:", self.config.SPA_APPLICATIONID)
        print("service_principal_password:", self.config.SPA_PASSWORD)
        svc_pr = ServicePrincipalAuthentication(
                            tenant_id=self.config.SPA_TENANTID,
                            service_principal_id=self.config.SPA_APPLICATIONID,
                            service_principal_password=self.config.SPA_PASSWORD)

        
        ws = Workspace(subscription_id=self.config.SUBSCRIPTION_VALUE,
                            resource_group=self.config.RESOURCEGROUP,
                            workspace_name=self.config.WORKSPACENAME,
                            auth=svc_pr
                )
        return ws, svc_pr

class PlotUtilities:
    @staticmethod
    def plot_distributed_data(df, col):
        """Plot distribution of data from a column having discrete data

        Arguments:
            df {dataframe} -- dataframe having the data
            col {str} -- column with discrete values used

        Returns:
            plot -- plot fig
        """
        plt.clf()
        dist = df.groupby([col]).size()
        dist = dist / dist.sum()
        fig, _ = plt.subplots(figsize=(12,8))
        sns.barplot(dist.keys(), dist.values)
        return fig
    
    @staticmethod
    def _get_confusion_matrix_plot(cm):
        """plot confusion matrix

        Arguments:
            cm {array} -- array that contains the data of confusion matrix

        Returns:
            plot -- plot fig
        """
        plt.clf()
        plt.imshow(cm, interpolation='nearest', cmap = plt.cm.Wistia) # pylint: disable=no-member
        classNames = ['Positive', 'Negative']
        plt.title('Confusion Matrix')
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        tick_marks = np.arange(len(classNames))
        plt.xticks(tick_marks, classNames, rotation=45)
        plt.yticks(tick_marks, classNames)

        plt.text(0, 0, 'TP' + " = " + str(cm[0][0]))
        plt.text(1, 0, 'FP' + " = " + str(cm[0][1]))
        plt.text(0, 1, 'FN' + " = " + str(cm[1][0]))
        plt.text(1, 1, 'TN' + " = " + str(cm[1][1]))

        return plt

class AzureMLLogsProvider:
    def __init__(self, run):
        self.run = run
    
    def get_log_from_brother_run(self, script_name, log_name):
        if not self.run.parent :
            raise Exception("this run has not parent")
        
        log_value = None
        
        for brother_run in self.run.parent.get_children():
            if brother_run.get_details()["runDefinition"]["script"] != script_name:
                continue
            run_metrics = brother_run.get_metrics()
            
            if log_name in run_metrics:
                log_value = run_metrics[log_name]
                print("log_value :", log_value)

        return  log_value
    
    def get_tag_from_brother_run(self, script_name, tag_name):
        if not self.run.parent :
            raise Exception("this run has not parent")

        tag_value = None
        for brother_run in self.run.parent.get_children():
            if brother_run.get_details()["runDefinition"]["script"] != script_name:
                continue
            run_tags = brother_run.get_tags()
            
            if tag_name in run_tags:
                tag_value = run_tags[tag_name]
                print("tag_value :", tag_value)

        #check if bool
        if (tag_value == "True"):
            tag_value = True
        elif (tag_value == "False"):
            tag_value = False

        return  tag_value

class ConfigProvider:
    def __init__(self, config_path):
        self.config_path = config_path

    def _load_data(self):
        with open(self.config_path) as stream:
            data = yaml.safe_load(stream)
        return data
    
    def load(self):
        data = self._load_data()
        #ApplicationInsights
        self.APPLICATION_INSIGHTS_CONNECTION_STRING = data["Azure"]["ApplicationInsights"]["ConnectionString"]

class ConfigGenerator:
    def __init__(self, config_template_file):
        """initializing class with path to the template of config file

        Arguments:
            config_template_file {str} -- path that points to template of the config file
        """
        self.config_template_file = config_template_file

    def by_file(self, config_value_file, confile_fle):
        """[summary]

        Arguments:
            config_value_file {str} -- path that contains file where there are values to replace in the template
            confile_fle {str} -- new config file to be created
        """
        config_template = open(self.config_template_file, "rt").read()
        with open(config_value_file) as fp:
            for line in fp:
                arr = line.split(":")
                config_template = config_template.replace(arr[0].strip(),arr[1].strip())

        with open(confile_fle,'w') as f:
            f.write(config_template)        

    def _keys_from_template(self):
        """returns keys found in the template file ex: azure.amlcompute.clustername

        Returns:
            array -- list of retrieved keys
        """
        keys = []
        with open(self.config_template_file) as fp:
            for line in fp:
                if ":" not in line:
                    continue
                if "{{" in line:
                    arr = line.split(":")
                    key = arr[1].strip()
                    key = key.replace("{{","").replace("}}", "").replace(".", "_")
                    keys.append(key)
        
        return keys

    def _create_config_values(self,args):
        """creation of dictionary containing keys and values for conf file

        Arguments:
            args {array} -- which contains arguments passed in parameters

        Returns:
            {dict} -- contains information that will be in yaml config file.
        """
        config_values = {}
        last_value = 0
        for index, value in enumerate(args):
            if index == 0:
                continue
            if index % 2 != 0:
                last_value = value
            else:
                if value.isnumeric():
                    config_values[last_value] = value
                else:
                    config_values[last_value] = '"' + value + '"'
        
        return config_values

    def _valide_config_values(self,args):
        """ validate information format for new config file

        Arguments:
            args {dict} -- contains information that will be in yaml config file

        Raises:
            TypeError: [description]
            Exception: [description]
            Exception: [description]
        """

        for key in args.keys():

            if "-" not in key:
                raise TypeError("{0} argname must be preceded by '-'".format(key))
        
        key_templates = self._keys_from_template()

        if len(key_templates) != len(args.keys()):
            raise Exception("number of arguments are not sufficient ({0}). {1} are needed. Refer to the config.template.yaml file".format(len(args.keys()), len(key_templates)))
    
        for key in args.keys():
            key = key.replace("-","")
            if key not in key_templates:
                raise Exception("{0} is not a supported key. Refer to the config.template.yaml file".format(key))

    def by_args(self, args, confile_fle):
        """ Generates config file by the arguments passed in parameters 

        Arguments:
            args {array} -- arguments passed in parameters 
            confile_fle {[type]} -- new config file to be created
        """

        config_values = self._create_config_values(args)

        self._valide_config_values(config_values)

        config_template = open(self.config_template_file, "rt").read()

        for key,value in config_values.items():
            key = key.replace("_", ".").replace("-","")
            config_template = config_template.replace("{{" + key + "}}",  value)

        with open(confile_fle,'w') as f:
            f.write(config_template)

class ConfigHandler:
    def get_file(self,config_path):
        """Loading config object to be used in the entire program

        Arguments:
            config_path {str} -- generated config file path

        Returns:
            ConfigProvider -- Object containing all the information in the config file
        """
        config = ConfigProvider(config_path)
        config.load()
        return config

    def generate(self, config_template, config_path):
        configGen = ConfigGenerator(config_template)

        # If it run locally, then we're going to use the config.values.txt 
        # file containing all the necessary information
        if len(sys.argv) == 1:
            configGen.by_file("../../config.values.txt",config_path)
        # If it's launched via DevOps, then the values will be pass as params
        else:
            configGen.by_args(sys.argv, config_path)

class PipelineEndpointLauncher:
    def start(self, ws, svc_pr, endpoint_pipeline, json_data):
        """The PIPELINE_ENDPOINT pipeline is launched through its published REST address.
        """
        #workspaceProvider = WorkspaceProvider(self.config)
        #ws,svc_pr = workspaceProvider.get_ws()
        auth_header = svc_pr.get_authentication_header()
        pipeline_endpoint_by_name = PipelineEndpoint.get(workspace=ws, name=endpoint_pipeline)
        rest_endpoint = pipeline_endpoint_by_name.endpoint
        print("pipeline_endpoint_by_name.endpoint : ", rest_endpoint)
        _ = requests.post(rest_endpoint, headers=auth_header, json=json_data)

class BlobStorageManagerMoq:
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    def upload(self,blob_container,  file_path, overwrite_v = False):
        #shutil.copy2(file_path, blob_container)
        print("upload simulated")

class AzureExperimentMoq:
    def __init__(self):
        self.runs = []

    def get_runs(self):
        return self.runs

class AzureMLRunMoq:
    def __init__(self, parent):
        self.parent = parent

        self.children = []
        self.json_data = {}
        self.tags = {}
        self.metrics = {}

    def get_children(self):
        return self.children
    
    def get_details(self):
        return self.json_data
    
    def get_tags(self):
        return self.tags
    
    def get_metrics(self):
        return self.metrics
    
    def log(self, title, value):
        print("title :", title)
        print("value :", value)
    
    def tag(self, title, value):
        print("title :", title)
        print("value :", value)

    def log_image(self, title, plot):
        print("tile:", title)
        print("plot :", plot)
        id = Helper.generate()
        if self.temp_dir:
            plot.savefig(os.path.join(self.temp_dir,"{0}_{1}.png".format(title, id)))
    
    def upload_file(self, name, path_or_stream):
        print("name :", name)
        print("path_or_stream :", path_or_stream)
    
    def set_temp_dir(self, temp_dir):
        self.temp_dir = temp_dir

class LoggerMoq(object):
    def info(self, value, args={}):
        print(value)

    def warning(self, value, args={}):
        print(value)
    
    def debug(self, value, args={}):
        print(value)

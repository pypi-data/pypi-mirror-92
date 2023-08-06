# deploy.py
import os
from importlib import import_module
import shutil
import sys
import subprocess

from mlops_settings import model_names, model_files, model_req_files
from mlops_settings import model_artifact_folders, infos, model_test_files
from akerbp.mlops.cdf.helpers import deploy_function, test_function 
from akerbp.mlops.cdf.helpers import download_model_version, set_up_cdf_client
from akerbp.mlops.utils import logger 

logging=logger.get_logger(name='MLOps')

# Read environmental variables
ENV = os.environ['ENV'] # Must be set
SERVICE_NAME = os.environ['SERVICE_NAME']
LOCAL_DEPLOYMENT = os.getenv('LOCAL_DEPLOYMENT') # Optional


def replace_string_file(s_old, s_new, file):
    with open(file) as f:
        s = f.read()
        if s_old not in s:
            logging.warning(f"Didn't find '{s_old}' in {file}")

    with open(file, 'w') as f:
        s = s.replace(s_old, s_new)
        f.write(s)


def set_test_mlops_import(req_file):
    # Some packages may not available in testpypi, so we give the standard
    # index as alternative
    old = 'akerbp.mlops'
    new = """
    -i https://test.pypi.org/simple
    --extra-index-url https://pypi.org/simple
    akerbp.mlops
    """
    replace_string_file(old, new, req_file)
    logging.debug("Modified requirements.txt to install test akerbp.mlops")

# Set CDF client
set_up_cdf_client()

model_settings = zip(
    model_names, 
    model_files, 
    model_req_files, 
    model_artifact_folders,
    infos,
    model_test_files
)

for setting in model_settings:
    (model_name, model_file, model_req_file, model_artifact_folder,
     info, model_test_file) = setting
    
    logging.info(f"Deploy model {model_name}")

    deployment_folder =f'mlops_{model_name}'
    function_name=f"{model_name}-{SERVICE_NAME}-{ENV}"
    get_top_folder = lambda s: s.split(os.sep)[0]
    model_code_folder = get_top_folder(model_file)

    logging.info("Create deployment folder and move required files/folders")
    os.mkdir(deployment_folder)
    logging.debug("model code => deployment folder")
    shutil.copytree(
        model_code_folder, 
        os.path.join(deployment_folder, model_code_folder), 
        dirs_exist_ok = True
    )
    logging.debug("user settings => deployment folder")
    shutil.copyfile(
        'mlops_settings.py', 
        os.path.join(deployment_folder, 'mlops_settings.py')
    )
    logging.debug("handler => deployment folder")
    from akerbp import mlops
    mlops_path = mlops.__path__._path[0]
    handler_path = os.path.join(mlops_path, SERVICE_NAME, 'handler.py')
    shutil.copyfile(
        handler_path,
        os.path.join(deployment_folder, 'handler.py')
    )
    
    if (
        ENV=='dev' and 
        SERVICE_NAME == 'prediction' and 
        os.path.isdir(model_artifact_folder)
    ):
        logging.info("artifact folder => deployment folder")
        shutil.copytree(
            model_artifact_folder, 
            os.path.join(deployment_folder, model_artifact_folder)
        )    

    logging.debug(f"cd {deployment_folder}")
    base_path = os.getcwd()
    os.chdir(deployment_folder)

    if SERVICE_NAME == 'prediction':
        if not os.path.isdir(model_artifact_folder):
            # This will always be executed in the test and prod env, assuming 
            # artifact folder is not committed to repo
            logging.info("Download serialized model")
            os.mkdir(model_artifact_folder)
            model_id = download_model_version(
                model_name, 
                ENV, 
                model_artifact_folder)
        elif ENV=='dev':
            logging.info(f"Use model artifact models {model_artifact_folder=}")
            model_id=f'{model_name}/dev/1'
        else:
            raise Exception("Model artifact folder in Test or Prod")
    else:
        model_id = None

    logging.info("Write settings file for the deployed function")
    model_import_path = model_file.replace(os.sep,'.').replace('.py','')
    if model_test_file:
        test_import_path = model_test_file.replace(os.sep,'.').replace('.py','')
    else:
        test_import_path = None
    mlops_settings=dict(
        model_name=model_name,
        model_artifact_folder=model_artifact_folder,
        model_import_path=model_import_path,
        model_code_folder=model_code_folder,
        env=ENV,
        model_id=model_id,
        test_import_path=test_import_path
    )
    # File name can't be mlops_settings.py, or there will be importing errors
    # during CDF deployment
    with open('service_settings.py', 'w') as config:
        config.write(f'{mlops_settings=}')
    
    logging.info("Create CDF requirement file")
    shutil.move(model_req_file, 'requirements.txt')

    if ENV in ["dev", "test"]:
        set_test_mlops_import('requirements.txt')
    
    if ENV != "dev":
        logging.info(f"Install python requirements from model {model_name}")
        subprocess.check_call(["pip", "install", "-r", 'requirements.txt'])

    # Important to run tests after downloading model artifacts, in case they're 
    # used to test prediction service
    if model_test_file:
        logging.info("Run tests")
        subprocess.check_call([
            sys.executable, 
            "-m", "pytest", 
            model_test_file
        ])
        mlops_test_path = 'akerbp.mlops.tests'
        subprocess.check_call([
            sys.executable, 
            "-m", "pytest", 
            "--pyargs", mlops_test_path
        ])
    else:
        logging.warning("Model test file is missing!")
    
    logging.info(f"Deploy {function_name} to CDF")
    if ENV != "dev" or LOCAL_DEPLOYMENT:
        logging.info("Deploy function")
        deploy_function(
            function_name, 
            info=info[SERVICE_NAME]
        )
        
        if test_import_path:
            logging.info("Test call")
            ServiceTest=import_module(test_import_path).ServiceTest  
            input = getattr(ServiceTest(), f"{SERVICE_NAME}_input")
            test_function(function_name, input)
        else:
            logging.warning("No test file was set up. End-to-end test skipped!")
    
    logging.debug(f"cd ..")
    os.chdir(base_path)
    logging.debug(f"Delete deployment folder")
    shutil.rmtree(deployment_folder)
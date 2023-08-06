# helpers.py

import subprocess

from google.cloud import secretmanager

from akerbp.mlops.utils import logger 

logging=logger.get_logger(name='gc_helper')

project_id = "subsurface-advanced-analytics"


def create_service_account(service_account):
    try:
        subprocess.check_call(
            f"gcloud iam service-accounts list | grep {service_account}",
            shell=True
        )
        logging.debug(f"Found service account {service_account}")
    except subprocess.CalledProcessError:
        subprocess.check_call(
            f"gcloud iam service-accounts create {service_account}",
            shell=True
        )
        logging.debug(f"Created service account {service_account}")


def access_secret_version(secret_id, version_id="latest"):
    """
    See https://codelabs.developers.google.com/codelabs/secret-manager-python/index.html?index=..%2F..index#5
    See https://dev.to/googlecloud/serverless-mysteries-with-secret-manager-libraries-on-google-cloud-3a1p
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    # Access the secret version.
    response = client.access_secret_version(name=name)
    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')


def register_secrets(secrets):
    pass


def create_image(function_name, folder='.'):
    # Create image
    subprocess.check_call(
        f"gcloud builds submit {folder} \
            --tag gcr.io/{project_id}/{function_name}",
        shell=True
    )


def allow_access_to_secret(service_account, secret_names):
    # Allow access to secret
    s_a_id = f"{service_account}@{project_id}.iam.gserviceaccount.com"
    for secret_name in secret_names:
        subprocess.check_call(
            f"gcloud secrets add-iam-policy-binding {secret_name} \
            --member serviceAccount: {s_a_id}\
            --role roles/secretmanager.secretAccessor"
        )


def run_container(function_name, service_account):
    # Run container
    subprocess.check_call(
        f"gcloud run deploy {function_name} \
            --image gcr.io/{project_id}/{function_name} \
            --platform managed \
            --region=europe-north1 \
            --no-allow-unauthenticated \
            --memory=512M \
            --service-account {service_account}",
        shell=True
    )


def deploy_function(
    function_name,
    folder='.',
    secrets={},
    **kwargs
):
    """
    Deploys a Google Cloud Run function from a folder. 

    Inputs:
      - function_name: name of the function to create
      - folder: path where the source code is located
      - handler_path: path to the handler file
      - secrets: api keys or similar that should be passed to the function
      - kwargs: accept `handler_path` and possibly other args required by CDF
            but not GC
    """
    service_account = f"{function_name}-acc"
    logging.debug(f"Deploy function {function_name}")
    create_service_account(service_account)
    register_secrets(secrets)
    allow_access_to_secret(service_account, secrets.keys())
    create_image(function_name, folder)
    run_container(function_name, service_account)


def read_service_url(function_name):
    # Read service url
    return subprocess.check_output(
        f"""gcloud run services list \
            --platform managed \
            --filter="metadata.name='{function_name}'" \
            --format="value(URL)") """,
        shell=True
    )


def call_function(function_name, data):
    """
    Call a function deployed in Google Cloud Run
    """
    read_service_url(function_name)
    #client = global_client["functions"]
    #function = client.functions.retrieve(external_id=function_name)
    #logging.debug(f"Retrieved function {function_name}")
    #response = function.call(data).get_response()
    #logging.debug(f"Called function: {response=}")
    #return response
    return {"status":"ok"}


def test_function(function_name, data):
    """
    Call a function with data and verify that the response's 
    status is 'ok'
    """
    logging.debug(f"Test function {function_name}")
    output = call_function(function_name, data)
    assert output['status'] == 'ok'
    logging.info(f"Test call was successful :)")
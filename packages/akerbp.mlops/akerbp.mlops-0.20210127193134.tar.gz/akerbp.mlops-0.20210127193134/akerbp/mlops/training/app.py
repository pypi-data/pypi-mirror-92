# model_service.py

from fastapi import FastAPI

from mlops.gc.helpers import access_secret_version
from mlops.training_gc.service import service
from mlops.utils import logger

logging=logger.get_logger()

app = FastAPI()

#secrets = access_secret_version('mlops-demo-cdf-key') 
secrets = {}
service = lambda x,y: {'status':'ok'}

@app.post(f'/train')
def api(data: dict):
    try:
        return service(data, secrets)
    except Exception as error:
      error_type = type(error).__name__
      error_message = f" Training service failed. {error_type}: {error}"
      logging.critical(error_message)
      return dict(status='error', error_message=error_message)

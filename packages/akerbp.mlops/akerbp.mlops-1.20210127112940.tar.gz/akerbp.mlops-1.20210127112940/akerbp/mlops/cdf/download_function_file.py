# download_function_file.py

import os

from akerbp.mlops.cdf.helpers import download_file 


if __name__ == "__main__":
    """
    Read env vars and call the download file function
    """
    
    api_key_file = os.environ['COGNITE_API_KEY_FILES']
    id = int(os.environ['FUNCTION_FILE_ID'])
    path = os.environ['FILE_PATH']
    
    download_file(api_key_file, dict(id=id), path)
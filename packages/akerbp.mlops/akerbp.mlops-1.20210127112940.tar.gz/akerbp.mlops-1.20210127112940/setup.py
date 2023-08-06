"""
setup.py 

Information used to build the package
"""
from setuptools import find_namespace_packages, setup
from datetime import datetime
import os


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

def get_version():
    ENV = os.environ['ENV'] # Must be set
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    if ENV in ['dev', 'test']:
        version = '0.' + date
    elif ENV == 'prod':
        version = '1.' + date

    return version

setup(
    name="akerbp.mlops", 
    version=get_version(),
    author="Alfonso M. Canterla",
    author_email="alfonso.canterla@soprasteria.com",
    description="MLOps framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/akerbp/mlops/",
    packages=[
        p for p in find_namespace_packages(where='.') 
        if 'model' not in p
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["cognite-sdk-experimental>=0.34.0", "pytest>=6.1.1"],
    scripts=[
        'akerbp/mlops/deploy_training_service.sh', 
        'akerbp/mlops/deploy_prediction_service.sh'
    ],
    python_requires='>=3.8',
)
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "0.1.0b0"
REQUIRES_PYTHON = ">=3.7.0"
REQUIRED = [
    "black == 22.6.0",
    "pytest == 7.1.2",
    "PyYAML == 5.4",
    "google-api-python-client == 2.78.0",
    "google-cloud-core == 2.3.2",
    "google-cloud-storage == 2.7.0",
    "zstd == 1.5.2.6",
    "boto == 2.49.0",
    "botocore == 1.29.127",
    "boto3 == 1.26",
    "docker == 6.1.2",
    "redis == 4.5.5",
]
DEV_REQUIRED = [
    "black >= 22.6.0",
    "pytest >= 7.1.2",
    "typer >= 0.6.0",
    "PyYAML >= 5.4.1",
]


setup(
    name="airdot",
    url="https://github.com/Abhinavfreecodecamp/ml-deployer-os",
    author="Abhinav Singh",
    author_email="abhhinav035991@gmail.com",
    packages=find_packages(),
    version=VERSION,
    description="A code base for deploying python functions",
    long_description=long_description,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
)

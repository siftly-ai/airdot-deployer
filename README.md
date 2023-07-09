# Airdot deployer


[![Python](https://img.shields.io/badge/PythonVersion-3.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


**Airdot deployer [Beta]** Tool to take your ml model live right from your jupyter notebook. No need to save model and upload anywhere, airdot-deploy takes care of everything including and not limited to getting your code, requirements, data objects. 

**Note - Before proceeding make sure you have installed docker and docker-compose and s2i.if not please follow the steps below**

#### Docker install 

```bash
# for mac please visit https://docs.docker.com/desktop/install/mac-install/
# for windows please visit https://docs.docker.com/desktop/install/windows-install/
# for linux please visit https://docs.docker.com/desktop/install/linux-install/
```

#### s2i install
For Mac
You can either follow the installation instructions for Linux (and use the darwin-amd64 link) or you can just install source-to-image with Homebrew:

```$ brew install source-to-image```

For Linux just run following command

```bash
curl -s https://api.github.com/repos/openshift/source-to-image/releases/latest| grep browser_download_url | grep linux-amd64 | cut -d '"' -f 4  | wget -qi -
```
For Windows plese follow instruction [here](https://github.com/openshift/source-to-image#for-windows)


## How to install

```bash
pip install "git+https://github.com/airdot-io/airdot-Deploy.git@main#egg=airdot"
```

## or

```bash
# pypi uri will be added soon
```

### How to Use for local deployments

#### Setup local minio and redis in your machine

```bash
# run this in terminal.
docker network create minio-network && wget  https://raw.githubusercontent.com/airdot-io/airdot-Deploy/main/docker-compose.yaml && docker-compose -p airdot up
```

#### Deployment on local

```python
from airdot import Deployer
import pandas as pd

config = {
    'deployment_type':'test',
    'bucket_type':'minio'
}
deployer = Deployer(deployment_configuration=config) 

# declare a ML function 
df2 = pd.DataFrame(data=[[10,20],[10,40]], columns=['1', '2'])
def get_value_data(cl_idx='1'):
    return df2[cl_idx].values.tolist()

deployer.run(get_value_data)
```

#### you will see output something like this

```bash
deployment started
test deployment, switching to local minio bucket
df2.pkl uploaded successfully and available at get-value-data/df2.pkl
switching to test deployment no deployment configuration is provided.
deploying on port: 8000
deployment ready, access using the curl command below
curl -XPOST http://127.0.0.1:8000 -H 'Content-Type: application/json' -d '{"cl_idx": "<value-for-argument>"}' 
```

#### How to stop local deployments

```python
deployer.stop('get_value_data') # to stop container
```

#### How to list local deployments

```python
deployer.list_deployments() # to list all deployments
```

#### update objects if any present

```python
df2 = pd.DataFrame(data=[[10,20],[10,40]], columns=['1', '2'])
deployer.update_objects(('df2',df2), 'get_value_data') # to update objects like model or dataframes.
```

**Note - This method use your current cluster and uses seldon-core to deploy**

#### Deployment on k8s using seldon-core deployments

```python
from airdot import Deployer
import pandas as pd

# this is using default seldon-deployment configuration.
config = {
        'deployment_type':'seldon',
        'bucket_type':'minio',
        'image_uri':'<registry>/get_value_data:latest'
        }
deployer = Deployer(deployment_configuration=config) 


df2 = pd.DataFrame(data=[[10,20],[10,40]], columns=['1', '2'])
def get_value_data(cl_idx='1'):
    return df2[cl_idx].values.tolist()

deployer.run(get_value_data) 
```
#### you will see output something like this

```bash
deployment started
test deployment, switching to local minio bucket
df2.pkl uploaded successfully and available at get-value-data/df2.pkl
---> Installing application source...
Build completed successfully
The push refers to repository [docker.io/<registry>/get_value_data]
9b21637b75e4: Pushed
latest: digest: sha256:4785ty4uybrti4ur5tg741 size: 3886
/tmp/1bz517cu4/seldon_model.json
seldondeployment.machinelearning.seldon.io/get-value-data created
Resources applied successfully.
```

#### you can also deploy using seldon custom configuration

```python
from airdot import Deployer
import pandas as pd

# this is using default seldon-deployment configuration.
config = {
        'deployment_type':'seldon',
        'bucket_type':'minio',
        'image_uri':'<registry>/get_value_data:latest',
        'seldon_configuration': '' # your custom seldon configuration
        }
deployer = Deployer(deployment_configuration=config) 


df2 = pd.DataFrame(data=[[10,20],[10,40]], columns=['1', '2'])
def get_value_data(cl_idx='1'):
    return df2[cl_idx].values.tolist()

deployer.run(get_value_data) 
```
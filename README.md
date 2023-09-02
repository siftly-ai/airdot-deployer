# 🚀 Airdot Deployer


[![Python](https://img.shields.io/badge/PythonVersion-3.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Deploy your ML models in **minutes**, not **weeks**.

Detailed documentation can be found [here](https://airdot-io.github.io/airdot-deployer/)

Airdot Deployer will automatically:

1. Restructure your Python code (from Jupyter Notebook/local IDEs) into modules.
2. Builds a REST API around your code.
3. Conterize the app.
4. Spins up the required hardware (local or K8s or cloud).
5. Monitors for model/data drift and performance (in development)

## Take your ML model from Local to Production with one-line of code

```python
from airdot.deployer import Deployer
deployer_obj = Deployer().run(<your-ml-predictor>)
```

Once deployed, your model will be up and running on the intra/internet, accessible to your users. No more worrying about complex server setups or manual configuration. Airdot Deployer does all the heavy lifting for you.

```bash
curl -XPOST <url> -H 'Content-Type: application/json' -d '{"args": "some-value"}'
```

Whether you're a data scientist, developer, or tech enthusiast, Airdot Deployer empowers you to showcase your machine learning prowess and share your creations effortlessly.



## What does Airdot Deployer supports ?

* Local Deployment with Docker ![docker](/icon/docker.png)
* K8s Deployment with seldon core  ![core](/icon/seldon-core.webp)

# Want to try Airdot ? follow setup instructions

## 📋 Setup Instructions

Before we get started, you'll need to have Docker, Docker Compose, and s2i installed on your machine. If you don't have these installed yet, no worries! Follow the steps below to get them set up:


### Docker Install
Please visit the appropriate links to install Docker on your machine:
- For macOS, visit [here](https://docs.docker.com/desktop/install/mac-install/)
- For Windows, visit [here](https://docs.docker.com/desktop/install/windows-install/)
- For Linux, visit [here](https://docs.docker.com/desktop/install/linux-install/)

#### S2I install
For Mac
You can either follow the installation instructions for Linux (and use the darwin-amd64 link) or you can just install source-to-image with Homebrew:

```$ brew install source-to-image```

For Linux just run following command

```bash
curl -s https://api.github.com/repos/openshift/source-to-image/releases/latest| grep browser_download_url | grep linux-amd64 | cut -d '"' -f 4  | wget -qi -
```
For Windows please follow instruction [here](https://github.com/openshift/source-to-image#for-windows)


## 💻 Airdot Deployer Installation
Install the Airdot Deployer package using pip:

```bash
pip install "git+https://github.com/airdot-io/airdot-deployer.git@main#egg=airdot"
```

## or

```bash
pip install airdot
```

## 🎯 Let's try out

### Local Deployments

#### Run following in terminal to setup minio and redis on your machine

```bash
docker network create minio-network && wget  https://raw.githubusercontent.com/airdot-io/airdot-deployer/main/docker-compose.yaml && docker-compose -p airdot up
```

### Train your model

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from airdot.deployer import Deployer
from sklearn import datasets
import pandas as pd
import numpy as np

iris = datasets.load_iris()
iris = pd.DataFrame(
    data= np.c_[iris['data'], iris['target']],
    columns= iris['feature_names'] + ['target']
)
X = iris.drop(['target'], axis=1)
X = X.to_numpy()[:, (2,3)]
y = iris['target']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.5, random_state=42)
log_reg = LogisticRegression()
log_reg.fit(X_train,y_train)
```

### Test your model

```python
def predict(value):
    return log_reg.predict(value)
```

### Deploy in one step 🤯

```python
deployer_obj = Deployer().run(predict)
```

### Use your deployed Model

```bash
curl -XPOST http://127.0.0.1:8000 -H 'Content-Type: application/json' -d '{"value": [[4.7, 1.2]]}'
```

### Want to stop your deployment

```python
deployer.stop('predict') # to stop container
```

## Deployment on k8s using seldon-core deployment

**Note - This method will use your current cluster and uses seldon-core to deploy**

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

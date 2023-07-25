# 🚀 Airdot Deployer


[![Python](https://img.shields.io/badge/PythonVersion-3.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Welcome aboard the Airdot Deployer [Beta] 🛠️, your ultimate one-stop solution for seamlessly transitioning your machine learning models from Jupyter notebooks to the live web 🌐. Bid farewell to the tedious process of manually saving and uploading models. Airdot Deployer serves as the perfect assistant, effortlessly managing everything from code and requirements to data objects and beyond, ensuring a smooth deployment experience like never before.

With Airdot Deployer, you can easily take your trained machine learning models and deploy them with just a few clicks. Imagine the simplicity of selecting your desired model, specifying the necessary dependencies, and hitting the "Deploy" button. The process is as smooth as pouring water.

```python
deployer_obj = Deployer().run(<your-ml-predictor>)
```

Once deployed, your model will be up and running on the web, accessible to users worldwide. No more worrying about complex server setups or manual configuration. Airdot Deployer does all the heavy lifting for you.

```bash
curl -XPOST <url> -H 'Content-Type: application/json' -d '{"value": "some-value"}'
```
Whether you're a data scientist, developer, or tech enthusiast, Airdot Deployer empowers you to showcase your machine learning prowess and share your creations effortlessly. So why wait? Join our beta program now and experience the future of machine learning deployment with Airdot Deployer.

# Want to try Airdot on your machine ?
### Train your model
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from airdot.deployer import Deployer
from sklearn import datasets
import pandas as pd

iris = datasets.load_iris()
iris = pd.DataFrame(
    data= np.c_[iris['data'], iris['target']],
    columns= iris['feature_names'] + ['target']
)
X = iris.drop(['target','species'], axis=1)
X = X.to_numpy()[:, (2,3)]
y = iris['target']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.5, random_state=42)
log_reg = LogisticRegression()
log_reg.fit(X_train,y_train)
```

### Test your model
```python
def predict(value)
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

## What does Airdot supports ?
This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.


* Local Deployment with Docker ![docker](/icon/docker.png)
* K8s Deployment with seldon core  ![docker](/icon/seldon-core.webp)

## 📋 Setup Instructions

Before we get started, you'll need to have Docker, Docker Compose, and s2i installed on your machine.

- **Docker**: Docker is an open-source platform used to automate the deployment, scaling, and management of applications. It does this by isolating applications into containers, allowing them to be portable and consistent across different environments. Docker is essential for running the Airdot Deployer, which operates in a containerized environment.

- **Docker Compose**: Docker Compose is a tool for defining and running multi-container Docker applications. With Compose, you can use a YAML file to configure your application's services, network, and volumes. This allows you to manage complex multi-container applications with ease.

- **s2i (Source-To-Image)**: s2i is a toolkit and workflow for building reproducible Docker images from source code. It injects source code into a Docker container and assembles a new Docker image for your application. This allows Airdot Deployer to handle your code efficiently, packaging it into a Docker container ready for deployment.

- **seldon-core** This is needed to be setup in your k8s. Want to know more about seldon-core and how it can help ? click [here](https://github.com/airdot-io/airdot-Deploy/blob/main/supplement/SELDONCORE.md).

If you don't have these installed yet, no worries! Follow the steps below to get them set up:

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
For Windows plese follow instruction [here](https://github.com/openshift/source-to-image#for-windows)


## 💻 Installation
Install the Airdot Deployer package using pip:

```bash
pip install "git+https://github.com/airdot-io/airdot-Deploy.git@main#egg=airdot"
```

## or

```bash
# pypi uri will be added soon
```

## 🎯 How to Use

### Local Deployments

#### Setup local minio and redis in your machine

```bash
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

[Laravel-url]: https://laravel.com
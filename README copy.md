# Airdot deployer


[![Python](https://img.shields.io/badge/PythonVersion-3.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


**Airdot deployer** Tool to take your ml model live right from your jupyter notebook. Before proceeding make sure you have
installed docker and docker-compose.

**[currently only supports local deployments]**

## How to install

```bash
pip install "git+https://github.com/Abhinavfreecodecamp/ml-deployer-os.git@devel#egg=airdot"
```

## or

```bash
```

### How to Use

```bash
# If using virtual env operator
docker network create minio-network && wget  https://github.com/Abhinavfreecodecamp/ml-deployer-os/blob/master/docker-compose.yaml && docker-compose -p airdot up
```

```python
from airdot import Deployer
import pandas as pd
deployer = Deployer() 


# declare a function
df2 = pd.DataFrame(data=[[10,20],[10,40]], columns=['1', '2'])
def get_value_data(cl_idx='1'):
    return df2[cl_idx].values.tolist()

deployer.run(get_value_data) # to deploy local
```

### How to stop

```python
deployer.stop('get_value_data') # to stop container
```

### How to list deployments

```python
deployer.list_deployments() # to list all deployments
```

### update objects

```python
df2 = pd.DataFrame(data=[[10,20],[10,40]], columns=['1', '2'])
deployer.update_objects(('df2',df2), 'get_value_data') # to update objects like model or dataframes.
```

# Airdot API reference
This page provides detailed documentation of all the methods airdot-deployer provides and how to use them, before moving moving ahead please make sure you have completed setting up airdot.

Using Airdot is actually quite simple and efficient and has not any complex methods which might confuses the user. Airdot has only one class which is `Deployer` rest only are its methods.

## Deployer API
This class is responsible for managing all user operations including.

- start deployment of user ML microservice.
- stop deployment of user ML microservice.
- restart deployment of user ML microservice.
- refresh data objects of user ML microservice.

#### Deployer instantiation

``` py hl_lines="1 2"
>>> from airdot.deployer import Deployer
>>> deployer_obj = Deployer()
```

##### Arguments

- minio_endpoint (str, optional): Local minio endpoint Defaults to `"http://127.0.0.1:9000"`.
- redis_endpoint (str, optional): Local redis endpoint Defaults to "localhost:6379".
- deployment_configuration (dict, optional): _description_. Defaults to { "deployment_type": "test", "bucket_type": "minio", }.

#### run() API

``` py hl_lines="1 2 3"
>>> from airdot.deployer import Deployer
>>> deployer_obj = Deployer()
>>> deployer_obj.run(<callable>)
>>> deployment started
>>> <object>.pkl uploaded successfully and available at <callable>/<object>.pkl
>>> switching to test deployment no deployment configuration is provided.
>>> deploying on port: 8000
>>> deployment ready, access using the curl command below
>>> curl -XPOST http://127.0.0.1:8000 -H 'Content-Type: application/json' -d '{"arg": "<value-for-argument>"}'
```

##### Arguments

- func (Callable): primary function which predicts, this can be model object itself.
- name (Optional[str], optional): service name. Defaults to None.
- python_version (Optional[str], optional): python version to be used for runtime. Defaults to "3.8".
- python_packages (Optional[List[str]], optional): List of python pkgs
    if not provided uses func to get user pakgs. Defaults to None.
- system_packages (Optional[List[str]], optional): Not yet implemented. Defaults to None.

#### build_deployment() API (Only Intended to be used by Advanced users)

``` py hl_lines="1 2 3"
>>> from airdot.deployer import Deployer
>>> deployer_obj = Deployer()
>>> deployer_obj.build_deployment(<callable>)
>>> {'source_file': {'user_name': 'source.py',
>>> 'seldon_name': 'seldon_wrapper.py',
>>> 'seldon_contents': None,
>>> 'user_contents': `{user auto generated ML microservice}`,
>>> 'value_files': {},
>>> 'name': 'predict',
>>> 'data_files': `{<user data objects>}`,
>>> 'module': 'source',
>>> 'arg_names': ['value'],
>>> 'arg_types': {},
>>> 'requirements_txt': 'numpy==1.24.3\npandas==1.5.2\nscikit-learn==1.3.0',
>>> 'python_version': '3.8',
>>> 'system_packages': None,
>>> 'dockerRun': None,
>>> 'func_props':}
```

##### Arguments

- func (Callable): primary function which predicts, this can be model object itself.
- name (Optional[str], optional): service name. Defaults to None.
- python_version (Optional[str], optional): python version to be used for runtime. Defaults to "3.8".
- python_packages (Optional[List[str]], optional): List of python pkgs
    if not provided uses func to get user pakgs. Defaults to None.
- system_packages (Optional[List[str]], optional): Not yet implemented. Defaults to None.


#### stop() API (currently only applicable for local deployments)

``` py hl_lines="1 2 3"
>>> from airdot.deployer import Deployer
>>> deployer_obj = Deployer()
>>> deployer_obj.stop('<str name of the user ML microservice>')
>>> deployment killed successfully
```

##### Arguments

- image_name (str):  name of service
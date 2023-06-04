from typing import List

from airdot.collection.collections import python_function_prop, source_file_props
from airdot.helpers.general_helpers import add_space


def make_soruce_file(
    dir: str, pyProps: python_function_prop, source_file_name: str = "source"
):

    sourceParts: List[str] = [
        "import sys",
        "from flask import escape, jsonify, Flask, request",
        "import pickle",
        "import boto3",
        "app = Flask('ml-deployer')",
    ]
    if pyProps.namespace_froms:
        for iAs, iModule in pyProps.namespace_froms.items():
            sourceParts.append(f"from {iModule} import {iAs}")
    if pyProps.namespace_imports:
        for iAs, iModule in pyProps.namespace_imports.items():
            if iModule == iAs:
                sourceParts.append(f"import {iModule}")
            else:
                sourceParts.append(f"import {iModule} as {iAs}")
    add_space(sourceParts)
    sourceParts.append(
        "client = boto3.resource('s3', endpoint_url='http://airdot-minio-1:9000', aws_access_key_id='minioadmin',aws_secret_access_key='miniopassword')"
    )
    sourceParts.append(f"bucket = client.Bucket('{pyProps.name.replace('_','-')}')")
    if pyProps.namespace_vars and pyProps.namespace_vars_desc:
        for nName, _ in pyProps.namespace_vars.items():
            sourceParts.append(
                f"{nName} = pickle.loads(bucket.Object('{nName}.pkl').get()['Body'].read())"
            )
    if pyProps.custom_init_code:
        sourceParts.append("\n" + "\n\n".join(pyProps.custom_init_code))
    add_space(sourceParts)
    if pyProps.namespace_functions:
        for _, fSource in pyProps.namespace_functions.items():
            sourceParts.append(fSource)
            add_space(sourceParts)
    add_space(sourceParts)

    if pyProps.source:
        sourceParts.append("# main function")
        sourceParts.append(pyProps.source)

    # add calling method
    add_space(sourceParts)
    sourceParts.append("@app.route('/', methods=['POST'])")
    sourceParts.append(f"def main_{pyProps.name}():")
    sourceParts.append("\tdata = request.get_json()")
    sourceParts.append("\tif data is None:")
    sourceParts.append(f"\t\treturn jsonify({pyProps.name}())")
    sourceParts.append("\telse:")
    sourceParts.append(f"\t\treturn jsonify({pyProps.name}(**data))")
    return source_file_props(f"{source_file_name}.py", "\n".join(sourceParts))


def get_docker_template(req_string):
    dockerBuildParts: List[str] = [
        "FROM python:3.8-slim",
        "ENV APP_HOME /app",
        "WORKDIR $APP_HOME",
        "COPY . ./",
        f"RUN pip install {req_string}",
        "CMD exec gunicorn --bind :8080 --workers 1 --threads 8 app:app",
    ]
    return dockerBuildParts

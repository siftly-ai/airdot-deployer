from typing import List

from airdot.collection.collections import python_function_prop, source_file_props
from airdot.helpers.general_helpers import add_space

bucket_type_import = {
    "gcs":"from google.cloud import storage",
    "s3":"import boto3",
    "azure":"import boto3",
    "minio":"import boto3"
}

object_type_import = {

}


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


def make_soruce_file_seldon(
    dir: str, pyProps: python_function_prop, source_file_name: str = "source", bucket_type='gcs', bucket_name = 'seldon-test'
):
    def check_function_template(line):
        return line.startswith("def")

    def add_self_to_function(line):
        if line.startswith("def"):
            temp_str = ""
            for char in line:
                if char == "(":
                    temp_str = temp_str + char + "self, "
                    continue
                temp_str = temp_str + char
        return temp_str

    sourceParts: List[str] = [
        "import sys",
        "from flask import escape, jsonify, Flask, request",
        "import pickle",
        "import logging",
        "from io import BytesIO, StringIO",
        bucket_type_import[bucket_type],
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

    sourceParts.append(f"class {pyProps.name}_class(object):")
    sourceParts.append(f"\tdef __init__(self):")

    add_space(sourceParts)

    if bucket_type is 'gcs':
        sourceParts.append("\t\tstorage_client = storage.Client()")
        sourceParts.append(f"\t\tbucket = storage_client.bucket({bucket_name})")
        if pyProps.namespace_vars and pyProps.namespace_vars_desc:
            for nName, _ in pyProps.namespace_vars.items():
                sourceParts.append(f"\t\t{nName}_blob = bucket.get_blob({nName}.pkl')")
                sourceParts.append(f"\t\tself.{nName} = BytesIO(blob.download_as_bytes())")

    elif bucket_type is 'minio': 
        sourceParts.append(
            "\t\tclient = boto3.resource('s3', endpoint_url='http://airdot-minio-1:9000', aws_access_key_id='minioadmin',aws_secret_access_key='miniopassword')"
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
            sourceParts.append("\t\t"+fSource)
            add_space(sourceParts)
    add_space(sourceParts)

    empty_str = ""
    for line in pyProps.source.split('\n'):
        if check_function_template(line):
            line = add_self_to_function(line)
        line = "\t" + line
        empty_str = empty_str + "\n" + line
    pyProps.source = empty_str

    if pyProps.source:
        sourceParts.append("# main function")
        sourceParts.append(pyProps.source)

    # add calling method
    add_space(sourceParts)
    sourceParts.append(f"\tdef predict(self, data):")
    sourceParts.append(f"\t\treturn self.{pyProps.name}(**data)")
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

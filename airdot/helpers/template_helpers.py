from typing import List

from airdot.collection.collections import python_function_prop, source_file_props
from airdot.helpers.general_helpers import add_space

bucket_type_import = {
    "gcs": "from google.cloud import storage",
    "s3": "import boto3",
    "azure": "import boto3",
    "minio": "import boto3",
}

object_type_import = {}


def make_soruce_file(
    dir: str, pyProps: python_function_prop, source_file_name: str = "source"
):

    source_parts: List[str] = [
        "import sys",
        "from flask import jsonify, Flask, request",
        "import pickle",
        "import boto3",
        "app = Flask('ml-deployer')",
    ]
    if pyProps.namespace_froms:
        for iAs, iModule in pyProps.namespace_froms.items():
            source_parts.append(f"from {iModule} import {iAs}")
    if pyProps.namespace_imports:
        for iAs, iModule in pyProps.namespace_imports.items():
            if iModule == iAs:
                source_parts.append(f"import {iModule}")
            else:
                source_parts.append(f"import {iModule} as {iAs}")
    add_space(source_parts)
    source_parts.append(
        "client = boto3.resource('s3', endpoint_url='http://airdot-minio-1:9000', aws_access_key_id='minioadmin',aws_secret_access_key='miniopassword')"
    )
    source_parts.append(f"bucket = client.Bucket('{pyProps.name.replace('_','-')}')")
    if pyProps.namespace_vars and pyProps.namespace_vars_desc:
        for nName, _ in pyProps.namespace_vars.items():
            source_parts.append(
                f"{nName} = pickle.loads(bucket.Object('{nName}.pkl').get()['Body'].read())"
            )
    if pyProps.custom_init_code:
        source_parts.append("\n" + "\n\n".join(pyProps.custom_init_code))
    add_space(source_parts)
    if pyProps.namespace_functions:
        for _, fSource in pyProps.namespace_functions.items():
            source_parts.append(fSource)
            add_space(source_parts)
    add_space(source_parts)

    if pyProps.source:
        source_parts.append("# main function")
        source_parts.append(pyProps.source)

    # add calling method
    add_space(source_parts)
    source_parts.append("@app.route('/', methods=['POST'])")
    source_parts.append(f"def main_{pyProps.name}():")
    source_parts.append("\tdata = request.get_json()")
    source_parts.append("\tif data is None:")
    source_parts.append(f"\t\treturn jsonify(str({pyProps.name}()))")
    source_parts.append("\telse:")
    source_parts.append(f"\t\treturn jsonify(str({pyProps.name}(**data)))")
    return source_file_props(
        name=f"{source_file_name}.py", user_contents="\n".join(source_parts)
    )


def build_source_template(
    dir: str,
    pyProps: python_function_prop,
    source_file_name: str = "source",
    bucket_type="gcs",
    bucket_name="seldon-test",
):
    source_parts: List[str] = [
        "import sys",
        "from flask import jsonify, Flask, request",
        "import pickle",
        "import logging",
        "from io import BytesIO, StringIO",
        bucket_type_import[bucket_type],
    ]

    # adding custom imports
    if pyProps.namespace_froms:
        for iAs, iModule in pyProps.namespace_froms.items():
            source_parts.append(f"from {iModule} import {iAs}")
    if pyProps.namespace_imports:
        for iAs, iModule in pyProps.namespace_imports.items():
            if iModule == iAs:
                source_parts.append(f"import {iModule}")
            else:
                source_parts.append(f"import {iModule} as {iAs}")

    for _ in range(4):
        add_space(source_parts)
    # adding bucket imports
    if bucket_type is "gcs":
        source_parts.append("storage_client = storage.Client()")
        source_parts.append(
            f"bucket = storage_client.bucket('{pyProps.name.replace('_','-')}')"
        )
        if pyProps.namespace_vars and pyProps.namespace_vars_desc:
            for nName, _ in pyProps.namespace_vars.items():
                source_parts.append(f"{nName}_blob = bucket.get_blob({nName}.pkl')")
                source_parts.append(f"self.{nName} = BytesIO(blob.download_as_bytes())")

    elif bucket_type is "minio":
        source_parts.append(
            "client = boto3.resource('s3', endpoint_url='http://airdot-minio-1:9000', aws_access_key_id='minioadmin',aws_secret_access_key='miniopassword')"
        )
        source_parts.append(
            f"bucket = client.Bucket('{pyProps.name.replace('_','-')}')"
        )
        if pyProps.namespace_vars and pyProps.namespace_vars_desc:
            for nName, _ in pyProps.namespace_vars.items():
                source_parts.append(
                    f"{nName} = pickle.loads(bucket.Object('{nName}.pkl').get()['Body'].read())"
                )
    if pyProps.custom_init_code:
        source_parts.append("\n" + "\n\n".join(pyProps.custom_init_code))
    add_space(source_parts)
    if pyProps.namespace_functions:
        for _, fSource in pyProps.namespace_functions.items():
            source_parts.append(fSource)
            add_space(source_parts)
    add_space(source_parts)

    if pyProps.source:
        source_parts.append("# main function")
        source_parts.append(pyProps.source)
    return source_parts


def make_soruce_file_seldon(
    dir: str,
    pyProps: python_function_prop,
    source_file_name: str = "source",
    bucket_type="gcs",
    bucket_name="seldon-test",
):

    source_parts: List[str] = [
        "import logging",
        f"from {pyProps.name}_source import {pyProps.name}",
    ]

    add_space(source_parts)

    source_parts.append(f"class {pyProps.name}_class(object):")
    source_parts.append(f"\tdef __init__(self):")
    source_parts.append(f"\t\t logging.info('service created ready to serve')")

    add_space(source_parts)

    # add calling method
    add_space(source_parts)
    source_parts.append(f"\tdef predict(self, data):")
    source_parts.append(f"\t\treturn {pyProps.name}(**data)")

    user_source = build_source_template(
        dir, pyProps, source_file_name, bucket_type, bucket_name
    )

    return source_file_props(
        name=f"{pyProps.name}_source.py",
        seldon_contents="\n".join(source_parts),
        user_contents="\n".join(user_source),
    )


def get_docker_template(req_string, source_name):
    dockerBuildParts: List[str] = [
        "FROM python:3.8-slim",
        "ENV APP_HOME /app",
        "WORKDIR $APP_HOME",
        "COPY . ./",
        f"RUN pip install {req_string}",
        f"CMD exec gunicorn --bind :8080 --workers 1 --threads 8 {source_name}:app",
    ]
    return dockerBuildParts

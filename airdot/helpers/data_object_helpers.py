import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2]))

import hashlib
import pickle
from google.cloud import storage
from typing import Dict, Tuple, Any, cast
import zstd
import pprint
import yaml

from google.cloud import storage
from google.oauth2 import service_account
from googleapiclient import discovery
from datetime import timedelta

SCHEMA_VERSION = 1
MAX_DESCRIPTION_SIZE = 5000
NULL_BYTE = b"\x00"

from airdot.helpers.minio_helper import minio_helper


def serialize_zstd(obj) -> Tuple[bytes, str, int]:
    pkl_data = pickle.dumps(obj)
    content_hash = f"sha1:{hashlib.sha1(pkl_data).hexdigest()}"
    obj_size = len(pkl_data)
    return (pkl_data, content_hash, obj_size)


def is_binary_file(content: bytes) -> bool:
    return NULL_BYTE in content


def decode_string(b: bytes) -> str:
    for encoding in ("ascii", "utf8", "latin1"):
        try:
            return b.decode(encoding)
        except UnicodeDecodeError:
            pass
    return b.decode("ascii", "ignore")


def describe_object(
    obj: Any, max_depth: int, remaining_characters=MAX_DESCRIPTION_SIZE
) -> Dict[str, Any]:
    objT = type(obj)
    if objT is dict and max_depth > 0:
        ret = {}
        for k, v in obj.items():
            ret[k] = describe_object(v, max_depth - 1, max(0, remaining_characters))
            remaining_characters -= len(str(ret[k]))
        return ret
    elif objT is bytes:
        if is_binary_file(obj):
            obj = "Unknown binary file"
        else:
            obj = decode_string(obj)
            objT = type(obj)
    description = (
        obj[:remaining_characters].strip()
        if type(obj) is str
        else pprint.pformat(obj, depth=1, width=100, compact=True)[
            :remaining_characters
        ].strip()
    )
    return {
        "module": objT.__module__,
        "class": objT.__name__,
        "description": description,
    }


def repr_str(dumper: yaml.Dumper, data: str):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def to_file_stub_dict(content_hash: str, obj_desc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "_": "MBFileStub",
        "content_hash": content_hash,
        "metadata": obj_desc,
        "schemaVersion": SCHEMA_VERSION,
    }


def to_yaml(content_hash: str, fileSize: int, obj_desc: Dict[str, Any]) -> str:
    metadata: Dict[str, Any] = {"file_size": fileSize, "object": obj_desc}

    obj = to_file_stub_dict(content_hash, metadata)
    yaml.add_representer(str, repr_str)
    return yaml.dump(obj, width=1000)


def put_secure_data(bucket_id, open_id, data: bytes, desc: str, endpoint: str):
    try:
        minio_helper_obj = minio_helper(endpoint=endpoint)
        minio_helper_obj.create_bucket(bucket_name=bucket_id)
        minio_helper_obj.put_object(bucket=bucket_id, key=f"{desc}.pkl", data=data)
        return True
    except Exception as e:
        print(f"failed to upload data object. Please try again {e}")
        return False


def upload_runtime_object(bucket_id, open_id, obj, desc: str, endpoint: str):
    (data, content_hash, obj_size) = serialize_zstd(obj)
    response = put_secure_data(bucket_id, open_id, data, desc, endpoint)
    if response:
        yamlObj = to_yaml(content_hash, obj_size, describe_object(obj, 1))
        return yamlObj  # need to think a way to save complete yamlObj
    else:
        return "None"


# uploading
def make_and_upload_data_files(bucket_id, open_id, py_state, endpoint):
    dataFiles: Dict[str, str] = {}
    if py_state.namespace_vars and py_state.namespace_vars_desc:
        for nName, nVal in py_state.namespace_vars.items():
            dataFiles[f"{nName}.pkl"] = upload_runtime_object(
                bucket_id, open_id, nVal, nName, endpoint
            )
    return dataFiles

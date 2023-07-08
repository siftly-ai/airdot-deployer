# python imports
from typing import Dict, List, Any, Optional
from datetime import datetime


class namespace:
    def __init__(self):
        self.functions: Dict[str, str] = {}
        self.vars: Dict[str, Any] = {}
        self.imports: Dict[str, str] = {}
        self.froms: Dict[str, str] = {"*": "typing"}
        self.all_modules: List[str] = []
        self.custom_init_code: List[str] = []


class python_function_prop:
    exclude_from_dict: List[str] = ["errors"]

    def __init__(self):
        self.source: Optional[str] = None
        self.name: Optional[str] = None
        self.arg_names: Optional[List[str]] = None
        self.arg_types: Optional[Dict[str, str]] = None
        self.namespace_vars_desc: Optional[Dict[str, str]] = None
        self.namespace_functions: Optional[Dict[str, str]] = None
        self.namespace_imports: Optional[Dict[str, str]] = None
        self.namespace_froms: Optional[Dict[str, str]] = None
        self.namespace_modules: Optional[List[str]] = None
        self.errors: Optional[List[str]] = None
        self.namespace_vars: Optional[Dict[str, Any]] = None
        self.custom_init_code: Optional[List[str]] = None


class authentication:
    def __init__(self) -> None:
        self.refresh_token: Optional[str] = None
        self.token_time: Optional[datetime] = datetime(2000, 1, 1)


class source_file_props:
    def __init__(
        self, user_contents: str, seldon_contents: str = None, name: str = "source.py"
    ):
        self.seldon_name = "seldon_wrapper.py"
        self.user_name = name
        self.seldon_contents = seldon_contents
        self.user_contents = user_contents

    def as_dict(self):
        return {
            "user_name": self.user_name,
            "seldon_name": self.seldon_name,
            "seldon_contents": self.seldon_contents,
            "user_contents": self.user_contents,
        }

import inspect
from typing import Callable, Any, List, Dict
import tempfile, os
import ast
import re

from airdot.collection.collections import namespace, python_function_prop


def get_function_properties(func, imported_modules):
    props = python_function_prop()
    if not callable(func):
        raise Exception("Object is not a callable function")
    else:
        props.name = func.__name__
        props.source = get_function_source_code(func)
        props.arg_names = get_func_args_name(func)
        props.arg_types = annotation_to_type_str(func.__annotations__)
        ns_collection = namespace()
        ns_collection = get_function_dep(func, ns_collection, imported_modules)
        props.namespace_functions = ns_collection.functions
        props.namespace_vars = ns_collection.vars
        props.namespace_vars_desc = get_string_values(ns_collection.vars)
        props.namespace_imports = ns_collection.imports
        props.namespace_froms = ns_collection.froms
        props.namespace_modules = list(set(ns_collection.all_modules))
        props.custom_init_code = ns_collection.custom_init_code
    return props


def get_string_values(args: Dict[str, Any]):
    new_dict: Dict[str, str] = {}
    for k, v in args.items():
        str_val = re.sub(r"\s+", " ", str(v))
        if type(v) is bytes:
            str_val = "Binary data"
        elif len(str_val) > 200:
            str_val = str_val[0:200] + "..."
        new_dict[k] = str_val
    return new_dict


def unindent(source: str) -> str:
    leading_whitespaces = len(source) - len(source.lstrip())
    if leading_whitespaces == 0:
        return source
    new_lines = [line[leading_whitespaces:] for line in source.split("\n")]
    return "\n".join(new_lines)


def get_function_source_code(func: Callable = None):
    if not callable(func):
        return None
    return unindent(inspect.getsource(func))


def get_func_args_name(func: Callable = None):
    arg_spec = inspect.getfullargspec(func)
    if arg_spec.varargs:
        return ["..."]
    if arg_spec.args:
        return arg_spec.args
    noArgs: List[str] = []
    return noArgs


def annotation_to_type_str(annotations: Dict[str, Any]):
    anno_strs: Dict[str, str] = {}
    for name, t_class in annotations.items():
        try:
            if t_class == Any:
                anno_strs[name] = "Any"
            else:
                anno_strs[name] = t_class.__name__
        except:
            pass
    return anno_strs


def has_state(obj: Any) -> bool:
    try:
        return len(obj.__dict__) > 0
    except:
        return False


def collect_byte_obj(
    maybe_func_var: Any, maybe_func_var_name: str, collection: namespace
):
    tmp_file_path = os.path.join(tempfile.gettempdir(), "btyd.pkl")
    maybe_func_var.save_model(tmp_file_path)
    with open(tmp_file_path, "rb") as f:
        collection.vars[maybe_func_var_name + "_state"] = f.read()
    collection.custom_init_code.append(
        f"""
    with open('data/{maybe_func_var_name}_state.tmp', 'wb') as fo:
    with open('data/{maybe_func_var_name}_state.pkl', 'rb') as fi:
    fo.write(pickle.load(fi))
    {maybe_func_var_name} = {maybe_func_var.__class__.__name__}()
    {maybe_func_var_name}.load_model('data/{maybe_func_var_name}_state.tmp')
    """.strip()
    )
    collection.froms[maybe_func_var.__class__.__name__] = maybe_func_var.__module__
    collection.imports["pickle"] = "pickle"
    collection.imports["btyd"] = "btyd"


def is_imported_module(imported_modules, module_name):
    for item in imported_modules:
        pkg_name, _ = item.split("==")
        if pkg_name == module_name:
            return True
    return False


def get_function_dep(func: Callable[..., Any], collection: namespace, imported_modules):
    if not callable(func):
        return collection
    collection = get_function_args(func, collection)
    globalsDict = func.__globals__  # type: ignore
    allNames = func.__code__.co_names + func.__code__.co_freevars
    for maybe_func_var_name in allNames:
        if maybe_func_var_name in globalsDict:
            maybe_func_var = globalsDict[maybe_func_var_name]
            if "__module__" in dir(maybe_func_var):
                if maybe_func_var.__module__ == "__main__":
                    arg_names = list(maybe_func_var.__code__.co_varnames or [])
                    funcSig = f"{maybe_func_var.__name__}({', '.join(arg_names)})"
                    if funcSig not in collection.functions:
                        collection.functions[funcSig] = inspect.getsource(
                            maybe_func_var
                        )
                        get_function_dep(maybe_func_var, collection, imported_modules)
                else:
                    if inspect.isclass(maybe_func_var):
                        collection.froms[
                            maybe_func_var_name
                        ] = maybe_func_var.__module__  #
                        collection.all_modules.append(maybe_func_var.__module__)
                    elif callable(maybe_func_var) and not has_state(maybe_func_var):
                        collection.froms[
                            maybe_func_var_name
                        ] = maybe_func_var.__module__  #
                        collection.all_modules.append(maybe_func_var.__module__)
                    elif "btyd.fitters" in f"{maybe_func_var.__module__}":
                        collection = collect_byte_obj(
                            maybe_func_var, maybe_func_var_name, collection
                        )
                    elif isinstance(maybe_func_var, object):
                        collection.froms[
                            maybe_func_var.__class__.__name__
                        ] = maybe_func_var.__module__
                        collection.all_modules.append(maybe_func_var.__module__)
                        collection.vars[maybe_func_var_name] = maybe_func_var
                    else:
                        collection.froms[
                            maybe_func_var_name
                        ] = f"NYI: {maybe_func_var.__module__}"
            elif str(maybe_func_var).startswith("<module"):
                collection.imports[maybe_func_var_name] = maybe_func_var.__name__
                collection.all_modules.append(maybe_func_var.__name__)
            elif inspect.isclass(maybe_func_var):
                collection.froms[maybe_func_var_name] = maybe_func_var.__module__  #
                collection.all_modules.append(maybe_func_var.__module__)
            else:
                collection.vars[maybe_func_var_name] = maybe_func_var
    return collection


def is_valid_package(pkg_str: str):
    return len(pkg_str.split(".")) > 0


def collect_mod_name(func, modName: str, collection: namespace):
    if modName in func.__globals__:
        gMod = func.__globals__[modName]
        if hasattr(gMod, "__module__"):
            collection.froms[modName] = gMod.__module__
        else:
            collection.imports[modName] = gMod.__name__
            collection.all_modules.append(func.__globals__[modName].__name__)
    return collection


def parse_ast_name_to_id(astName: Any):
    if hasattr(astName, "attr"):
        return astName.value.id
    else:
        return astName.id


def get_function_args(func: Callable[..., Any], collection: namespace):
    try:
        sigAst = ast.parse(inspect.getsource(func)).body[0]  # type: ignore
        for a in sigAst.args.args:  # type: ignore
            if a.annotation is None:  # type: ignore
                continue
            collection = collect_mod_name(func, parse_ast_name_to_id(a.annotation), collection=collection)  # type: ignore
        if sigAst.returns is not None:  # type: ignore
            collection = collect_mod_name(func, parse_ast_name_to_id(sigAst.returns), collection=collection)  # type: ignore
        return collection
    except Exception as err:
        strErr = f"{err}"
        if (
            strErr != "could not get source code"
        ):  # triggers when deploying pure sklearn model
            print(f"Warning: failed parsing type annotations: {err}")

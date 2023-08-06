import os
import traceback
import datetime
from typing import Callable, Union, Any

from .utils import get_list_values, get_values, _check_lambda_args
from .client import ManageClient

__all__ = ('event', 'list_value_event')


class __Executor(object):
    def __init__(
        self,
        function: Callable,
        keys=None,
        list_value=None,
        iter_key=None,
        description=None,
        *args,
        **kwargs
    ):
        self.function = function
        self.keys = keys
        self.list_value = list_value
        self.iter_key = iter_key
        self.args = args
        self.kwargs = kwargs
        self.description = description

    def execution(self, definition: dict, timestamp: str, *args, **kwargs) -> Any:
        init_kwargs = {
            "system_id": os.environ.get("MANAGE_SYSTEM_ID", ""),
            "system_url": os.environ.get("MANAGE_SYSTEM_URL", ""),
            "token": os.environ.get("MANAGE_SYSTEM_TOKEN", ""),
            "debug": os.environ.get("MANAGE_SYSTEM_DEBUG", '0'),
        }
        client = ManageClient(**init_kwargs)
        client.push_event(
            definition=definition,
            start_time=timestamp,
            status=False,
            description=self.description,
        )
        # print(pushed)
        try:
            args = _check_lambda_args(args)
            if args or kwargs:
                func_result = self.function(*args, **kwargs)
            else:
                func_result = self.function()
        except Exception as exc_description:
            t = traceback.format_exc()
            t = t.replace("func_result = function", self.function.__name__)
            return client.log_exception(
                definition=definition, description=str(exc_description), trb=t
            )
        client.push_event(
            definition=definition,
            start_time=timestamp,
            status=True,
            description=self.description,
        )
        return func_result

    def push(self, list_: bool = False, *args, **kwargs):
        definition = {}
        var_names = self.function.__code__.co_varnames
        try:
            if self.keys is not None and not list_:
                values = get_values(self.keys, var_names, *args, **kwargs)
                definition = values["definition"]
                if not definition:
                    definition = {self.function.__name__: self.function.__name__}
            elif list_:
                list_values = get_list_values(
                    self.keys,
                    self.list_value,
                    self.iter_key,
                    var_names,
                    *args,
                    **kwargs
                )
                definition = list_values["definition"]
            else:
                definition = {self.function.__name__: self.function.__name__}

        except IndexError:
            pass
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.execution(definition, timestamp, *args, **kwargs)


def event(keys=None, description=None):
    def decorator(function, *args, **kwargs):
        def push_function_results(*args, **kwargs):
            executor = __Executor(function=function, keys=keys, description=description)
            return executor.push(False, *args, **kwargs)

        return push_function_results

    return decorator


def list_value_event(
    keys: Union[str, list], list_value: str, iter_key: str, description=None
) -> Any:
    def decorator(function, *args, **kwargs):
        def push_function_results(*args, **kwargs):
            executor = __Executor(
                function=function,
                keys=keys,
                list_value=list_value,
                iter_key=iter_key,
                description=description,
            )
            return executor.push(True, *args, **kwargs)

        return push_function_results

    return decorator

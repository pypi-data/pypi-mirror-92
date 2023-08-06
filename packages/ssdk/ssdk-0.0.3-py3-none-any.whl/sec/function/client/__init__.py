import os

from sec.function.client.base import BaseFunctionClient
from sec.function.client.queue import QueueFunctionClient
from sec.function.client.repo import RepoFunctionClient
from sec.function.client.task import TaskFunctionClient
from sec.function.client.template import TemplateFunctionClient
from sec.util import read_config


class FunctionClient(QueueFunctionClient, RepoFunctionClient, TaskFunctionClient, TemplateFunctionClient,
                     BaseFunctionClient):
    @staticmethod
    def from_env(namespace=None, try_config=False, try_env=True):
        url = None
        token = None
        namespace_val = None
        if try_config:
            config = read_config()
            if config:
                url = config.get('function', {}).get('url', None)
                token = config.get('function', {}).get('token', None)
                namespace_val = config.get('function', {}).get('namespace', None)

        if try_env:
            if os.environ.get('SEC__FUNCTION_URL', None):
                url = os.environ.get('SEC__FUNCTION_URL')
            if os.environ.get('SEC__FUNCTION_TOKEN', None):
                token = os.environ.get('SEC__FUNCTION_TOKEN')
            if os.environ.get('SEC__FUNCTION_NAMESPACE', None):
                namespace_val = os.environ.get('SEC__FUNCTION_NAMESPACE')

        if namespace:
            namespace_val = namespace_val

        if not url:
            raise Exception('SEC__FUNCTION_URL environment variable is not set')
        if not token:
            raise Exception('SEC__FUNCTION_TOKEN environment variable is not set')
        if not namespace_val:
            raise Exception('SEC__FUNCTION_NAMESPACE environment variable is not set')

        return FunctionClient(url, token, namespace_val)

import tabulate

from sec.function.client import FunctionClient


class FunctionCli:
    def __init__(self, namespace=None):
        self._client = FunctionClient.from_env(namespace, try_config=True, try_env=True)
        self.queue = FunctionQueueCli(self._client)
        self.repo = FunctionRepoCli(self._client)
        self.task = FunctionTaskCli(self._client)
        self.template = FunctionTemplateCli(self._client)


def print_table(res, headers):
    def _get(d, key):
        key_parts = key.split('.')
        v = d
        for key_part in key_parts:
            if v is None:
                break
            v = v.get(key_part, None)
        return v

    table_headers = headers
    table_res = [[_get(d, key) for key in headers] for d in res['results']]
    print('total:', res['totalCount'])
    print(tabulate.tabulate(table_res, headers=table_headers))


class FunctionQueueCli:
    def __init__(self, client):
        self._client = client

    def add(self, name):
        return self._client.add_queue(name)

    def list(self, fields=None, limit=10, offset=0):
        res = self._client.get_queues(fields, limit, offset)
        print_table(res, ['id', 'name', 'updatedAt', 'createdAt'])


class FunctionTaskCli:
    def __init__(self, client):
        self._client = client

    def add(self, queue, template, variables=None):
        return self._client.create_task_from_template(queue, template, variables)

    def get(self, task_id, fields=None):
        return self._client.get_task(task_id, fields)

    def list(self, fields=None, limit=10, offset=0):
        res = self._client.get_tasks(fields, limit, offset)
        print_table(res, ['id', 'image', 'command', 'queue.name', 'template.name', 'status', 'createdAt'])


class FunctionRepoCli:
    def __init__(self, client):
        self._client = client

    def add(self, name, url, branch):
        return self._client.add_repo(name, url, branch)

    def list(self, fields=None, limit=10, offset=0):
        res = self._client.get_repos(fields, limit, offset)
        print_table(res, ['id', 'name', 'url', 'branch', 'state.status', 'state.sha', 'state.syncedAt', 'createdAt'])

    def sync(self, name):
        return self._client.sync_repo(name)


class FunctionTemplateCli:
    def __init__(self, client):
        self._client = client

    def get(self, template_id, fields=None):
        return self._client.get_template(template_id, fields)

    def list(self, fields=None, limit=10, offset=0):
        res = self._client.get_templates(fields, limit, offset)
        print_table(res, ['id', 'name', 'repository.name', 'path', 'enabled', 'schedule', 'scheduleQueue', 'createdAt'])

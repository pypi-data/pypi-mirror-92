import json

from sec.function.client.base import BaseQuery, BaseFunctionClient


class TaskFunctionClient(BaseFunctionClient):
    def create_task_from_template(self, queue, template, variables=None, fields=None):
        if variables is None:
            variables = {}
        payload = {
            'query': CreateTaskFromTemplateMutation.generate(fields),
            'variables': {
                'namespaceName': self.namespace,
                'queue': queue,
                'templateName': template,
                'variables': json.dumps(variables),
            }
        }
        res = self._call(payload)
        try:
            return res['data']['createTaskFromTemplate']['task']['id']
        except Exception as e:
            print(res)
            raise e

    def get_task(self, task_id, fields=None):
        payload = {
            'query': GetTaskQuery.generate(fields),
            'variables': {'id': task_id}
        }
        res = self._call(payload)
        try:
            return res['data']['task']
        except:
            print(res)

    def get_tasks(self, fields=None, limit=10, offset=0):
        payload = {
            'query': GetTasksQuery.generate(fields),
            'variables': {'namespace': self.namespace, 'limit': limit, 'offset': offset}
        }
        res = self._call(payload)
        try:
            return res['data']['tasks']
        except:
            print(res)


class CreateTaskFromTemplateMutation(BaseQuery):
    operation = 'mutation'
    arguments = {
        '$namespaceName': 'String!',
        '$queue': 'String!',
        '$templateName': 'String!',
        '$variables': 'JSONString!',
    }
    default_fields = [
        'ok',
        'error',
        'task { id }',
    ]
    template = '''
        createTaskFromTemplate(
            namespace: {{name: $namespaceName}},
            queue: $queue,
            template: {{name: $templateName}},
            variables: $variables,
            streamStdout: false,
            streamStderr: false,
        ) {{ {fields} }}
    '''


class GetTaskQuery(BaseQuery):
    operation = 'query'
    arguments = {
        '$id': 'ID!',
    }
    default_fields = [
        'id',
        'image',
        'script',
        'command',
        'queue { id name }',
        'namespace { id name }',
        'template { id name }',
        'group { id name }',
        'streamStdout',
        'streamStderr',
        'status',
        'worker { id name }',
        'stdout',
        'stderr',
        'result',
        'createdBy',
        'isScheduled',
        'createdAt',
        'updatedAt',
    ]
    template = 'task(id: $id) {{ {fields} }}'


class GetTasksQuery(BaseQuery):
    operation = 'query'
    arguments = {
        '$namespace': 'String!',
        '$limit': 'Int!',
        '$offset': 'Int!',
    }
    default_fields = [
        'id',
        'image',
        'command',
        'queue { id name }',
        'template { id name }',
        'group { id name }',
        'status',
        'worker { id name }',
        'createdBy',
        'isScheduled',
        'createdAt',
        'updatedAt',
    ]
    template = '''
        tasks(namespace_Name: $namespace) {{
            totalCount
            results(limit: $limit, offset: $offset) {{ {fields} }}
        }}'''

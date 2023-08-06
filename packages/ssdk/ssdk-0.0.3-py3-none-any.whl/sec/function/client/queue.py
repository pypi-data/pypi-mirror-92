from sec.function.client.base import BaseQuery, BaseFunctionClient


class QueueFunctionClient(BaseFunctionClient):
    def get_queues(self, fields=None, limit=10, offset=0):
        payload = {
            'query': GetQueuesQuery.generate(fields),
            'variables': {'namespace': self.namespace, 'limit': limit, 'offset': offset}
        }
        res = self._call(payload)
        try:
            return res['data']['queues']
        except:
            print(res)

    def add_queue(self, name, fields=None):
        payload = {
            'query': CreateQueueMutation.generate(fields),
            'variables': {
                'name': name,
                'namespaceName': self.namespace,
            }
        }
        res = self._call(payload)
        try:
            return res['data']['createQueue']['queue']['id']
        except:
            print(res)


class GetQueuesQuery(BaseQuery):
    operation = 'query'
    arguments = {
        '$namespace': 'String!',
        '$limit': 'Int!',
        '$offset': 'Int!',
    }
    default_fields = [
        'id',
        'name',
        'createdAt',
        'updatedAt',
    ]
    template = '''
        queues(namespace_Name: $namespace) {{
            totalCount
            results(limit: $limit, offset: $offset) {{ {fields} }}
        }}'''


class CreateQueueMutation(BaseQuery):
    operation = 'mutation'
    arguments = {
        '$name': 'String!',
        '$namespaceName': 'String!',
    }
    default_fields = ['id']
    template = '''
        createQueue(name: $name, namespace: {{name: $namespaceName}}) {{
            ok queue {{ {fields} }} 
        }}
    '''

from sec.function.client.base import BaseQuery, BaseFunctionClient


class TemplateFunctionClient(BaseFunctionClient):
    def get_template(self, id, fields=None):
        payload = {
            'query': GetTemplateQuery.generate(fields),
            'variables': {'id': id}
        }
        res = self._call(payload)
        try:
            return res['data']['template']
        except:
            print(res)

    def get_templates(self, fields=None, limit=10, offset=0):
        payload = {
            'query': GetTemplatesQuery.generate(fields),
            'variables': {'namespace': self.namespace, 'limit': limit, 'offset': offset}
        }
        res = self._call(payload)
        try:
            return res['data']['templates']
        except:
            print(res)


class GetTemplateQuery(BaseQuery):
    operation = 'query'
    arguments = {'$id': 'ID!'}
    default_fields = [
        'id',
        'name',
        'repository { id name }',
        'path',
        'enabled',
        'schedule',
        'scheduleQueue',
        'spec',
        'createdAt',
        'updatedAt',
    ]
    template = 'template(id: $id) {{ {fields} }}'


class GetTemplatesQuery(BaseQuery):
    operation = 'query'
    arguments = {
        '$namespace': 'String!',
        '$limit': 'Int!',
        '$offset': 'Int!',
    }
    default_fields = [
        'id',
        'name',
        'repository { id name }',
        'path',
        'enabled',
        'schedule',
        'scheduleQueue',
        'createdAt',
        'updatedAt',
    ]
    template = '''
        templates(namespace_Name: $namespace) {{
            totalCount
            results(limit: $limit, offset: $offset) {{ {fields} }}
        }}'''

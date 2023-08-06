from sec.function.client.base import BaseQuery, BaseFunctionClient


class RepoFunctionClient(BaseFunctionClient):
    def get_repos(self, fields=None, limit=10, offset=0):
        payload = {
            'query': GetRepositoriesQuery.generate(fields),
            'variables': {'namespace': self.namespace, 'limit': limit, 'offset': offset}
        }
        res = self._call(payload)
        try:
            return res['data']['repositories']
        except:
            print(res)

    def add_repo(self, name, url, branch, fields=None):
        payload = {
            'query': CreateRepoMutation.generate(fields),
            'variables': {
                'name': name,
                'namespaceName': self.namespace,
                'url': url,
                'branch': branch,
            }
        }
        res = self._call(payload)
        try:
            return res['data']['createRepository']['repository']['id']
        except:
            print(res)

    def sync_repo(self, name, fields=None):
        payload = {
            'query': SyncRepoMutation.generate(fields),
            'variables': {'name': name}
        }
        res = self._call(payload)
        try:
            return res['data']['repositories']
        except:
            print(res)


class GetRepositoriesQuery(BaseQuery):
    operation = 'query'
    arguments = {
        '$namespace': 'String!',
        '$limit': 'Int!',
        '$offset': 'Int!',
    }
    default_fields = [
        'id',
        'name',
        'url',
        'branch',
        'state { status syncedAt sha }',
        'createdAt',
        'updatedAt',
    ]
    template = '''
        repositories(namespace_Name: $namespace) {{
            totalCount
            results(limit: $limit, offset: $offset) {{ {fields} }}
        }}'''


class SyncRepoMutation(BaseQuery):
    operation = 'mutation'
    arguments = {'$name': 'String!'}
    default_fields = []
    template = 'syncRepository(repository: {{name: $name}}) {{ ok }}'


class CreateRepoMutation(BaseQuery):
    operation = 'mutation'
    arguments = {
        '$name': 'String!',
        '$namespaceName': 'String!',
        '$url': 'String!',
        '$branch': 'String!',
    }
    default_fields = ['id']
    template = '''
        createRepository(name: $name, namespace: {{name: $namespaceName}}, url: $url, branch: $branch) {{
            ok repository {{ {fields} }} 
        }}
    '''

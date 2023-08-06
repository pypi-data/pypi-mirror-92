from abc import abstractmethod

import requests


class BaseFunctionClient:
    def __init__(self, url, token, namespace):
        self.url = url
        self.token = token
        self.namespace = namespace

    def _call(self, payload):
        headers = {'Authorization': f'token {self.token}'}
        res = requests.post(f'{self.url}/graphql', headers=headers, json=payload)
        return res.json()


class BaseQuery:
    @property
    @abstractmethod
    def operation(self):
        pass

    @property
    @abstractmethod
    def arguments(self):
        pass

    @property
    @abstractmethod
    def default_fields(self):
        pass

    @property
    @abstractmethod
    def template(self):
        pass

    @classmethod
    def generate(cls, fields=None):
        if fields is None:
            fields = cls.default_fields
        alias = cls.__name__
        header = f'{cls.operation} {alias}'
        if len(cls.arguments) > 0:
            arguments_string = ','.join([f'{k}: {v}' for k, v in cls.arguments.items()])
            header += f'({arguments_string})'
        body = cls.template.format(fields=' '.join(fields))
        return f'{header} {{ {body} }}'

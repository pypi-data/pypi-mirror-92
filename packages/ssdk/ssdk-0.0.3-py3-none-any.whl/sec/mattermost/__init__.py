import requests


class MattermostClient:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, data):
        requests.post(self.webhook_url, json=data)

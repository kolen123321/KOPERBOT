import json

class Config:
    def __init__(self, path="config.json"):
        self.data = json.loads(open(path, "r", encoding='utf-8-sig').read())

    

class Config:
    def __init__(self, memo):
        self.memo = memo
        self.configs = []

    def add(self, conf):
        self.configs.append(conf)

class ConfigPS(Config):
    def __init__(self, url, key, memo):
        super().__init__(memo)
        self.url = url
        self.key = key



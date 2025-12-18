from enum import Enum

BASE_URL = "https://allegro.pl"
BASE_URL_SANDBOX = "https://allegro.pl.allegrosandbox.pl"


class PathTo(Enum):
    DEVICE = "/auth/oauth/device"
    TOKEN = "/auth/oauth/token"

    def getPath(self):
        return self.value

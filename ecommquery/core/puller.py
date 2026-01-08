import time
from datetime import datetime, timedelta

from ecommquery import Endpoint
from ecommquery.core.service_management import ManagementService


class Puller:
    class Config:
        def __init__(self, service, action, zero_call, freq):
            self._freq = freq
            self.srv = service
            self.act = action

            if zero_call:
                self._next_call = datetime.now()
            else:
                self._next_call = datetime.now() + timedelta(seconds=Puller.refreshRate(freq))

        def callNow(self, time_now):
            call_now = (self._next_call <= time_now)
            if call_now:
                print(f"Time to call")
                self._next_call = time_now + timedelta(seconds=Puller.refreshRate(self._freq))
            else:
                print(f"Not now")
            return call_now

    @staticmethod
    def refreshRate(freq) -> int:
        f_arr = freq.split('/')
        p = int(f_arr[0])

        if p <= 0:
            raise ValueError(f"Invalid frequency: {f_arr[0]}")

        match f_arr[1].lower():
            case 'd' | 'day':
                period = 86400
            case 'h' | 'hour':
                period = 3600
            case 'm' | 'min':
                period = 60
            case _:
                raise ValueError(f"Invalid frequency period: {f_arr[1]}")

        return int(period / p)

    def __init__(self, def_freq = '1/h'):
        self._def_freq = def_freq
        self._list = []
        self._last_idx = 0
        
    def register(self, service:ManagementService, action, zero_call = True, freq = None):
        self._list.append(Puller.Config(service, action, zero_call, self._def_freq if freq == None else freq))
    
    def probe(self):
        time_now = datetime.now()

        for idx, conf in enumerate(self._list, start=self._last_idx):
            if conf.callNow(time_now):
                self._last_idx = idx + 1
                return conf.srv, conf.act

        self._last_idx = 0
        return None, None

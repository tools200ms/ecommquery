
from datetime import datetime, timedelta

from ecommquery import Endpoint
from ecommquery.core.service_management import ManagementService


class Puller:
    class Config:
        def __init__(self, service, action, freq:str, start_shift:str):
            self._freq = freq
            self.srv = service
            self.act = action

            if start_shift is not None:
                self._next_call = datetime.now() + timedelta(seconds=Puller.refreshRate(start_shift))
            else:
                self._next_call = datetime.now()

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

        self._change_report_stack = []
        self._change_report_underprocess = None
        
    def register(self, service, action, freq:str = None, start_shift:str = None):
        self._list.append(Puller.Config(service,
                                        action,
                                        self._def_freq if freq == None else freq,
                                        start_shift))
    
    def probe(self):
        time_now = datetime.now()

        if len(self._change_report_stack) == 0 and self._change_report_underprocess == None:
            current_change_report, change_report_by = None, None
        else:
            if self._change_report_underprocess == None:
                self._change_report_underprocess = self._change_report_stack.pop()
            current_change_report, change_report_by = self._change_report_underprocess

        for idx, conf in enumerate(self._list, start=self._last_idx):
            if conf.callNow(time_now) or \
                (change_report_by != None and change_report_by != conf.srv):
                self._last_idx = idx + 1
                return conf.act, conf.srv, (current_change_report, change_report_by)

        self._last_idx = 0
        self._change_report_underprocess = None

        return None, None, (None, None)

    def update(self, srv, change_report):
        self._change_report_stack.append((srv, change_report))
        self._last_idx = 0
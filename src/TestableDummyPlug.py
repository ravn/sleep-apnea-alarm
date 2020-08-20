from datetime import datetime, timedelta
import random

from kasa import SmartDeviceException


class EmeterRealtime:
    def __init__(self) -> None:
        self.low_start_time = (datetime.now() + timedelta(seconds=5)).time()
        self.low_end_time = (datetime.now() + timedelta(seconds=75)).time()
        self.count = 0

    def get(self, key):
        if self.count >= 1:
            self.count = 0
        else:
            self.count = self.count + 0.001

        if self.low_start_time < datetime.now().time() < self.low_end_time:
            return 5 + self.count
        else:
            return 100 + self.count

    def __str__(self):
        return str(self.get("power"))



class TestableDummyPlug:

    def __init__(self) -> None:
        self.alias = self.__class__.__name__
        self.emeter_realtime = EmeterRealtime()

    @staticmethod
    async def update():
        f = random
        randint = f.randint(0, 1)
        if randint == 0:
            try:
                raise OSError("Dummy network error")
            except OSError as e:
                raise SmartDeviceException("Dummy wrapped error") from e


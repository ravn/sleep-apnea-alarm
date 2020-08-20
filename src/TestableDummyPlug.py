class TestableDummyPlug:

    def __init__(self) -> None:
        self.alias = self.__class__.__name__

    @staticmethod
    async def update():
        return None

    emeter_realtime = {"power": 5.0}  # Watts

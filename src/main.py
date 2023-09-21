import asyncio
import logging
import traceback
from datetime import datetime
import time
from kasa import Discover, SmartDeviceException

from src.TestableDummyPlug import TestableDummyPlug


async def print_alias(dev):
    print(f"Discovered {dev.alias}")


async def main(discover_plugs=lambda: Discover.discover(),  # discover_single("192.168.0.200"),
               alarm=lambda s: print("ALARM", s),
               delay=True):
    # https://python-kasa.readthedocs.io/en/latest/smartplug.html

    # For some reason this doesn't work here, but works in the kasa cli program

    # devices_found = await Discover.discover(on_discovered=print_alias)

    # plugs_found = filter(lambda dev: dev.has_emeter, devices_found)
    log = logging.getLogger(__name__)

    try:
        plugs_found = await discover_plugs()
    except SmartDeviceException as e:
        raise e

    if len(plugs_found) == 0:
        print("No plugs found")
        exit(1)

    if len(plugs_found) > 1:
        print("More than one plug found")
        exit(1)

    plug = next(iter(plugs_found.values()))

    time_to_be_below_threshold = 60  # seconds

    time_in_range_now = False

    while True:
        if delay:
            time.sleep(1)
        time_in_range_then = time_in_range_now
        now = datetime.now()
        time_in_range_now = True  # Elaborate check pending
        emeter_realtime = "<not set>"
        current_power = 0
        if time_in_range_now:
            if not time_in_range_then:
                power_currently_below_threshold = False
                power_threshold = 10  # Watts

            try:
                await plug.update()

                emeter_realtime = plug.emeter_realtime
                current_power = emeter_realtime.get("power")

                if current_power < power_threshold:
                    if not power_currently_below_threshold:
                        start_time_below_threshold = now
                        power_currently_below_threshold = True
                    seconds_below_threshold = (now - start_time_below_threshold).total_seconds()
                    if seconds_below_threshold > time_to_be_below_threshold:
                        alarm(seconds_below_threshold)
                else:
                    power_currently_below_threshold = False
            except SmartDeviceException as e:
                # For now we assume that network errors are transient.
                pass

        print(now, plug.alias, current_power, emeter_realtime)


async def testableDummyPlug():
    return TestableDummyPlug()


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s    File "%(pathname)s", line %(lineno)s', level=logging.WARN)
    # execute only if run as a script
    #    asyncio.run(main(discover_plugs=lambda: testableDummyPlug(), alarm=lambda s: print(s)))
    #    asyncio.run(main(discover_plugs=lambda: testableDummyPlug(), delay=True))
    asyncio.run(main(delay=True))

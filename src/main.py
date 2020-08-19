import asyncio
from datetime import datetime
import time
from kasa import SmartPlug, Discover, SmartDeviceException


async def print_alias(dev):
    print(f"Discovered {dev.alias}")


async def main():
    # https://python-kasa.readthedocs.io/en/latest/smartplug.html

    # For some reason this doesn't work here, but works in the kasa cli program

    # devices_found = await Discover.discover(on_discovered=print_alias)

    # plugs_found = filter(lambda dev: dev.has_emeter, devices_found)

    plug_found = await Discover.discover_single("192.168.0.11")
    #
    # if len(plugs_found == 0):
    #     print("No plugs found")
    #     exit(1)
    #
    # if len(plugs_found > 1):
    #     print("More than one plug found")
    #     exit(1)
    #
    # plug = plugs_found[0]

    plug = plug_found

    time_to_be_below_threshold = 60  # seconds

    time_in_range_now = False

    while True:
        time.sleep(1)
        time_in_range_then = time_in_range_now
        now = datetime.now()
        time_in_range_now = True  # Elaborate check pending
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
                        print(f"BEEN BELOW FOR {seconds_below_threshold}")
                else:
                    power_currently_below_threshold = False
            except SmartDeviceException as e:
                # Network failure is a chained OSError
                # try:
                #     if e.__cause__:
                #         raise e.__cause__
                # except OSError:
                #     # Silently ignore all operating system issues for now.
                #     pass
                # except :
                raise e

        print(now, plug.alias, emeter_realtime)

    #   await p.turn_off()


if __name__ == "__main__":
    # execute only if run as a script
    asyncio.run(main())

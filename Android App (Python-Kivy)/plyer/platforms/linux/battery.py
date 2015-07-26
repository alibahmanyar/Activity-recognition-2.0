from subprocess import Popen, PIPE
from plyer.facades import Battery
from plyer.utils import whereis_exe


class LinuxBattery(Battery):
    def _get_state(self):
        status = {"isCharging": None, "percentage": None}

        # We are supporting only one battery now
        dev = "/org/freedesktop/UPower/device/battery_BAT0"
        upower_process = Popen(["upower", "-d", dev],
                stdout=PIPE)
        output = upower_process.communicate()[0]

        if not output:
            return status

        power_supply = percentage = None
        for l in output.splitlines():
            if 'power supply' in l:
                power_supply = l.rpartition(':')[-1].strip()
            if 'percentage' in l:
                percentage = float(l.rpartition(':')[-1].strip()[:-1])

        if(power_supply):
            status['isCharging'] = power_supply != "yes"

        status['percentage'] = percentage

        return status


def instance():
    import sys
    if whereis_exe('upower'):
        return LinuxBattery()
    sys.stderr.write("upower not found.")
    return Battery()

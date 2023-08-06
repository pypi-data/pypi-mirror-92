import psutil
def getBatteryCharge():
    battery = psutil.sensors_battery()
    percent = str(battery.percent)+" %"
    return percent

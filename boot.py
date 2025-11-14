import network, time, env

SSID = env.WIFI_SSID
PASSWORD = env.WIFI_PASSWORD
print("is this thing on?")
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected() or not wlan.active():
            time.sleep(1)
    print("Connected:", wlan.ifconfig())

connect_wifi()

import ubinascii
import requests as urequests
import os, machine
import datetime


def get_formatted_mac():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True) 
    wlan_mac_bytes = sta_if.config('mac')
    mac_hex = ubinascii.hexlify(wlan_mac_bytes).decode()
    return mac_hex[-6:]

from ssd1306 import SSD1306_I2C

SDA_PIN = 8
SCL_PIN = 9
OLED_WIDTH = 128
OLED_HEIGHT = 64 
try:
    i2c = machine.I2C(0, scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN))
    oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
except Exception as e:
    print(f"Error initializing I2C or OLED: {e}")
    
def display_mac():
    mac_addr = get_formatted_mac()
    oled.text(mac_addr, 0, 16)
    oled.text("chk", 0, 0)
    oled.show()

# --- Main loop ---
if 'oled' in locals():
    display_mac()





DEVICE_ID = get_formatted_mac()
SERVER = env.SERVER

def get_version():
    try:
        with open("version.txt") as f:
            result = f.read()[1:-1].split(", ")
        if result == [""]:
            return [1,1,1,0,0,0]
        return result
    except:
        return [1,1,1,0,0,0]

print("get_version", get_version())
def save_version(v):
    with open("version.txt", "w") as f:
        f.write(str(v))

def update():
    print("trying to update")
    v = get_version()
    while True:
        try:
            print("before request")
            print(f"{SERVER}/api/check-updates?deviceId={DEVICE_ID}")
            res = urequests.get(f"{SERVER}/api/check-updates?deviceId={DEVICE_ID}")
            print("request success")
            date_current = v
            date_update = res.text.strip()
            space = date_update.split(" ")
            dates = space[0].split("-")
            times = space[1].split(":")
            print(dates)
            print(times)
            date_updateobj = datetime.datetime(int(dates[0]), int(dates[1]), int(dates[2]), int(times[0]), int(times[1]), int(times[2]))
            print(date_updateobj)
            date_currentobj = datetime.datetime(int(v[0]),int(v[1]),int(v[2]),int(v[3]),int(v[4]),int(v[5]))
            print(date_currentobj)
            if date_updateobj > date_currentobj:
                print("New update found! Downloading...")
                oled.text("dw", 0, 0)
                oled.show
                r2 = urequests.get(f"{SERVER}/api/download?deviceId={DEVICE_ID}")
                with open("main.mpy", "wb") as f:
                    f.write(r2.content)
                save_version([int(dates[0]), int(dates[1]), int(dates[2]), int(times[0]), int(times[1]), int(times[2])])
                print("Update complete.")
                time.sleep(2)
                #machine.reset()
            else:
                print("No update.")
                oled.fill(0)
                oled.text(get_formatted_mac(), 0, 16)
                oled.text("-",0,0)
                oled.show()
            break
        except Exception as e:
            print("Update error:", e)
            time.sleep(2)
            oled.fill(0)
            oled.text(get_formatted_mac(), 0, 16)
            oled.text("err",0,0)
            oled.show()

    
update()

__import__('main')



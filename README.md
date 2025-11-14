# MicroPython OTA Boot
For the Frontend IDE and Backend API, please click [here]("https://github.com/leejiaq/MicroPython_OTA_IDE").

## Setup
1. Flash MicroPython to ESP32  
2. Upload `boot.py` and `env.py`
3. Install the [library](#install-the-library-required) required
4. Reboot  
5. Device will auto-check for updates

## env.py Example
```python
WIFI_SSID = "WIFI"
WIFI_PASSWORD = "PASS"
SERVER = "127.0.0.1:3000"
``` 

## Install the library required
From terminal:
```bash
mpremote mip install requests
mpremote mip install ssd1306
mpremote mip install datetime
```
or

From REPL:
```python
import mip
mip.install("requests")
mip.install("ssd1306")
mip.install("datetime")
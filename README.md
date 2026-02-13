# METAR-Desk-Clock

Display ICAO METAR weather data with a Raspberry Pi. 

This is based on the original project from Michael duPont which can be found at https://github.com/devdupont/METAR-RasPi.

## Screen

This version runs the METAR program on a touchscreen display. I did not have a plate availible to test and work with as the original project did so I have diabled the plate functions.

### Hardware I have used / tested 

- Raspberry Pi 5 (will work on any amount of PI 5 ram)
- NVME HAT
- NVME / POE+ HAT

Tested displays:
- 7 Inch Touchscreen IPS DSI Display Compatible with Raspberry Pi 5/4/3, 800x480 Pixel Capacitive Screen MIPI Driver-Free Interface (https://www.amazon.com/dp/B0D3QB7X4Z)

- 5 Inch Touchscreen IPS MIPI DSI Display Compatible with Raspberry Pi 5/4/3, 800x480 Pixel Capacitive Screen Driver-Free Interface (https://www.amazon.com/dp/B0CXTFN8K9)



### Program Config

Common project settings are stored in `metar/config.py`. For the screen, the ones you may want to change are:

- `layout`: Size of the screen. Loads the layout from `metar/screen_settings`
- `shutdown_on_exit`: Set to `True` to shutdown the Pi when exiting the program
- `clock_utc`: Clock displays UTC or local time. Not applicable to 320x240 size
- `include_remarks`: Set to `True` to include the remarks section in scroll line


## Installing

My preference is to do the install though an SSH terminal. I used the standard windows terminal for my install.

I started with a fresh install of raspbian "Debian GNU/Linux 13 (Trixie)" this can be checked my running

```bash 
cat /etc/os-release
```

Make sure your pi is fully updated

```bash
sudo apt update
```
```bash
sudo apt full-upgrade -y
```

This project uses the avwx-engine for connecting to the data source. Se we'll go ahead and install it. This will install AVWX globally not in a virtual enviroment. 

```bash
python3 -m pip install git+https://github.com/avwx-rest/avwx-engine.git --break-system-packages
python3 -m pip install shapely --break-system-packages

```

We'll also need hatch for this to work properly
```bash
sudo apt install pipx
pipx ensurepath
source ~/.bashrc
```



Now lets get the the fun part. The install of the Desk Clock Software:
```bash
git clone https://github.com/jujubeenuk/METAR-RasPi.git
```

Start the screen
```bash
DISPLAY=:0 python3 ~/METAR-RasPi/metar_raspi/screen.py
```
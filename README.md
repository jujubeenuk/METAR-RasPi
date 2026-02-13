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
cd ~/METAR-RasPi
DISPLAY=:0 PYTHONPATH=. python3 metar_raspi/screen.py
```

Now if you would like this to start when your RaspberryPi starts we'll have to create a service for it.

First navigate to where services are stored

```bash
cd /etc/systemd/system/
```

Now we're gonna create the new service:
```bash
sudo nano metar-screen.service
```

The service will contain the following:
```bash
[Unit]
Description=METAR Display Service
# Wait until after graphical enviroment is ready
After=graphical.target
Wants=graphical.target

[Service]
# Run the service as the user who owns the files (assumed 'pi')
User=pi
Group=pi

# Set the working directory to the user's home directory
# (since the METAR-RasPi folder is inside it)
WorkingDirectory=/home/pi/

# Set the PYTHONPATH environment variable using the full absolute path
# This is required for your module imports to resolve correctly
Environment=PYTHONPATH=/home/pi/METAR-RasPi

# ----------------------------------------------------
# ADD THESE LINES to set the DISPLAY environment for the GUI
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority

# The command to execute: python followed by the script's absolute path
ExecStart=/usr/bin/python /home/pi/METAR-RasPi/metar_raspi/screen.py

# Restart the service if it stops unexpectedly
Restart=never

[Install]
# This target ensures the service starts when the graphical desktop boots
WantedBy=graphical.target
cd /etc/systemd/system/
```

Update the service permissions
```bash
sudo chmod 644 metar-screen.service
```

Next set ther service to run on boot:
```bash
sudo systemctl enable metar-screen.service
```


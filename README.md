# METAR Desk Clock 

Display ICAO METAR weather data with a Raspberry Pi. 

This project began life as a project found at https://github.com/devdupont/METAR-RasPi by Michael duPont. I struggled with getting it installed and to function with updates to raspbian, avwx, and python. As an avaition geek and hobbiest programmer I took it upon myself to update the project and create and step-by-step walkthough on getting it installed after I got the functionality back. 

## Screen

This version runs the METAR program on a touchscreen display. I did not have a plate availible to test and work with as the original project did so I have diabled/removed the plate functions.

### Hardware I have used / tested 

- Raspberry Pi 5 (will work on any amount of PI 5 ram) I don't see why this wouldn't work on any other RaspberryPi I just havent tested it.
- NVME HAT
- NVME / POE+ HAT
- This can also be installed on an SD Card if you don't want the added expense of an NVME hat and drive. The NVME and hat are for longevity and testing on my part. 

Tested displays:
- 7 Inch Touchscreen IPS DSI Display Compatible with Raspberry Pi 5/4/3, 800x480 Pixel Capacitive Screen MIPI Driver-Free Interface (https://www.amazon.com/dp/B0D3QB7X4Z)

- 5 Inch Touchscreen IPS MIPI DSI Display Compatible with Raspberry Pi 5/4/3, 800x480 Pixel Capacitive Screen Driver-Free Interface (https://www.amazon.com/dp/B0CXTFN8K9)

- 52Pi 3.5 inch Touch Screen with case and Official Radiator for Raspberry Pi 5 (driver installed from https://github.com/goodtft/LCD-show) prior to moving on with these directions. I have discovered this by default sets the rotation to the power on the bottom edge of the case if you want to set it on edge. I recommend rotating the screen 180 degrees.

#### How to rotate the display direction (ONLY FOR 3.5 INCH SCREEN)
This method only applies to the Raspberry Pi series of display screens, other display screens do not apply.

Method 1, If the driver is not installed, execute the following command (Raspberry Pi needs to connected to the Internet):
```bash
sudo rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./XXX-show 180
```

After execution, the driver will be installed. The system will automatically restart, and the display screen will rotate 180 degrees to display and touch normally.
( ' XXX-show ' can be changed to the corresponding driver, and ' 180 ' can be changed to 0, 90, 180 and 270, respectively representing rotation angles of 0 degrees, 90 degrees, 180 degrees, 270 degrees)

Method 2, If the driver is already installed, execute the following command:
```bash
cd LCD-show/
sudo ./rotate.sh 180
```

After execution, the system will automatically restart, and the display screen will rotate 180 degrees to display and touch normally.
( ' 180 ' can be changed to 0, 90, 180 and 270, respectively representing rotation angles of 0 degrees, 90 degrees, 180 degrees, 270 degrees)
(If the rotate.sh prompt cannot be found, use Method 1 to install the latest drivers)


## Program Config

Common project settings are stored in `metar_raspi/screen.py`. For the screen, the ones you may want to change are:

- `layout`: Size of the screen. Loads the layout from `metar_raspi/settings` (Default: `800x480`) The 5 and 7 inch screen above are in this resolution. the 3.5 inch screen above needs this changed to `480x320`
- `shutdown_on_exit`: Set to `True` to shutdown the Pi when exiting the program (Default: `false`)
- `clock_utc`: Clock displays UTC or local time. Not applicable to 320x240 size (Default: `local`)
- `include_remarks`: Set to `True` to include the remarks section in scroll line (Default: `true`)
- The initial airport is set to KIPJ Lincolnton Regional just outside Charlotte NC


## Installing

###Phase 1: Installing the python script

My preference is to do the install though an SSH terminal. I used the standard windows terminal for my install.

I started with a fresh install of raspbian "Debian GNU/Linux 13 (Trixie)" this can be checked my running

```bash 
cat /etc/os-release
```

My python version is 3.15.5. You can check yours using:

```bash
python3 --version
```

I point thse out in the event trouble shooting is needed in the future.

Make sure your pi is fully updated

```bash
sudo apt update && sudo apt full-upgrade -y
```

This project uses the avwx-engine for connecting to the data source. Se we'll go ahead and install it. This will install AVWX globally not in a virtual enviroment. This will also install the latest version of avwx-engine as of this publish (2/13/26).

```bash
python3 -m pip install git+https://github.com/avwx-rest/avwx-engine.git --break-system-packages
python3 -m pip install shapely --break-system-packages

```

We'll also need pipxand hatch globally for this to work properly
```bash
sudo apt install pipx -y
sudo pipx install hatch --global
sudo pipx ensurepath --global
source ~/.bashrc
```


Now lets get to the actual project. The install of the Desk Clock Software:
```bash
git clone https://github.com/jujubeenuk/METAR-RasPi.git
```

This can be used to manually start the screen and test everything is working.

```bash
cd ~/METAR-RasPi
DISPLAY=:0 PYTHONPATH=. python3 metar_raspi/screen.py
```
Now you can use ctrl+c to close: keep in mind this will stop the running project

###Phase 2: Launching the python script:

If everything is working lets create a desktop icon to launch this in the event it fails to start:

This will create the icon
```bash
nano /home/pi/Desktop/Start_Metar.desktop
```
Here are the file contents
```bash
[Desktop Entry]
Type=Application
Name=Start METAR Clock
Comment=Launches METAR screen directly
Exec=bash -c "cd /home/pi/METAR-RasPi && DISPLAY=:0 PYTHONPATH=. python3 metar_raspi/screen.py"
Terminal=false
Categories=Utility;
```
Set the permissions to be executable
```bash
chmod +x /home/pi/Desktop/Start_Metar.desktop
```
At this point the script can be run from the desktop. 

###Phase 3: Autostarting when booting the raspberrypi (Currently not working again - working to repair)

Now if you would like this to start when your RaspberryPi starts since the plan is to use it as a desk clock, we'll have to create a service for it.

I like to work in my directory structure so navigate to the services folder:
```bash
cd /etc/systemd/system/
```

Now it's time to create the new service:

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

Update the service permissions:
```bash
sudo chmod 644 metar-screen.service
```

Next set the service to run on boot:
```bash
sudo systemctl enable metar-screen.service
```

At this poinst you can reboot the RaspberryPi and enjoy your new desk clock.

```bash
sudo reboot
```

When this starts it will check to see if an internet connection is present. It just pings the google 8.8.8.8 DNS servers to check. If connection is present via wired or wire less it will then boot into the full screen desk top display of the desk clock.

If no connection is present it will close the program automatically. If you see this behavior then please check your internet connection and make sure it is online. Once connected run the command below from the terminal to launch the clock or just reboot if steps were followed for setting it to auto start.

##Functions

Manual Launch from the command line:
```bash
cd ~/METAR-RasPi
DISPLAY=:0 PYTHONPATH=. python3 metar_raspi/screen.py
```
Starting from the icon on the desktop just requires double clicking it to launch

The automatic start function is not working with the most recent (7/12/26) raspbian install. I'm working to resove this issue.

The airport can be changed using the gear icon and the green up/down arrow. Just navigate to the ICO code for the airport you wish to view.

The red circle closes out the program if you want to do things from the desktop. 

# RNAi-CAM

## Install Raspberry Pi software
Format SD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/)

This guide uses a raspberry pi 5, and the 64-bit OS.


## Pi Connect
Click this:
![button in menu](guideImages/piConnect.jpg)
Input the hostname of the pi as the name of your device when prompted.

Choose 'Turn On Raspberry Pi Connect'. The browser will open. Sign in, using the username of the pi as the device name.

You will now be able to connect to the raspberry pi here: [https://connect.raspberrypi.com/devices](https://connect.raspberrypi.com/devices)

## Connecting cameras
The nest camera should be connected as camera 0 and the external camera should be camera 1. The positions are indicated by CAM/DISP 0 and CAM/DISP 1 on the board of the raspberry pi:
![Camera connections](guideImages/camera.jpg)

## Check mounting location of external hard drive
run the following in terminal:
```bash
sudo fdisk -l
```
This will list mounted drives, and look for /dev/sda1 in last line.
Hard drives must be mounted at sda1. Do not connect other hard drives to pi.

## Preview camera (to test focus, framing, etc)
```bash
rpicam-hello -t 0 --camera 0 #you should see the nest
```
```bash
rpicam-hello -t 0 --camera 1 #you should see the outside
```

## Take a single full resolution photo
```bash
rpicam-jpeg -o test.jpeg
```

## Setting up RTC
* Note: Requires access with internet
1. Connect RTC battery to slot labelled 'BAT'
2. check that clock is working with sudo hwclock -r
3. Run this:
   ```bash
   sudo hwclock --systohc
   ```
5. Edit configurations,
   ```sudo -E rpi-eeprom-config --edit```
   modifying the two lines (if these variables do not exist, add them):
   ```
   POWER_OFF_ON_HALT = 1
   WAKE_ON_GPIO=0
   ```
7. After adding the lines, ctl+s will save. Then use ctl+x to leave.

## Clone this repository
```bash
git clone https://github.com/vasalerno/RNAi-CAM.git
```
Move all contents of this repositoty into home directory ('~'). You can do it in the GUI, or input this into the terminal:
```bash
cp -rf RNAi-CAM/* ~
```

## Make mount directory
```bash
sudo mkdir /mnt/RNAi-CAM
```
If folder exists, it will refuse to make the directory. Ignore it and move on.


## Install openCV library
```bash
cd ~
python3 -m venv rnai_2025
source rnai_2025/bin/activate
pip3 install opencv-contrib-python
```

Now it's good to reboot:
```bash
sudo reboot -h now
```

## Add lines to the crontab
Open up crontab with the following command:
```bash
crontab -e
```
Choose 1.
 
Then add the following lines to the bottom of the crontab file if they're not there already (to get permissions and mount directory for external hard drive)
```bash
@reboot sudo systemctl daemon-reload
@reboot sudo mount /dev/sda1 /mnt/RNAi-CAM -o umask=000
@reboot sudo chmod 777 /mnt/RNAi-CAM
*/10 * * * * /usr/bin/python Recording.py
```
After adding the lines, ctl+s will save. Then use ctl+x to leave.

*NB if you want to use the camera (e.g, for preview, check focus, or to troubleshoot record.py script), turn off autoamted recording by commenting out that last line

Restart computer after updating crontab. osmiaCAM should run automatically after this.
```bash
sudo reboot -h now
```

## Lighting
In order to use the relay module to control the lights automatically, the raspberry pi, relay, and lights must be connected properly. The images below illustrate pin/wire locations on the raspberry pi and relay module. To insert wires to the relay, use a screwdriver.

![Connection from raspberry pi to relay: pins must be connected properly](guideImages/lightsOverview.jpg)
![Wire locations on raspberry pi](guideImages/lightsPi2Relay.jpg)
![Wire locations on relay connecting relay to raspberry pi](guideImages/lightsRelay2Pi.jpg)
![Wire locations on relay connecting relay to lights and power](guideImages/lightsRelay2Lights.jpg)
* Note that only the black ends should be soldered together.

The two wires coming from the relay can then be plugged into the lights and battery. The configuration does not matter.

## Turn on GPIO pins
Click on the raspberry --> settings --> Raspberry PI Configuration --> Interfaces --> turn on SPI and I2C


## Testing
Restart and come back after 20 minutes to check if expected files are in expected locations on hard drive. RNAi-CAM should be created, with FOLDER WIHTIN and the videos should be 9 min 45 s video every 10 min.

## Deployment
While deploying, it is advisable to check the focus of the camera and adjust as needed, even if the unit has been built and tested in the lab. However, if the above steps have been executed successfully, the normal functioning of the unit will interfer with this. To avoid this, edit the crontab:
```bash
crontab -e
```
Now comment out the lines that refer to dayShift and nightShift scripts. It should look like this:


Remember to uncomment these lines before actually deploying the unit. Note also that nightShift runs at startup and will put the unit to sleep after 10 seconds. If a unit must be deployed at night, edit the crontab during the day ahead of time.

## Check videos
Videos are recorded as .h264s, which are great for file sizes but a bit cumbersome to convert and view. We have written some utility functions to help out with this. 
First, for the nest and outside videos, a single frame from each video is now output automatically to check framing, etc
Second, you can first convert 'raw' h264 videos to mp4 on the pi with the 'converth264.py' function, and then view them with the 'play_mp4.py' script. Here's an example:

### Install openCV library
First if you haven't already, create a virtual environment and install openCV

```bash
cd ~
python3 -m venv rnai_2025
source rnai_2025/bin/activate
pip3 install opencv-contrib-python
```

Then run this in terminal:
```bash
cd ~
source rnai_2025/bin/activate
python3 converth264.py
```
This will prompt you for a filename. The easiest way to get this when communicating over Raspberry Pi Connect is by navigating to the h264 file you'd like to view, selecting 'copy path' under 'Edit' in the file browser, then click 'copy from remote'. Then in the window prompt, click 'paste to remote' back in the Terminal window

After a few moments (maybe a couple minutes for full sized videos), there should now be an mp4 video with the same filename. To view this file, now run:

```bash
python3 play_mp4.py
```
This will again prompt you for a filename, which now you'll have to add as the 'mp4' file, as above

### playback timelapse

```bash
source rnai_2025/bin/activate
cd ~/rnai_2025
python3 playback_stills.py
```


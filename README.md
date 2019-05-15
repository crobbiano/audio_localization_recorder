# audio_localization_recorder
Combines a 4 mic array hat for the raspi 3 and a neo 6m gps module for doing accurate temporal-spatial audio recordings

Does recording using the Seeed Studio 4-mic array raspberry pi 3b hat, and a Neo 6M GPA module.  
Every sample of the audio data is associated with a reading from the GPS to record all the fancy GPS things.

Eventually to be used to analyze algorithms for audio source detection, classification, and localization.

Uses stuff from the following:
Threaded PyAudio streaming from default audio device to a file:
https://gist.githubusercontent.com/sloria/5693955/raw/88f2f14a32deff2308e2fa332fc82b4de402c29f/recorder.py
Drivers for the 4 mic pi hat:
http://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/

## Drivers for audio
Run the following to install 4 mic array drivers:
sudo apt-get update
sudo apt-get upgrade
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh
reboot

## Packages for audio testing
Run the following commands to install necessary packages:
sudo apt-get install portaudio19-dev
sudo apt-get install python-numpy 
sudo pip3 install pyaudio
sudo pip3 install webrtcvad
sudo pip3 install pyusb

## GPS Setup
The GPS should be plugged in via USB and enumerated to /dev/ttyACM0

Run the following:
sudo apt install gpsd gpsd-clients
sudo pip3 install pynmea2

sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
! The following line may not be needed
sudo gpsd /dev/ttyACM0 -F /var/run/gpsd.sock

To check if the GPS is working, run the following command in the terminal:
cgps -s

## Operation
This sctipr assumes that the GPS is plugged in via usb.

To run the script, run the following command in the terminal:
python3 record_data.py

The mic hat will blink yellow until a sat. fix is found, then it will blink green while it is recording.  Pressing ctrl-c will stop recording and the mic hat will blink red.  Each time the program records stuff, two files are made.  The first is a wav file in logs/audio and the second is a csv file that contains time stamps and lon/lat for the device at least time stamp.  The last line in the csv contains the start and stop times of the audio recording so it can be synced across devices when processing.

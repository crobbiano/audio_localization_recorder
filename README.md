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


Run the following to install 4 mic array drivers:
sudo apt-get update
sudo apt-get upgrade
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh
reboot

Run the following commands to install necessary packages:
sudo apt-get install portaudio19-dev
sudo pip install pyaudio
sudo pip install webrtcvad
sudo apt-get install python-numpy 
sudo pip install pyusb

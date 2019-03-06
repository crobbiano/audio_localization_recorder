from utils import pixels
from audio_subsystem import audio_subsystem as recorder
import signal
import time
import os
import re

class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

def checkAudioDirs(audioLogDir='./logs/audio', fileBaseName='audioLog'):
    # check for the logs/audio directory
    if not os.path.isdir(audioLogDir):
        os.makedirs(audioLogDir)

    # find the latest audio log file
    files1 = [f for f in os.listdir(audioLogDir)]
    files = [f for f in os.listdir(audioLogDir) if re.match(r'audioLog.*\.wav', f)]

    numFiles = len(files)
    currNum = numFiles + 1
    newFileName = os.path.join(audioLogDir, fileBaseName + str(currNum) + '.wav' )

    return newFileName


if __name__=="__main__":
    killer = GracefulKiller()

    # Check to see if directories are set up and get latest filename for recording audio
    audioFile = checkAudioDirs()

    # Instantiate the Pixels class
    pixel = pixels.Pixels()
    # Blink the green lights to indicate that the recording is starting
    pixel.blinkGreenStart()

    rec = recorder.Recorder(channels=4)
    with rec.open(audioFile,'wb') as recfile:
        recfile.start_recording()
        while True:
            time.sleep(5)
            if killer.kill_now:
                break
            pixel.blinkGreen()

        recfile.stop_recording()

    pixel.blinkRedStart()
    time.sleep(1)

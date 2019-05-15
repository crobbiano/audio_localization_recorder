from utils import pixels
from audio_subsystem import audio_subsystem as recorder
import signal
import time
import os
import re
from serial import Serial
import pynmea2
#import adafruit_gps

class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

def checkDirs(audioLogDir='./logs/audio', fileBaseName='audioLog', csvLogDir='./logs/csv'):
    # check for the logs/audio directory
    if not os.path.isdir(audioLogDir):
        os.makedirs(audioLogDir)
    # check for the logs/csv directory
    if not os.path.isdir(csvLogDir):
        os.makedirs(csvLogDir)

    # find the latest audio log file
    files1 = [f for f in os.listdir(audioLogDir)]
    files = [f for f in os.listdir(audioLogDir) if re.match(r'audioLog.*\.wav', f)]

    numFiles = len(files)
    currNum = numFiles + 1
    newAudioFileName = os.path.join(audioLogDir, fileBaseName + str(currNum) + '.wav' )
    newCsvFileName = os.path.join(csvLogDir, fileBaseName + str(currNum) + '.csv' )

    return newAudioFileName, newCsvFileName

def parseGPS(serialPort):
    while 1:
        gpsStr = str(serialPort.readline(), 'utf-8', 'ignore')
        if gpsStr.find('GGA')>0:
            msg = pynmea2.parse(gpsStr)
            # print("Time: {0}, Lat: {1} {2}, Lon: {3} {4}".format(msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir))
            return msg

def writeToCsv(csvfile, msg):
    csvfile.write('{}, {}, {}, {}, {}\n'.format(
        msg.timestamp,
        msg.lat,
        msg.lon,
        msg.num_sats,
        msg.gps_qual))

if __name__=="__main__":
    killer = GracefulKiller()

    # Check to see if directories are set up and get latest filename for recording audio
    (audioFile, csvFile) = checkDirs()

    # Instantiate the Pixels class
    pixel = pixels.Pixels()

    # Setup the GPS
    updateRate = 0.1 # these values are hard coded into the GPS
    baudRate = 38400 # these values are hard coded into the GPS
    serialPort = Serial("/dev/ttyACM0", baudRate, timeout=2)
    while not parseGPS(serialPort).gps_qual:
        time.sleep(1)
        pixel.blinkYellow()
        if killer.kill_now:
            exit()
        # print('Waiting for fix..')
    # print('GOT FIX!!')
    # Blink the green lights to indicate that the recording is starting
    pixel.blinkGreenStart()

    last = time.monotonic()

    # open csv file for writing
    csvfile = open(csvFile, "w+")

    rec = recorder.Recorder(channels=4)
    with rec.open(audioFile,'wb') as recfile:
        msg = parseGPS(serialPort)
        writeToCsv(csvfile, msg)
        startTime = msg.timestamp

        recfile.start_recording()
        while True:
            current = time.monotonic()
            if current - last >= updateRate:
                last = current
                msg = parseGPS(serialPort)
                writeToCsv(csvfile, msg)
            if killer.kill_now:
                break
            pixel.blinkGreen()

        msg = parseGPS(serialPort)
        writeToCsv(csvfile, msg)
        stopTime = msg.timestamp

        recfile.stop_recording()

        # Add start and stop time to the csv
        csvfile.write(',,,,{},{}\n'.format(startTime, stopTime))
        csvfile.close()


    pixel.blinkRedStart()
    time.sleep(1)

import audio_subsystem as recorder
import time

if __name__=="__main__":
   print('recording 0')
   rec = recorder.Recorder(channels=4)
   print('recording 1')
   with rec.open('nonblocking.wav','wb') as recfile:
       recfile.start_recording()
       print('recording')
       time.sleep(5)
       recfile.stop_recording()

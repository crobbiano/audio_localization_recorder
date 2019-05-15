try:
    from . import apa102
except SystemError:
    import apa102
import time
import threading
from gpiozero import LED
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

try:
    from .custom_pattern import customPattern
except SystemError:
    from custom_pattern import customPattern

class Pixels:
    PIXELS_N = 12

    def __init__(self, pattern=customPattern):
        self.pattern = pattern(show=self.show)

        self.dev = apa102.APA102(num_led=self.PIXELS_N)

        self.power = LED(5)
        self.power.on()

        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

        self.last_direction = None

    def wakeup(self, direction=0):
        self.last_direction = direction
        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        if self.last_direction:
            def f():
                self.pattern.wakeup(self.last_direction)
            self.put(f)
        else:
            self.put(self.pattern.listen)

    def blinkGreenStart(self):
        self.put(self.pattern.blinkGreenStart)

    def blinkGreen(self):
        self.put(self.pattern.blinkGreen)

    def blinkYellow(self):
        self.put(self.pattern.blinkYellow)

    def blinkRedStart(self):
        self.put(self.pattern.blinkRedStart)

    def blinkRed(self):
        self.put(self.pattern.blinkRed)

    def think(self):
        self.put(self.pattern.think)

    def speak(self):
        self.put(self.pattern.speak)

    def off(self):
        self.put(self.pattern.off)

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))

        self.dev.show()




if __name__ == '__main__':
    pixels = Pixels()
    while True:

        try:
            pixels.blinkGreen()
            time.sleep(1)
            pixels.blinkRed()
            time.sleep(1)
        except KeyboardInterrupt:
            print('saw some funny business')
            break


    pixels.off()
    time.sleep(1)

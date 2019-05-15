#!/usr/bin/env python

# Copyright (C) 2017 Seeed Technology Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import numpy
import time


class customPattern(object):
    def __init__(self, show=None, number=12):
        self.pixels_number = number
        self.pixels = [0] * 4 * number

        if not show or not callable(show):
            def dummy(data):
                pass
            show = dummy

        self.show = show
        self.stop = False

    def wakeup(self, direction=0):
        position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number

        pixels = [0, 0, 0, 24] * self.pixels_number
        pixels[position * 4 + 2] = 48

        self.show(pixels)

    def listen(self):
        pixels = [0, 0, 0, 24] * self.pixels_number

        self.show(pixels)

    def blinkGreenStart(self):
        pixels_on  = [ 0, 0, 5, 0] * self.pixels_number
        pixels_off  = [ 0, 0, 0, 0] * self.pixels_number

        for x in range(3):
            self.show(pixels_on)
            time.sleep(0.2)
            self.show(pixels_off)
            time.sleep(0.2)

    def blinkGreen(self):
        pixels_on  = [ 0, 0, 5, 0] * self.pixels_number
        pixels_off  = [ 0, 0, 0, 0] * self.pixels_number

        self.show(pixels_on)
        time.sleep(0.2)
        self.show(pixels_off)
        time.sleep(0.2)

    def blinkYellow(self):
        pixels_on  = [ 0, 5, 5, 0] * self.pixels_number
        pixels_off  = [ 0, 0, 0, 0] * self.pixels_number

        self.show(pixels_on)
        time.sleep(0.2)
        self.show(pixels_off)
        time.sleep(0.2)

    def blinkRedStart(self):
        pixels_on  = [ 0, 5, 0, 0] * self.pixels_number
        pixels_off  = [ 0, 0, 0, 0] * self.pixels_number

        for x in range(3):
            self.show(pixels_on)
            time.sleep(0.2)
            self.show(pixels_off)
            time.sleep(0.2)

    def blinkRed(self):
        pixels_on  = [ 0, 5, 0, 0] * self.pixels_number
        pixels_off  = [ 0, 0, 0, 0] * self.pixels_number

        self.show(pixels_on)
        time.sleep(0.2)
        self.show(pixels_off)
        time.sleep(0.2)

    def think(self):
        pixels_on  = [ 0, 5, 0, 0] * self.pixels_number
        pixels_off  = [ 0, 0, 0, 0] * self.pixels_number
        #pixels_on  = [ 0, 0, 5, 0] * self.pixels_number
        #pixels_off  = [ 0, 0, 0, 0] * self.pixels_number

        while not self.stop:
            self.show(pixels_off)
            time.sleep(0.5)
            self.show(pixels_on)
            time.sleep(0.5)
            #pixels_off = pixels_off[-4:] + pixels_off[:-4]

    def speak(self):
        step = 1
        position = 12
        while not self.stop:
            pixels  = [0, 0, position, 24 - position] * self.pixels_number
            self.show(pixels)
            time.sleep(0.01)
            if position <= 0:
                step = 1
                time.sleep(0.4)
            elif position >= 12:
                step = -1
                time.sleep(0.4)

            position += step

    def off(self):
        self.show([0] * 4 * 12)

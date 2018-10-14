# MIT License

# Copyright (c) 2018 Freedge.org

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================

import os
import cv2
import datetime
import RPi.GPIO as GPIO


class device:
    def __init__(self,id):
        self.id = id;

class camera(device):
    def __init__(self, port = None, **kwargs):
        self.port = device
        super(Camera,self).__init__(**kwargs)

    def getinput(self):
        print("\nTaking photo from camera %s"% self.device)
        capture = cv2.VideoCapture(self.device)

        #variable***
        capture.set(3,640)  # CV_CAP_PROP_FRAME_WIDTH
        capture.set(4,480)  # CV_CAP_PROP_FRAME_HEIGHT

        # return image
        image = capture.read()

        if not ret:
            print('Cannot read camera %s' % self.device)
            capture.release()
            return None

        capture.release()
        return image

# Magnetic Switch runs in BCM mode (convert input)
GPIO.setmode(GPIO.BCM)

class switchsensor:
    def __init__(self, port, wait_time, **kwargs):
        self.port = port
        self.in_open_state = False
        self.wait_time = wait_time
        self.last_open = time.time()
        self.last_close = time.time()
        super(switchsensor, self).__init__(**kwargs)

        # Set up the door sensor port.
        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_open(self):
        # 0 : Close // 1 : Open
        is_openning = bool(GPIO.input(self.port))
        if is_openning and not self.in_open_state:
            self.in_open_state = True
            self.last_open = time.time()
        elif not is_openning and self.in_open_state:
            self.in_open_state = False
            self.last_close = time.time()
        return is_openning

    def is_recently_closed(self):
        if time.time() - self.last_close < self.wait_time:
            return True
        else:
            return False

    def get_active_period(self):
        return self.last_close - self.last_open

    def cleanup(self):
        GPIO.cleanup()

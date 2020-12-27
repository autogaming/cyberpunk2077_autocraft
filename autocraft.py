import time
import threading
import pyautogui
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener, KeyCode, Key, Controller as KeyboardController
import sys
import win32gui

# A method to get the location of the mouse

# print('Press Ctrl-C to quit.')
# try:
#     while True:
#         # x, y = pyautogui.position()
#         # positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         # print(positionStr, end='')
#         # print('\b' * len(positionStr), end='', flush=True)
        
#         flags, hcursor, (x,y) = win32gui.GetCursorInfo()
#         positionStr = 'X: ' + str((x,y)[0]).rjust(4) + ' Y: ' + str((x,y)[1]).rjust(4)
#         print(positionStr, end='')
#         print('\b' * len(positionStr), end='', flush=True)
#         # print((x,y)[0])
# except KeyboardInterrupt:
#     print('\n')

def on_press(key):
    if key == start_stop_key:
        if click_thread.crafting:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()

class Craft(threading.Thread):
    global count
    
    def __init__(self, delay, button):
        super(Craft, self).__init__()
        self.delay = delay
        self.button = button
        self.crafting = False
        self.disassembling = False
        self.program_running = True

    def start_clicking(self):
        self.disassembling = False
        self.crafting = True

    def stop_clicking(self):
        self.crafting = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        count = 0
        while self.program_running:
            while self.crafting:
                # Crafting limit
                if count >= 5000:
                    self.crafting = False
                    count = 0
                mouse.press(self.button)
                time.sleep(self.delay)
                mouse.release(self.button)
                print("Click number " + str(count))
                count += 1
            time.sleep(0.1)

#key to start and stop
start_stop_key = KeyCode(char='s')

#key to quit crafting
exit_key = KeyCode(char='q')

button = Button.left

#Hold down time
delay = 0.15

click_thread = Craft(delay, button)
mouse = MouseController()
keyboard = KeyboardController()
click_thread.start()

with Listener(on_press=on_press) as listener:
    listener.join()

from .randombuttonbox import RandomButtonBox
from .common import GPIOButtonFactory
import RPi.GPIO as GPIO
#import RPiSim.GPIO as GPIO

class ButtonBox:
    def __init__(self):
        factory = GPIOButtonFactory(GPIO)
        buttons = RandomButtonBox(factory)
        buttons.start()
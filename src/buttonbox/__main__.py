from .randombuttonbox import RandomButtonBox
from .common import GPIOButtonFactory
import RPi.GPIO as GPIO
#import RPiSim.GPIO as GPIO

factory = GPIOButtonFactory(GPIO)
buttons = RandomButtonBox(factory)
buttons.start()


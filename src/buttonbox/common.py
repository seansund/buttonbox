class Observable:
    def __init__(self):
        self.observers = []
 
    def register(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)
 
    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
 
    def unregister_all(self):
        if self.observers:
            del self.observers[:]
 
    def update_observers(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(*args, **kwargs)

class Observer:
    def update(self, *args, **kwargs):
        pass

class Button(Observable):
    def __init__(self, button_pin, led_pin):
        Observable.__init__(self)
        
        self.button_pin = button_pin
        self.led_pin = led_pin
        self._selected = None
   
    @property
    def selected(self):
        """I'm the 'selected' property."""
        return self._selected
    @selected.setter
    def selected(self, value):
        self._selected = value
    @selected.deleter
    def selected(self):
        del self._selected
    
    def press(self):
        self.update_observers(self)

class SimpleButtonFactory:
    def getButtons(self):
        return [Button(1,2), Button(3,4), Button(5,6), Button(7,8), Button(9,10), Button(11,12)]


class GPIOButton(Button):
    def __init__(self, GPIO, button_pin, led_pin):
        Button.__init__(self, button_pin, led_pin)
        
        self.GPIO = GPIO
        
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(led_pin, GPIO.OUT, initial = GPIO.LOW)
        
        # add and event listener for 'RISING' (button press)
        GPIO.add_event_detect(button_pin, GPIO.RISING, callback=self.hw_button_callback)
    
    def hw_button_callback(self, channel):
        print('This is a edge event callback function!')
        print('Edge detected on channel %s'%channel)
        # trigger the internal button 'press' event
        self.press()
    
    @Button.selected.setter
    def selected(self, value):
        self._selected = value
        
        # change the value on the LED pin based on 'selected'
        if value:
            print('LED(' + str(self.led_pin) + '): on')
            self.GPIO.output(self.led_pin, self.GPIO.HIGH)
        else:
            print('LED(' + str(self.led_pin) + '): off')
            self.GPIO.output(self.led_pin, self.GPIO.LOW)
        
class GPIOButtonFactory:
    def __init__(self, GPIO):
        # init GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        #[4,17,27,22,5,6,13,26]
        #[18,23,24,25,12,16]
        #GPIONames = [14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21, 2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]
        
        self.buttons = [GPIOButton(GPIO,4,17), GPIOButton(GPIO,27,22), GPIOButton(GPIO,5,6), GPIOButton(GPIO,13,26), GPIOButton(GPIO,18,23), GPIOButton(GPIO,24,25)] 
        
    def getButtons(self):
        return self.buttons

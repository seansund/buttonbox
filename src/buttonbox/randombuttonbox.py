import random
from .common import Observer

class RandomButtonBox(Observer):
    def __init__(self, buttonFactory):
        self.buttons = buttonFactory.getButtons()
    
    def start(self):
        # register as observer for buttons to watch for button press
        for b in self.buttons:
            b.register(self)
        
        # randomly select one of the buttons to start
        return self.select_random_button(self.buttons)
    
    def update(self, *args, **kwargs):
        pressed_button = args[0]
        if pressed_button.selected == True:
            new_list = self.list_without_buttons(pressed_button)
            
            pressed_button.selected = False
            self.select_random_button(new_list)
        else:
            pass
    
    def list_without_buttons(self, button):
        index = self.buttons.index(button)
        
        new_list = []
        if index == 0:
            new_list = self.buttons[1:]
        elif index == len(self.buttons)-1:
            new_list = self.buttons[0:(index)]
        else:
            new_list = self.buttons[0:(index)] + self.buttons[(index+1):]
        
        return new_list
        
    def select_random_button(self, button_list):
        index = random.randint(0, len(button_list)-1)
        selected_button = button_list[index];
        selected_button.selected = True
        
        return selected_button

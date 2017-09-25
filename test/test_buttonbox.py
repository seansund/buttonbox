import unittest

import RPiSim.GPIO as GPIO
from buttonbox.common import Observable
from buttonbox.common import Observer
from buttonbox.common import Button
from buttonbox.common import SimpleButtonFactory
from buttonbox.common import GPIOButtonFactory
from buttonbox.randombuttonbox import RandomButtonBox

class TestObserver(Observer):
    def __init__(self):
        self.args = []
        self.kwargs = {}

    def update(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return    

class TestButton(unittest.TestCase):
    def setUp(self):
        self.button = Button(1,2)
        self.observer = TestObserver()
        
    def test_button_create(self):
        self.assertEqual(1, self.button.button_pin, "Button pin should match")
    
    def test_before_register_observers(self):
        self.assertEqual(0, len(self.button.observers), "Observers should be empty initially")
    
    def test_register_one_observer(self):
        self.button.register(self.observer)
        self.assertEqual(1, len(self.button.observers), "Observers should have 1 item after register")
    
    def test_unregister_observer(self):
        self.button.register(self.observer)
        self.button.unregister(self.observer)
        self.assertEqual(0, len(self.button.observers), "Observers should be empty after unregister")
    
    def test_button_pressed(self):
        self.button.register(self.observer)
        self.button.press()
        
        self.assertEqual(self.observer.args[0].button_pin, self.button.button_pin, "Button should be the same")

factory = GPIOButtonFactory(GPIO)

class TestRandomButtonBox(unittest.TestCase):
    def setUp(self):
        #factory = SimpleButtonFactory()
        self.box = RandomButtonBox(factory)
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        GPIO.cleanup()
        
    def test_buttonbox_create(self):
        self.assertEqual(6, len(self.box.buttons), "should have 6 buttons")
    
    def test_remove_first_button(self):
        buttons = self.box.buttons
        
        button = buttons[0]
        new_list = self.box.list_without_buttons(button)
        
        self.assertNotEqual(button.button_pin, new_list[0].button_pin, "The first item should be removed from the list")
        self.assertEqual(len(buttons)-1, len(new_list), "The new list should have one fewer elements")
    
    def test_remove_last_button(self):
        buttons = self.box.buttons
        
        button = buttons[len(buttons)-1]
        new_list = self.box.list_without_buttons(button)
        
        self.assertNotEqual(button.button_pin, new_list[len(new_list)-1].button_pin, "The last item should be removed from the list")
        self.assertEqual(len(buttons)-1, len(new_list), "The new list should have one fewer elements")
    
    def test_remove_middle_button(self):
        buttons = self.box.buttons
        
        index = 3
        button = buttons[index]
        new_list = self.box.list_without_buttons(button)
        
        self.assertNotEqual(button.button_pin, new_list[index].button_pin, "The middle item should be removed from the list")
        self.assertNotEqual(button.button_pin, new_list[index-1].button_pin, "The middle item should be removed from the list")
        self.assertNotEqual(button.button_pin, new_list[index+1].button_pin, "The middle item should be removed from the list")
        self.assertEqual(len(buttons)-1, len(new_list), "The new list should have one fewer elements")
    
    def test_buttonbox_start(self):
        button = self.box.start()
        
        self.assertEqual(True, button.selected, "First button should be selected")
    
    def test_buttonbox_next(self):
        button = self.box.start()
        
        button.press()
        self.assertEqual(False, button.selected, "Button should not be selected after pressed")

    def find_selected_button(self, button_list):
        selected_button = None
        
        for button in button_list:
            if button.selected:
                selected_button = button
                break
        
        return selected_button
    
    def test_buttonbox_next2(self):
        button = self.box.start()
        buttons = self.box.buttons
        
        prev_button = None
        for x in range(0, 6):
            button.press()
            
            if prev_button is not None:
                self.assertNotEqual(button.button_pin, prev_button.button_pin, "Next button should not be same as previous")
            
            prev_button = button
            button = self.find_selected_button(buttons)
            self.assertTrue(button is not None, "Button should be selected")
        

if __name__ == '__main__':
    unittest.main()
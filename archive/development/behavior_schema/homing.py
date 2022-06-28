class Homing:
    def __init__(self):
        self.done = False
        
    def home(self):
        if self.done:
            # go home
            return True
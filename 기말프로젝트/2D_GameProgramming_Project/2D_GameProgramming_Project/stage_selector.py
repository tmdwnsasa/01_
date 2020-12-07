import gfw
from pico2d import *

class stage:
    def __init__(self):
        self.stage_num = 1
        self.kill_count = 0

    def update(self):
        if self.kill_count >= 5 + self.stage_num and self.stage_num < 4:
            self.stage_num += 1
            self.kill_count = 0
    
    def bg_selector(self):
        if self.stage_num == 1:
            return 'res/dawn.png'
        if self.stage_num == 2:
            return 'res/Background.png'
        if self.stage_num == 3:
            return 'res/evening.png'
        if self.stage_num == 4:
            return 'res/night.png'

import pandas as pd
from time import sleep
from functools import partial
import datetime as dt


# String to date
s2d = partial(pd.to_datetime, dayfirst=True)


def save_csv(df, name):
    df.to_csv(f'../data/wz2017_{name}.csv', index=False)


def load_csv(name):
    df = pd.read_csv(f'../data/wz2017_{name}.csv.gz')
    df.entry_date = pd.to_datetime(df.entry_date)    
    return df


# Canvas
from ipywidgets import Play, IntProgress, HBox, VBox, link
from ipycanvas import Canvas, hold_canvas
import math
from time import sleep
from threading import Thread
from ipywidgets import Image
from ipycanvas import MultiCanvas, hold_canvas


class _Clock(Thread):
    def _current_time(self):    
        while True:
            now = dt.datetime.now()
            yield now.hour, now.minute, now.second
            sleep(0.1)        
            
    def draw(self, hour, minute, second=None):    
        pass
    
    def run(self):
        for (hour, minute, second) in self.time_keeper:
            self.draw(hour, minute, second)    



class WallClock(_Clock):
    def __init__(self, face_canvas, hand_canvas, x, y, radius, clock=None):
        self.face_canvas = face_canvas
        self.canvas = hand_canvas
        self.x = x
        self.y = y
        self.radius = radius
        if clock is not None:
            self.time_keeper = clock     
        else:
            self.time_keeper = self._current_time()                
        self.draw_face()
        self.draw(12, 0, 0)
        super(WallClock, self).__init__()
        
    def draw_face(self): 
        with hold_canvas(self.face_canvas):
            self.face_canvas.reset_transform()            
            self.face_canvas.translate(self.x, self.y)            
            self.face_canvas.translate(self.radius, self.radius)
            # Outline
            self.face_canvas.stroke_arc(0, 0, self.radius, 0, 2 * math.pi)
            # Center dot
            self.face_canvas.stroke_arc(0, 0, self.radius * 0.1, 0, 2 * math.pi)
            self.face_canvas.fill_style = '#333'
            self.face_canvas.fill()
            # numbers
            self.face_canvas.font = str(self.radius * 0.15) + "px arial"
            self.face_canvas.text_baseline = "middle"
            self.face_canvas.text_align = "center"
            for num in range(1, 13):
                ang = num * math.pi / 6
                self.face_canvas.rotate(ang);
                self.face_canvas.translate(0, -self.radius * 0.85)
                self.face_canvas.rotate(-ang)
                self.face_canvas.fill_text(str(num), 0, 0)
                self.face_canvas.rotate(ang)
                self.face_canvas.translate(0, self.radius * 0.85)
                self.face_canvas.rotate(-ang)        

    def draw_hand(self, pos, length, width):    
        self.canvas.begin_path()
        self.canvas.line_width = width
        self.canvas.line_cap = "round"
        self.canvas.move_to(0, 0)
        self.canvas.rotate(pos)
        self.canvas.line_to(0, -length)
        self.canvas.stroke()
        self.canvas.rotate(-pos)        

    def draw_time(self, hour, minute, second=None):
        if second is not None:
            second = (second * math.pi / 30)
            self.draw_hand(second, self.radius * 0.9, self.radius * 0.02)
        else:
            second = 0
        hour = (hour * math.pi / 6) + (minute * math.pi / (6*60)) + (second * math.pi / (360 * 60))
        self.draw_hand(hour, self.radius * 0.5, self.radius * 0.07)
        minute = (minute * math.pi / 30) + (second * math.pi / (30 * 60))
        self.draw_hand(minute, self.radius * 0.8, self.radius * 0.07)

    def draw(self, hour, minute, second=None):
        with hold_canvas(self.canvas):
            self.canvas.reset_transform()
            self.canvas.clear()
            self.canvas.translate(self.x, self.y)
            self.canvas.translate(self.radius, self.radius)
            self.draw_time(hour, minute, second)             
            
            
class DigitalClock(_Clock):
    def __init__(self, canvas, x, y, clock=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        if clock is not None:
            self.time_keeper = clock     
        else:
            self.time_keeper = self._current_time()
        self.canvas.font = "30pt calibri"
        self.draw(0, 0)
        super(DigitalClock, self).__init__()        
    
    def _pad(self, digit):
        return f'0{digit}' if digit < 10 else str(digit)
    
    def draw(self, hour, minute, second=None):
        with hold_canvas(self.canvas):
            time = [self._pad(hour), self._pad(minute)]
            if second is not None:
                time.append(self._pad(second))
            self.canvas.clear()
            self.canvas.fill_text(':'.join(time), self.x, self.y)
            
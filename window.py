from tkinter import Tk, BOTH, Canvas
from time import time


class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Test Title")
        self.canvas = Canvas(self.root, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        
    def close(self):
        self.running = False
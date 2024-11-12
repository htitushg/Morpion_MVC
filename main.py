#!/usr/bin/env python3.6
import tkinter as tk
from controller import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Jeu du morpion')

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(self, view)

        # set the controller to view
        view.set_controller(controller)

if __name__ == '__main__':
    app=App()
    app.mainloop()
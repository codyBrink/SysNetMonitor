# a simple little network host monitor that uses ping
# Author: Cody Brink
import tkinter as tk

import Controller.MonitorController as monitor

if __name__ == "__main__":
    root = tk.Tk()
    controller = monitor.MonitorController()
    root.config(menu=controller.view.menubar)
    controller.init()
    controller.view.pack(fill="both", expand=True)
    root.protocol("WM_DELETE_WINDOW", controller.endProgram)
    root.mainloop()
# contains the GUI widgets for the Monitoring portion of the program
import tkinter as tk

class MonitorView(tk.Frame):
    def __init__(self):
        super().__init__()

        # creation of menubar
        self.menubar = tk.Menu()

        # creation of the menubar item configure
        self.config_menu = tk.Menu(self.menubar)

        # adds the config_menu to the menubar
        self.menubar.add_cascade(label="Configure", menu=self.config_menu)

        # frame to hold the watchlist and entry field
        self.topFrame = tk.Frame(self)
        self.topFrame.pack(side="top", fill="both", expand=True)

        # frame to hold the watch list area
        self.watchListFrame = tk.Frame(self.topFrame)
        self.watchListFrame.pack(side="left", fill="both", expand=True)

        # widgets for the watchlist area
        self.removeJobBtn = tk.Button(self.watchListFrame, text="remove selected job")
        self.removeJobBtn.pack(side="top", fill="both")

        self.jobsListLbl = tk.Label(self.watchListFrame, text="List of monitored hosts:")
        self.jobsListLbl.pack(side="top", fill="both")

        self.jobsList = tk.Listbox(self.watchListFrame, borderwidth=3)
        self.jobsList.pack(side="bottom", fill="both", expand=True)

        # frame to hold the entry data to create jobs
        self.jobEntryFrame = tk.Frame(self.topFrame)
        self.jobEntryFrame.pack(side="right", fill="both", expand=True)

        self.entryLbl = tk.Label(self.jobEntryFrame, text="Enter a IP address or Hostname to start monitoring:")
        self.entryLbl.pack(side="top", fill="x")

        self.hostTextField = tk.Entry(self.jobEntryFrame, borderwidth=3)
        self.hostTextField.pack(side="left", fill="x", expand=True)

        self.addJobBtn = tk.Button(self.jobEntryFrame, text="Submit")
        self.addJobBtn.pack(side="right", fill="x", expand=True)

        # frame to hold any error messages
        self.errMsgFrame = tk.Frame(self)
        self.errMsgFrame.pack(side="bottom", fill="both", expand=True)

        self.errList = tk.Listbox(self.errMsgFrame, borderwidth=3)
        self.errList.pack(fill="both", expand=True)

from Controller.Controller import Controller
from View.MonitorView import MonitorView
from Model.MonitorModel import MonitorModel
from Utils.Helper import createConfig, getCurTimeStamp
import sys
from pathlib import Path

class MonitorController(Controller):
    def __init__(self):
        super().__init__()
        self.view = MonitorView()
        self.model = MonitorModel()

    # method gets called when the window closes
    def endProgram(self):
        for job in self.model.jobs:
            host = self.model.jobs.get(job)
            host.process.stop()
        sys.exit()

    # gets the currently selected job from the list
    def getSelectedJob(self):
        try:
            host = self.view.jobsList.get(self.view.jobsList.curselection())
            print("host is:",host)
            self.model.removeJob(host)
        except:
            self.model.writeErr(getCurTimeStamp()+"could not remove job. no item was selected from the list")

    # gets config file
    def getConfig(self):
        # checks to see if a config file doesn't exist
        configFile = Path("data files//config.txt")
        if not configFile.is_file():
            createConfig()
        # reads from the config file
        try:
            with open("data files//config.txt") as configReader:
                configData = configReader.readlines()
                # gets the values we need for the monitor flow from the config file
                # and assigns them accordingly 
                for line in configData:
                    if "threshold" in line.rstrip():
                        self.model.pingFailureThreshold = int(line.split(":")[1].strip())
        except Exception as err:
            with open("logs//err.log", "a+") as errWriter:
                errWriter.write(getCurTimeStamp()+str(err))

    # overriding parent method
    def init(self):
        # method binds
        self.view.addJobBtn.bind("<Button-1>", lambda e: self.model.startMonitoring(
            self.view.hostTextField.get()))
        self.view.removeJobBtn.bind("<Button-1>", lambda e: self.getSelectedJob())

        # subscribes the job list to the StringVar stored in the model
        self.view.jobsList.configure(listvariable=self.model.jobsSubscriberList)
        # subscribes the error list widget to the error list subscription
        self.view.errList.configure(listvariable=self.model.errSubscriberList)

        # gets config file and assign the values needed from it and
        # resume any jobs for any hosts found in the jobs.txt file
        self.getConfig()
        self.model.resumeJobs()


import tkinter as tk
from Model.Host import Host
from Utils.Process import Process
from Utils.Helper import validateHost, getCurTimeStamp
from Utils.Network import runPing

class MonitorModel():
    def __init__(self):

        # list to store all the current hosts that we have jobs for
        self.jobs = {}

        # StringVar to display all the current hosts being monitored in the view
        self.jobsSubscriberList = tk.StringVar()

        # list to hold error messages
        self.errMsgs = []

        # tkinter StringVar to update the error list in the view
        self.errSubscriberList = tk.StringVar(value=self.errMsgs)

        # path to error log
        self.errLog = ""

        # gotten from the config file
        self.pingFailureThreshold = ""

    # method to look for any jobs in the jobs.txt and resume them
    def resumeJobs(self):
        with open("data files//jobs.txt") as jobReader:
            jobs = jobReader.readlines()
            # filters out newline chars
            for job in jobs:
                if job == "\n":
                    pass
                else:
                    self.createPingProcess(job.rstrip())

    # method to write to and update subscriber list
    def writeErr(self, msg):
        self.errMsgs.append(msg)
        self.errSubscriberList.set(self.errMsgs)



    # creates the ping job
    def createPingProcess(self, host):
        # creates a thread for this ping job
        pingProc = Process(runPing, host, self.failedPingHandler)
        pingProc.start()

        # creates a Host object and
        # adds the host and the associated object to the jobs dictionary
        self.jobs[host] = Host(host, pingProc)
        # updates the subscribed job list (casts it to a list to have it
        # appear correctly in the listbox)
        self.jobsSubscriberList.set(list(self.jobs.keys()))

    # method that starts monitoring a host
    def startMonitoring(self, host):
        try:
            # check to see if the target is already in the list
            with open("data files/jobs.txt") as hosts:
                for job in hosts.readlines():
                    # using rstrip() to remove trailing new line
                    if host == job.rstrip():
                        self.writeErr(getCurTimeStamp()+"host is already being monitored")
                        return
            # checks to see if the given host is a valid entry and is active
            validationRes = validateHost(host)
            # returns a value of 0 if everything went okay
            if validationRes != 0:
                self.writeErr(getCurTimeStamp()+"error when adding host '%s': %s" % (host, validationRes))
                return

            # add host to file
            writer = open("data files/jobs.txt", "a+")
            writer.write(host + "\n")
            writer.close()
            self.createPingProcess(host)
        except Exception as err:
            self.writeErr(str(err))

    # method that gets returned from the ping job and determines if a email needs to be sent
    def failedPingHandler(self, host, res):
        try:
            curHost = self.jobs.get(host)
            # if the ping was successful
            if res == 0:
                # if the host object has a 0 for the amount of fails, than nothing needs to be done
                if curHost.fails == 0:
                    return
                else:
                    # if it's not, than write to the failed pings log that it's back up and
                    # and set the amount of fails of the host object back to 0
                    with open("logs//failedPings.log", "a") as logWriter:
                        logWriter.write(getCurTimeStamp() + "host %s is backup!" % (host))
                    self.writeErr(getCurTimeStamp() + "host %s is backup!" % (host))
                    curHost.fails = 0
            # anything returned should indicate an failed response
            else:
                # if the current host fails is greater than the threshold, it indicates
                # that an email alert has been sent out and still waiting for it to come back up
                if curHost.fails > self.pingFailureThreshold:
                    return
                elif curHost.fails == self.pingFailureThreshold:
                    with open("logs//failedPings.log", "a") as logWriter:
                        err = (getCurTimeStamp() + "host '%s' has not responded within the given threshold. "
                                                "sending alert email!" % (host))
                        logWriter.write(err)
                    self.writeErr(err)
                    curHost.fails = curHost.fails + 1

                elif curHost.fails < self.pingFailureThreshold:
                    with open("logs//failedPings.log", "a") as logWriter:
                        err = (getCurTimeStamp() + "host '%s' did not respond. number of consistent failures: %s" % (
                        host, curHost.fails))
                        logWriter.write(err)
                    self.writeErr(err)
                    curHost.fails = curHost.fails + 1
        except Exception as err:
            print(err)

        # removes a selected job
        def removeJob(self, host):
            # removes the host from jobs dictionary
            curHost = self.jobs.get(host)
            curHost.process.stop()
            self.jobs.pop(host)
            self.jobsSubscriberList.set(list(self.jobs.keys()))

            # removes the host from the jobs.txt file
            with open("data files//jobs.txt", "r+") as jobReader:
                jobs = jobReader.readlines()
                for i in range(len(jobs)):
                    if jobs[i].rstrip() == host:
                        # sets the value to removed so we know to skip it
                        # when writing back to the file
                        jobs[i] = "removed"
                        break
                # truncates the size of the file to 0 (effectively clearing it out)
                jobReader.truncate(0)
                # sets the cursor position back to the beginning of the file
                jobReader.seek(0)
                # rewrites the data back to the file
                for job in jobs:
                    if job == "removed":
                        pass
                    else:
                        jobReader.write(job.strip(" ") + "\n")
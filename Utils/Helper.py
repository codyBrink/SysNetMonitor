# file to store some helper methods
import re
from datetime import datetime
from Utils.Network import runPing
# method to validate ip addresses and hostnames
def validateHost(host):
    failedFormatChk = ""
    # pattern for ip address
    ipAdressPat = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    # pattern for hostname
    hostnamePat = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"

    isValidIP = re.search(ipAdressPat, host)

    if isValidIP:
        pass
    else:
        isValidHostname = re.search(hostnamePat, host)
        if isValidHostname:
            pass
        else:
            failedFormatChk = True

    if failedFormatChk == True:
        return "host address given was not a valid IP address or hostname"
    else:
        # runs a single ping to test if the host will respond
        return runPing(host)


# method to return current time formatted
def getCurTimeStamp():
    curTime = datetime.now()
    formattedTs = curTime.strftime("[%m/%d/%Y %H:%M:%S] ")
    return formattedTs

#creates default config file if one doesn't exist
def createConfig():
    # default values
    defVal = ["threshold: 10\n"]
    try:
        with open("data files//config.txt", "w+") as configFileWriter:
            for val in defVal:
                configFileWriter.write(val)

    except Exception as err:
        print(err)
# network related functions
import subprocess
import time

# method for ping processes
def runPing(target, callback=None):
    # buffer size set to 1 so it will return a response after 1 ping
    ping = subprocess.run(["ping", target, "-n", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        bufsize=1)
    result = str(ping.stdout)
    time.sleep(1)
    # if there was a reply
    if "TTL=" in result:
        if callback != None:
            callback(target, 0)
        else:
            return 0

    # if there wasn't a reply
    elif "Request timed out" in result:
        if callback != None:
            callback(target, 1)
        else:
            return "the echo request to the given host timed out, amount of failed attempts:"

    # if it returns destination host unreachable or any of those errors
    else:
        if callback != None:
            callback(target, 2)
        else:
            return "an error occurred, the destination maybe unreachable or could be a connection problem."

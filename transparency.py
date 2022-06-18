import processinfo
import dnslookup
import updatefile
import webserver
import time
import os
import pickle
from datetime import datetime

# Create a global variable which will be utilized by each thread
# Check if the serialized variable already exists
if(os.path.exists("output.pickle")):
    with open("output.pickle", "rb") as f:
        processes = pickle.load(f)
else:
    processes = {}

print("Starting at", datetime.today().strftime('%Y-%m-%d %I:%M%p'))

# This thread gathers information about currently
# running processes and their network connections
processInfo_thread = processinfo.ProcessInfo(processes)

# This thread uses a local geolite2 database to find
# location information for IP addresses
dnsLookup_thread = dnslookup.DNSLookup(processes)

# This thread writes the global dictionary
# to a file every 5 minutes
updateFile_thread = updatefile.UpdateFile(processes)

# This thread runs the webserver
webserver_thread = webserver.WebServer(processes)

# start the threads
processInfo_thread.start()
dnsLookup_thread.start()
updateFile_thread.start()
webserver_thread.start()

import ipaddress
import socket
import time
import copy
from datetime import datetime
from geoip import geolite2
from threading import Thread

# python -m pip install ipaddress
# python -m pip install python-geoip
# python -m pip install python-geoip-geolite2  // This is a free MaxMind Geolite2 database

class DNSLookup(Thread):

    '''
    This thread uses a local geolite2 database to find
    location information for IP addresses

    Inputs: global dictionary named "processes" which contains IP addresses,
            and a local geolite2 database
    Processing: Lookup location information for all IP addresses in the
            processes dictionary
    Outputs: Update the processes dictionary with the IP address location
            information
    '''

    def __init__(self, processes):
        # Call the Thread class's init function
        Thread.__init__(self)

        # Add the global dictionary to self
        self.processes = processes

    def run(self):
        # This is a method of the Thread class
        # which is called after Thread.start()

        # Lookup DNS/location information for all
        # IP addresses
        while(1):
            # number of seconds to wait before
            # updating dns/location information
            # Every 5 minutes
            wait_time = 300
            time.sleep(wait_time)

            # Iterate through all processes
            # To avoid the "RuntimeError: dictionary changed size during iteration"
            # error we are making a copy of the dict and iterating over that

            self.processes_copy = copy.deepcopy(self.processes)
            for process in self.processes_copy:
                # Extract the Remote IP dictionary
                for ip in self.processes_copy[process][3]:
                    try:
                        # Check if the ip address is valid
                        # it will generate an exception if it's not
                        is_valid_ip = ipaddress.ip_address(ip)
                    except Exception as e:
                        print(e)
                        # skip to the next ip address
                        continue

                    try:
                        # Attempt to lookup the ip address in geolite2
                        # database, if it's not found then continue to
                        # next ip. Below is an example of what ip_info should store
                        #   ip_info = {'ip': '2001:4860:4860::8888', 'country': 'US',
                        #   'continent': 'NA', 'subdivisions': frozenset(),
                        #   'timezone': 'None', 'location': (39.76, -98.5)}
                        ip_info = geolite2.lookup(ip).to_dict()
                    except Exception as e:
                        continue

                    try:
                        # Check if the database has subdivision information
                        # In the US this would be the state.
                        ip_info["subdivisions"] = list(ip_info["subdivisions"])[0]
                    except:
                        # Make the subdivion blank if there's nothing in the
                        # geolite2 database
                        ip_info["subdivisions"] = ""

                    try:
                        # Do a DNS lookup if there is not already a domain for
                        # that IP address
                        if(self.processes_copy[process][3][ip][0] == ""):
                            try:
                                # Add the time the domain is first found
                                current_time = datetime.today().strftime('%Y-%m-%d %I:%M%p')
                                # Add the time
                                self.processes[process][3][ip][5] = current_time
                            except:
                                current_time = ""
                                # Add the time
                                self.processes[process][3][ip][5] = current_time

                            # lookup domain
                            domain = socket.gethostbyaddr(ip)[0]
                            # add domain
                            self.processes[process][3][ip][0] = domain

                    except:
                        # DNS lookup failed
                        pass

                    # '8.8.8.8':[domain, country, continent, subdivisions, [latitude, longitude], time]

                    try:
                        # Add the country
                        self.processes[process][3][ip][1] = ip_info["country"]
                        # Add the continent
                        self.processes[process][3][ip][2] = ip_info["continent"]
                        # Add the subdivision
                        self.processes[process][3][ip][3] = ip_info["subdivisions"]
                        # Add the latitude
                        self.processes[process][3][ip][4][0] = round(list(ip_info["location"])[0], 2)
                        # Add the longitude
                        self.processes[process][3][ip][4][1] = round(list(ip_info["location"])[1], 2)
                    except Exception as e:
                        # There should not be any exceptions here, but
                        # just in case
                        print(e)

import psutil
import ipaddress
from threading import Thread

class ProcessInfo(Thread):

    '''
    This class gathers information about currently
    running processes and their network connections

    Inputs: global dictionary named "processes"
    Processing: Uses psutil library to gather network connection information
    Outputs: Add process network connections to global dictionary
    '''

    def __init__(self, processes):
        # Call the Thread class's init function
        Thread.__init__(self)

        # Add the global dictionary to self
        self.processes = processes


    def run(self):
        # This is a method of the Thread class
        # which is called after Thread.start()

        # Monitor network connections continously
        while(1):
            domains = ""
            countries = ""
            cities = ""
            regions = ""
            orgs = ""

            # Iterate through each network connection and extract information
            for row in psutil.net_connections(kind="all"):
                fd = row[0]  # integer
                family = row[1].name  # AF_INET, AF_INET6, AF_UNIX  // AKA ipv4, ipv6, interprocess communication
                sock_type = row[2].name  # SOCK_STREAM, SOCK_DGRAM, SOCK_SEQPACKET  // AKA TCP, UDP, ? (close to tcp)
                laddr = [row[3].ip, row[3].port]  # local address  // [ip, port]
                try:
                    raddr = [row[4].ip, row[4].port]  # remote address, [ip, port]
                    # Check if remote IP is public or private
                    is_private_ip = ipaddress.ip_address(raddr[0]).is_private
                    # if the remote IP is private, then remove the remote port
                    if(is_private_ip):
                        raddr[1] = ""
                except:
                    raddr = ["", ""]  # no remote address, it must just be listening
                status = row[5] # There is a lot of statuses  // ESTABLISHED, SYN_SENT, CLOSE, etc...
                pid = row[6]  # Process ID

                # Change the family name to something more clear
                if(family == "AF_INET"):
                    family = "IPv4"
                elif(family == "AF_INET6"):
                    family = "IPv6"
                else:
                    family = "IPC"

                # Change the sock_type to something more clear
                if(sock_type == "SOCK_STREAM"):
                    sock_type = "TCP"
                elif(sock_type == "SOCK_DGRAM"):
                    sock_type = "UDP"

                # Try to get process information using the process ID
                try:
                    process = psutil.Process(pid)
                except:
                    process = ""
                try:
                    # The filename of the executable
                    process_filename = process.name()
                except:
                    process_filename = ""
                try:
                    # The filepath of the executable
                    process_filepath = process.exe()
                except:
                    process_filepath = ""
                try:
                    # The command line arguments
                    # On windows, the python script must be run as administrator
                    # cmdline = ['something.exe', '-h']
                    # Convert to a string so it can be added to a set
                    process_cmdline = " ".join(process.cmdline())
                except:
                    process_cmdline = ""
                try:
                    # The user running the process
                    # On windows, the python script must be run as administrator
                    process_username = process.username()
                except:
                    process_username = ""

                # if there's no filepath then ignore it
                if(process_filepath != ""):

                    # is it a new filepath?
                    if(process_filepath not in self.processes.keys()):
                        # Check if there's a remote IP, if there is then add it to the dictionary
                        if(raddr[0] != ""):
                            self.processes[process_filepath] = [process_filename, {laddr[0]},
                                                           {laddr[1]}, {raddr[0]:['', '', '', '', ['', ''], '']}, {raddr[1]}, {family}, {sock_type},
                                                           {process_username}, {process_cmdline}]
                        # If there's no remote IP, then create an empty dict
                        else:
                            self.processes[process_filepath] = [process_filename, {laddr[0]},
                                                           {laddr[1]}, {}, {raddr[1]}, {family}, {sock_type},
                                                           {process_username}, {process_cmdline}]
                    # {'8.8.8.8':[domain, country, continent, subdivisions, location], '1.2.3.4'}
                    #  'country': 'US', 'continent': 'NA',
                    #   'subdivisions': 'CA', 'location': (37.386, -122.0838)
                    #  domain

                    # It is an existing filepath
                    else:
                        if(laddr[0] != ""):
                            self.processes[process_filepath][1].add(laddr[0])
                        if(laddr[1] != "" and len(self.processes[process_filepath][2]) < 15):
                            self.processes[process_filepath][2].add(laddr[1])
                        if(raddr[0] != ""):
                            if(raddr[0] not in self.processes[process_filepath][3].keys()):
                                self.processes[process_filepath][3][raddr[0]] = ['', '', '', '', ['', ''], '']
                        if(raddr[1] != ""):
                            self.processes[process_filepath][4].add(raddr[1])
                        if(family != ""):
                            self.processes[process_filepath][5].add(family)
                        if(sock_type != ""):
                            self.processes[process_filepath][6].add(sock_type)
                        if(process_username != ""):
                            self.processes[process_filepath][7].add(process_username)
                        if(process_cmdline != "" and len(self.processes[process_filepath][8]) < 500):
                            self.processes[process_filepath][8].add(process_cmdline)

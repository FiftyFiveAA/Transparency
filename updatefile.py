import csv
import pickle
import time
from threading import Thread


class UpdateFile(Thread):

    '''
    This class writes the global processes dictionary
    to a file every 5 minutes

    Inputs: global dictionary named "processes"
    Processing: Uses pickle library to serialize dictionary
    Outputs: Writes dictionary to a file named "output.pickle"
    '''

    def __init__(self, processes):
        # Call the Thread class's init function
        Thread.__init__(self)

        # Add the global dictionary to self
        self.processes = processes

        
    def run(self):
        # This is a method of the Thread class
        # which is called after Thread.start()

        # Write global dict "processes" to file
        # every 5 minutes

        counter = 1
        while(1):
            # number of seconds to wait before
            # updating file
            wait_time = 30
            time.sleep(wait_time)
            
            with open("output.pickle", "wb") as f:
                f.write(pickle.dumps(self.processes))

            # create a backup once every 10 saves
            counter += 1
            if(counter % 10 == 0):
                counter = 1
                
                with open("output_backup.pickle", "wb") as f:
                    f.write(pickle.dumps(self.processes))

                # This will contain remote IP's and their lookup information
                table_processes_locations = []

                # This will contain processes and their information
                table_processes_generic = []
                
                for process in self.processes:
                    # iterate through each remote IP address
                    for remote_ip in self.processes[process][3]:
                        # Create the first javascript variable named "processes_data"
                        # This is an array of arrays containing the following information
                        # [[file_path, file_name, remote_ip, domain, country, continent,
                        #       subdivisions,[latitude,longitude], time],[...]]
                        
                        try:
                            table_processes_locations.append([process, self.processes[process][0], remote_ip, self.processes[process][3][remote_ip][0],
                                   self.processes[process][3][remote_ip][1], self.processes[process][3][remote_ip][2],
                                   self.processes[process][3][remote_ip][3], self.processes[process][3][remote_ip][4],
                                   self.processes[process][3][remote_ip][5]])
                        # If the entry doesn't have a remote IP, then ignore it
                        except:
                            pass
                        
                    # Create the second javascript variable named "processes_generic"
                    # This is an array of arrays containing the following information
                    # [[file_path, file_name, local_ips, local_ports, remote_ports, family, socket_types,
                    #       process_username, process_cmdline]],[...]]
                    table_processes_generic.append([process, self.processes[process][0], list(self.processes[process][1]),
                                                    list(self.processes[process][2]),list(self.processes[process][4]),
                                                    list(self.processes[process][5]), list(self.processes[process][6]),
                                                    list(self.processes[process][7]), list(self.processes[process][8])])

                with open("output_locations.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Filepath", "Filename", "Remote IP", "Domain", "Country",
                                     "Continent", "Subdivision", "Location (Lat,Long)", "Time"])
                    writer.writerows(table_processes_locations)

                with open("output_generic.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Filepath", "Filename", "Local IPs", "Local Ports",
                                     "Remote Ports", "Family", "Socket Types", "User",
                                     "Command Line"])
                    writer.writerows(table_processes_generic)
                
                

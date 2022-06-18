import pickle
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from functools import partial

class WebServer(Thread):

    '''
    This class runs the webserver

    Inputs: global dictionary named "processes"
    Processing: writes the "processes" dict to tables.js and handles requests
    Outputs: http://127.0.0.1:12345
    '''

    def __init__(self, processes):
        # Call the Thread class's init function
        Thread.__init__(self)

        # Add the global dictionary to self
        self.processes = processes

    def run(self):
        # This is a method of the Thread class
        # which is called after Thread.start()

        # run the webserver
        while(1):
            handler_class = partial(handler, self.processes)
            with HTTPServer(('localhost', 12345), handler_class) as server:
                server.serve_forever()

# This class handles requests sent to the web server
class handler(BaseHTTPRequestHandler):
    def __init__(self, processes, *args, **kwargs):
        self.processes = processes
        super().__init__(*args, **kwargs)

    # stop the webserver from printing out request information
    # to the command line
    def log_message(self, format, *args):
        return
    
    # If the request is a GET request then follow this logic
    # If it's a POST or anything else, the server responds w/ a 501 error
    def do_GET(self):
        # Send a 200 OK to the browser
        self.send_response(200)
        # Look at the file extension of the requested resource and
        # return the correct content type
        try:
            file_type = self.path.split(".")[-1]
            if(file_type == "js"):
                self.send_header('Content-type','text/javascript; charset=UTF-8')
            elif(file_type == "css"):
                self.send_header('Content-type','text/css')
            elif(file_type == "json"):
                self.send_header('Content-type','application/json')
            elif(file_type == "html"):
                self.send_header('Content-type','text/html; charset=UTF-8')
            elif(file_type == "ico"):
                self.send_header('Content-type','image/x-icon')
        except:
            pass
        self.end_headers()

        # If the request is to the main site
        if(self.path == "/" or self.path == "/index.html"):
            with open("webserver/index.html", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))

        elif(self.path == "/js/tables.js"):
            with open("webserver/js/tables.js") as f:
                html_template = f.read()

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


            python_html = ""
            # Create the first javascript variable named "processes_data"
            python_html += "var processes_data = " + str(table_processes_locations) + ";" + "\n"
            # Create the second javascript variable named "processes_generic"
            python_html += "var processes_generic = " + str(table_processes_generic) + ";" + "\n"

            html = html_template.replace("{{python_replace}}", python_html)
            self.wfile.write(bytes(html, "utf8"))

        # If the request is to an allowed javascript or css resource
        # then load that file and return its contents
        # This is manually intensive but ensures the web server isn't
        # returning unintended local files
        elif(self.path == "/js/main.js"):
            with open("webserver/js/main.js", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))

        elif(self.path == "/js/d3.v3.min.js"):
            with open("webserver/js/d3.v3.min.js", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))

        elif(self.path == "/js/planetaryjs.js"):
            with open("webserver/js/planetaryjs.js", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))

        elif(self.path == "/js/topojson.v1.min.js"):
            with open("webserver/js/topojson.v1.min.js", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))

        elif(self.path == "/css/main.css"):
            with open("webserver/css/main.css", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))

        elif(self.path == "/world-110m-withlakes.json"):
            with open("webserver/json/world-110m-withlakes.json", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))

        elif(self.path == "/world-110m.json"):
            with open("webserver/json/world-110m.json", "r") as f:
                self.wfile.write(bytes(f.read(), "utf8"))

        elif(self.path == "/favicon.ico"):
            with open("webserver/img/favicon.ico", "rb") as f:
                #print(f.read())
                self.wfile.write(f.read())
        # If any other file is requested then return nothing
        else:
            self.wfile.write(bytes("", "utf8"))


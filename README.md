# Transparency

https://user-images.githubusercontent.com/90160593/174447578-61b11fd4-4532-4c51-a25a-b975ff12b429.mp4

### About

This project is intended to provide an easy way to view the connections Windows computers are making over long periods of time. Python is used to gather information about network connections on the local machine. That information is displayed in a web application which contains a spinning/interactive globe with pings representing locations where that device has sent or received data. Additionally, there are tables with more detailed process information including filepaths, ports, and command line arguments.

The application should be able to run 24/7 with minimal filesize overhead.

### Install

#### Download Python

* Download python 3.* and install the required libraries

```
pip3 install ipaddress, python-geoip, python-geoip-geolite2, psutil
```

#### Download the 3 JS libraries

* **If** you want to download the JS libraries so your browser doesn't reach out to a 3rd party site everytime
  - **I've already included the files I used during development. They will become out of date so it's recommended to follow the below instructions.**
  - **Download Planetary JS**. Go to http://planetaryjs.com/download/ and download the Core Library **Unminified** version. Only the unminified version works for me.
  - **Download D3 JS**. I wasn't able to get the more recent versions to work, so download **version 3**. https://d3js.org/d3.v3.min.js
  - Download TopoJSON. https://d3js.org/topojson.v1.min.js
  - Add d3.v3.min.js, planetaryjs.js, topojson.v1.min.js to the **transparency/webserver/js** folder.
  - Go to transparency/webserver/index.html and looks at lines 3-5. This is where the HTML tries to load these 3 libraries. **Ensure that the filenames match**.

* **Else if** you want the JS libraries to be loaded from the 3rd party site everytime
  - Go to transparency/webserver/index.html and edit lines 3-5. Change the src to be the URLs of each JS library.

### Usage

* Run transparency.py

```
python transparency.py
```

* In your browser navigate to **127.0.0.1:12345**. The table next to the globe contains the data populating the pings. Type in the search bar to limit the results (it searches through all columns and rows). If you want to ignore results in a particular country then type in an exclamation mark then the country's ISO code. For example "!us" to show only results from outside the United States.

* There are 2 more tables that contain searchable data. Click the "Ports Table" or "Command Line Table" buttons in the top right of the screen to quickly navigate to those tables.

* **Note**: If you run the script as Administrator then it will return more information for higher privileged processes.

### Misc

##### Design Notes

* **Python**:
  - There are multiple threads that all are reading/writing to a global variable. If you were doing this properly then you should use a thread safe mechanism instead.
  - processinfo.py utilizes the psutil library for gathering socket information, it is queried constantly in a while loop. There is the potential for a socket to be opened and closed in this time period, and thus the code will miss it. During testing I was unable to observe this, but it's theoretically possible.
  - The "database" is just the huge global dictionary that the threads utilize. The "pickle" library is used to serialize the dictionary which is then saved to a file "output.pickle".
  - There are 4 output files. output.pickle is the main database that is looked for when the code starts. output_backup.pickle is a backup that can be renamed to "output.pickle" if the original is corrupted. Output_generic.csv and output_locations.csv and also available for further analysis.

* **Web App**:
  - I used http.server because I wanted as minimal of a web server as possible. I hardcoded the server responses in webserver.py.

##### Software Bill of Materials (SBOM)

###### Python Libraries

* copy, csv, datetime, functools, geoip, http.server, ipaddress, os, pickle, psutil, socket, threading, time

###### JS Libraries

  - **Planetary.js**: http://planetaryjs.com/download/
  - **D3.js**: https://d3js.org/d3.v3.min.js
  - **TopoJSON**: https://d3js.org/topojson.v1.min.js

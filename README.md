# gtfs_work

Contains a .py file developed for analysing GTFS data. This uses the gtfs_functions library to produce sets of HTML files with maps of bus routes contained in the GTFS data.
The .py file will also produce a shape file which can be used with Geographic Information Software (e.g. QGIS) to perform geospatial analysis.
The .py file also calculates the distance of each bus route in the file and produces a CSV file containing this detail.

### NB This python script requires the `gtfs_functions` library to be installed. This can be done using pip installer

.py file is designed to be run from the command line with one argument passed:
* Location of .zip archive of GTFS data from DfT Open Bus Data portal: https://data.bus-data.dft.gov.uk/timetable/download/
* **NB filename passed to .py file should include .zip extension

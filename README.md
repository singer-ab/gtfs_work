# gtfs_work

Contains a .py file developed for analysing GTFS data. This uses the gtfs_functions library to produce sets of HTML files with maps of bus routes contained in the GTFS data.
The .py file will also produce a shape file which can be used with Geographic Information Software (e.g. QGIS) to perform geospatial analysis.
The .py file also calculates the distance of each bus route in the file and produces a CSV file containing this detail.

## Installation requirements
**NB This python script requires the `gtfs_functions` library to be installed. This can be done using pip installer**

## Running the code
.py file is designed to be run from the command line with one argument passed:
* Location of .zip archive of GTFS data from DfT Open Bus Data portal: https://data.bus-data.dft.gov.uk/timetable/download/
* **NB filename passed to .py file should include .zip extension**

## Outputs generated
Outputs from the script include:
* Sub-directory in working directory containing HTML files of route maps for each bus route in the data
* New .zip archive with `_line_freq` suffix containing shape file data for use in GIS
* `route_lengths.csv` containing a summary of the distances travelled associated with each bus route in the GTFS data

## Sample data
A file entitled `itm_wales_gtfs.zip` is included in this repository for use in testing the code.

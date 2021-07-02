# gtfs_work

## Introduction
`gtfs_functions_testing.py` uses the gtfs_functions library to undertake a series of analyses on GTFS data. This has been of interest recently with the UK Department for Transport providing more data on a regular basis at https://data.bus-data.dft.gov.uk/timetable/download/

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

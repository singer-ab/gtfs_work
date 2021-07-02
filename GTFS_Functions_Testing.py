#!/usr/bin/env python
# coding: utf-8

# # GTFS Functions Python Library
# Testing out `gtfs_functions` library for creating shapefiles from GTFS files for bus routes.
# This .py file uses GTFS library to generate route maps for all routes in a GTFS file.
# A csv file is also generated containing the journey length of all unique journeys in the GTFS file
# 
# GTFS data provided on DfT website at: https://data.bus-data.dft.gov.uk/timetable/download/

# When run from command line, requires one argument - full name of folder to be analyzed

# Import libraries used in this script

import zipfile, os, shutil, time, math, sys
import pandas as pd
import gtfs_functions as gtfs
from selenium import webdriver

# Function for checking for presence of direction_id column in trips.txt
def dir_col_check(folder_name=''):
	
    # Check folder name has been provided
    if folder_name == '':
        print('    Please specify a folder name for running the script on. \nThis should be a .zip archive containing GTFS files.')
	
    else:	
        # Make directory for unzipping - deletes directory if it already exists
        folder_name = folder_name
        
        if os.path.isdir(folder_name):
            shutil.rmtree(folder_name)
        os.mkdir(folder_name)
        
        # Unzip archive
        with zipfile.ZipFile(folder_name + '.zip') as zip_ref:
            zip_ref.extractall(folder_name)
        
        edited_archive = False
        		
        # Find trips.txt file in extracted folder and import as dataframe
        if os.path.isfile(os.path.join(folder_name, 'trips.txt')):
            df = pd.read_csv(os.path.join(folder_name, 'trips.txt'))
            if 'direction_id' not in list(df.columns):
                df['direction_id'] = 1
                df.to_csv(os.path.join(folder_name, 'trips.txt'))
                edited_archive = True
            else:
                print('    direction_id already included in trips.txt file.')
        else:
            print('    trips.txt not included in GTFS file set.')
        		
        # Remove existing zip directory ready for zipping up edited GTFS file set
        os.remove(folder_name + '.zip')
        
        # Create function for zipping directory
        shutil.make_archive(folder_name, 'zip', folder_name)
        if edited_archive:
            print('    Archive updated.')
        
        # Remove extracted directory
        shutil.rmtree(folder_name)

# Function for checking stop times for invalid times
def stop_time_check(folder_name=''):
    
    # Check folder name has been provided
    if folder_name == '':
        print('    Please specify a folder name for running the script on. \nThis should be a .zip archive containing GTFS files.')
	
    else:	
        
        # Unzip archive
        if os.path.isdir(folder_name):
            shutil.rmtree(folder_name)
        os.mkdir(folder_name)
        
        with zipfile.ZipFile(folder_name + '.zip') as zip_ref:
            zip_ref.extractall(folder_name)
                
        # Read stop_times file
        stop_times = pd.read_csv(os.path.join(folder_name, 'stop_times.txt'))
        
        # Count number of affected rows
        aff = stop_times.loc[stop_times.arrival_time>='24:00:00'].shape[0]
        tot = stop_times.shape[0]
        
        print(f'    There are {aff} rows with invalid stop times out of {tot}.')
        print('    These will now be edited.')
        
        
        # Edit invalid stop times
        stop_times['arr'] = stop_times.apply(lambda x: '0' + str(int(x['arrival_time'][:2]) - 24) + x['arrival_time'][2:]
                                             if int(x['arrival_time'][:2]) >= 24 else
                                             x['arrival_time'], axis=1)
        stop_times['dep'] = stop_times.apply(lambda x: '0' + str(int(x['departure_time'][:2]) - 24) + x['departure_time'][2:]
                                             if int(x['departure_time'][:2]) >= 24 else
                                             x['departure_time'], axis=1)
        
        # Edit column names and order
        cols = list(stop_times.columns)
        stop_times = stop_times.drop(['arrival_time', 'departure_time'], axis=1)
        counter = 0
        
        for col in cols:
            if col=='arrival_time':
                cols[counter] = 'arr'
            if col=='departure_time':
                cols[counter] = 'dep'
            counter += 1
        
        cols = cols[:-2]
        stop_times = stop_times[cols]
        
        counter = 0
        for col in cols:
            if col=='arr':
                cols[counter] = 'arrival_time'
            if col=='dep':
                cols[counter] = 'departure_time'
            counter += 1
        
        stop_times.columns = cols
        
        # Export txt file and rezip directory
        stop_times.to_csv(os.path.join(folder_name, 'stop_times.txt'))
        os.remove(folder_name + '.zip')
        shutil.make_archive(folder_name, 'zip', folder_name)
        shutil.rmtree(folder_name)
        print('    Edited stop_times file to remove invalid timings.')

# Function for importing GTFS .txt files and setting up gtfs_functions library
def gtfs_import(folder_name=''):

    # Check folder name has been provided
    if folder_name == '':
        print('    Please specify a folder name for running the script on. \nThis should be a .zip archive containing GTFS files.')
    
    else:
        folder_name = folder_name        
        start_time = time.perf_counter()
        routes, stops, stop_times, trips, shapes = gtfs.import_gtfs(folder_name + '.zip')
        total_time = time.perf_counter() - start_time
        mins = math.floor(total_time / 60)
        secs = total_time % 60
        print(f'    {folder_name} GTFS files imported in {mins} minutes and {round(secs, 0)} seconds.')
        return routes, stops, stop_times, trips, shapes

# Function for creating an HTML route map for all routes in the GTFS file
def route_maps(line_freq=None):

    # Check line frequency dataframe has been passed    
    if line_freq is None:
        print('    Line frequency dataframe has not been passed.\nThis will cause the script to crash.')

    else:
        # Make output file path
        run_function = True
        if os.path.isdir('route_maps'):
            resp = input('    Route Maps directory already exists. Continuing to run will overwrite files.\n    Continue? [y/n] ')
            if resp == 'n':
                run_function = False
        
        if run_function:
            if not os.path.isdir('route_maps'):
                os.mkdir('route_maps')
            
            # Loop through routes in the line_freq data frame and export a map for each    
            for route in line_freq['route_name'].unique():
                gdf = line_freq.loc[line_freq.route_name==route,:].reset_index()
                gdf = gdf.head(1)
                route_map = gtfs.map_gdf(gdf = gdf,
                            variable = 'ntrips',
                            colors = ['#d13870', '#e895b3', '#55d992', '#3ab071', '#0e8955', '#066a40'],
                            tooltip_var = ['route_name', 'frequency'],
                            tooltip_labels = ['Route #: ', 'Frequency (mins): '],
                            breaks = [5, 10, 20, 50])
                
                delay = 5
                fn=f'route_maps/route_{route}.html'
                tmpurl=f'file://{os.getcwd()}/route_maps/{fn}'
                route_map.save(fn)
            print('    Created route maps.')
        else:
            print('    Existing route maps not overwritten.')

# Function for exporting a shape file containing all routes in the GTFS file
def export_shape_file(line_freq=None, folder_name=''):
    
    # Check line frequency dataframe has been passed
    if line_freq is None:
        print('    Line frequency dataframe has not been passed.\n    This will cause the script to crash.')
    elif folder_name == '':
        print('    Folder name has not been speicified for shape file export.')
    else:
        run_function = True
        if os.path.isfile(folder_name + '_line_freq.zip'):
            resp = input('    Shape file output file name already exists. \n    Delete existing file? [y/n] ')
            if resp != 'y':
                run_function = False
        if run_function:
            gtfs.save_gdf(line_freq, folder_name + '_line_freq', geojson=False, shapefile=True)
            print('    Shape file generated.')
        else:
            print('    Shapefile not overwritten.')

# Function for calculating all route lengths and exporting a CSV containing them all.
def calculate_lengths(line_freq=None):

    run_function = True
    
    # Check if route_lengths file already exists
    if os.path.isfile('route_lengths.csv'):
        resp = input('    route_lengths.csv file already exists. \n    Delete existing file? [y/n] ')
        if resp == 'n':
            run_function = False
        else:
            try:
                os.remove('route_lengths.csv')
            except:
                print('    Cannot delete route_legnths.csv\n    Check if file is open.')
                sys.exit()
    
    if run_function:
                
        # Update CRS of geodataframe to GB National Grid
        line_freq = line_freq.set_crs(epsg=4326)
        line_freq = line_freq.to_crs(epsg=27700)
        
        # Create dataframe for storing unique route_id's and lengths
        cols = ['route_id', 'route_name', 'distance_(km)']
        distances = pd.DataFrame(columns=cols)
        
        # loop through lines in line_freq dataframe and get length of each
        for line in list(line_freq.route_id.unique()):
            temp_df = line_freq.loc[line_freq.route_id==line].head(1)
            name = temp_df.iloc[0]['route_name']
            km = temp_df.iloc[0]['geometry'].length / 1000
            new_line = {
                'route_id' : line,
                'route_name' : name,
                'distance_(km)' : km}
            distances = distances.append(new_line, ignore_index=True)
        
        # export CSV of distances
        distances['distance_(miles)'] = distances['distance_(km)'] * 0.621371
        distances = distances.sort_values(['route_name'])
        distances = distances.reset_index()
        distances.to_csv('route_lengths.csv')
        print('    CSV file generated.')
    else:
        print('    CSV file not generated.')

def main():
    
    # Set folder name and set up files for process
    folder_name = sys.argv[1]
    
    print('\n')
    print('Checking for direction_id column in trips.txt file.')
    dir_col_check(folder_name)
    print('\n')
    
    print('Updating stop_times file to remove invalid timings.')
    stop_time_check(folder_name)
    print('\n')
    
    print('Importing GTFS file.')
    routes, stops, stop_times, trips, shapes = gtfs_import(folder_name)
    print('\n')
    
    # Create line_freq dataframe using gtfs
    print('Creating line frequencies dataframe.')
    cutoffs = range(0, 23)
    line_freq = gtfs.lines_freq(stop_times, trips, shapes, routes, cutoffs=cutoffs)
    print('    Dataframe created.')
    print('\n')
    
    # Export route maps
    print('Generating route maps.')
    route_maps(line_freq)
    print('\n')
    
    # Export shape file
    print('Exporting shape file.')
    export_shape_file(line_freq, folder_name)
    print('\n')
    
    # Calculate route lengths and generate CSV
    print('Creating CSV of route lengths.')
    calculate_lengths(line_freq)  
    print('\n')
    print('Process complete!')

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
'''
Use Plotty to graph data in csv file from Aranet4 device
'''


__author__ = "Ian Robertson"
__version__ = "0.9.0"
__license__ = "GNU Affero General Public License v3.0"



import argparse
import datetime
import os
import os.path
import sys
import click
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates

def main(args):
    """ Main entry point of the app """
    infile = sys.argv[1]
    outdir = os.path.splitext(sys.argv[1])[0]

    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    used_locations = []
    sensor_csv_data = pd.read_csv(
        infile, index_col='Time', parse_dates=True, dayfirst=True)

    read_dt = sensor_csv_data.index

    reading_dates = read_dt.map(lambda t: t.date()).unique()

    for reading_date in reading_dates:

        dayname = reading_date.strftime("%a")
        # skip sat / sun unless told otherwise
        if dayname in ('Sat', 'Sun') and args.allweek is False:
            continue
        click.clear()
        print(os.path.basename(__file__))
        humandate = reading_date.strftime("%a %d %B %Y")
        print('Do you wish readings from: [' +
              sys.argv[1]+']  for  ['+humandate+']')

        if confirm_use_date(humandate) is False:
            continue
        if len(used_locations) != 0:
            used_str = [str(i) for i in used_locations]
            used = " ".join(used_str)
            print("Locations already used ["+used+"]")

        location = get_location(humandate)
        used_locations.append(location)

        reading_start = reading_date
        reading_end = reading_date+datetime.timedelta(days=1)

        reading_start = pd.to_datetime(reading_start)
        reading_end = pd.to_datetime(reading_end)

        reading_start_idx = sensor_csv_data.index.searchsorted(reading_start)
        reading_end_idx = sensor_csv_data.index.searchsorted(reading_end)

        todays = sensor_csv_data.iloc[reading_start_idx:reading_end_idx]

        working_hours = todays.between_time(args.start_time, args.end_time)
        
        working_hours.plot( y=args.graphtype ) 

        date_format = mpl_dates.DateFormatter('%H:%m')
        #fig, ax = plt.subplots()
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.margins(0)
        plt.title(str(reading_date)+' '+location, loc='left')


        
        if args.graphtype == 'CO₂(ppm)':

            try:
                maxc02 = working_hours['CO₂(ppm)'].max()
                co2limit = int(maxc02+0.1*maxc02)
            except:
                co2limit = 2000

            if co2limit < 1500:
                co2limit = 2000

            plt.axhspan(0, 800, facecolor='green', alpha=0.5)
            plt.axhspan(800, 1500, facecolor='yellow', alpha=0.5)
            plt.axhspan(1500, co2limit, facecolor='red', alpha=0.5)
       
        plt.savefig(outdir+'/'+
                    location+'-'+
                    args.graphtype+'-' +
                    str(reading_date)+
                    '.'+args.imgformat)


    click.clear()
    print(os.path.basename(__file__))
    if len(used_locations) != 0:
        used_str = [str(i) for i in used_locations]
        used = " ".join(used_str)
        print("Created graphs for ["+used+"]\n\tThese can be found in [" +
              outdir+"] in directory containg the CSV file")


def confirm_use_date(rundate):
    '''Confirm we want to process a date'''
    reply = str(
        input('\tConfirm wish to use readings on ['+rundate+'] (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False

    return confirm_use_date( rundate)


def confirm_location(llocation, rundate):
    '''Verify a  location for a rundate'''

    if args.nocheck is True:

        reply = str(input(
            '\tConfirm Location ['+
            llocation+'] for readings on ['+rundate+
            '] (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

        return confirm_location("Uhhhh... please enter ", rundate)

    return True


def get_location(rundate):

    ''' Get location of data recording for a rundate'''
    while True:
        location = input(
            "Please enter location for readings on ["+rundate+"]: ")
        if len(location) >= 3 and confirm_location(location, rundate):
            return location

# main
if __name__ == "__main__":

    parser = argparse.ArgumentParser( 
        description='\na script to plot CSV data from an Aranet4 device')
    parser.add_argument('csv_data_file', type=argparse.FileType('r'),
                        help='Name of file containing aranet4 csv data')
    parser.add_argument('--nocheck', nargs='?', const=True, default=False,
                        help='If [--nocheck] set locations will not be confirmed')

    parser.add_argument('--allweek', nargs='?', const=True, default=False,
                        help='[--allweek] offer weekend readings')

    parser.add_argument('--imgformat', nargs='?', const='png', default='png',
                        choices=['png', 'jpg', 'webp', 'svg', 'pdf'],
                        help='Choose output format, default png')
    parser.add_argument('--graphtype', nargs='?', const='CO₂(ppm)', default='CO₂(ppm)',
                        choices=['CO₂(ppm)', 'Temperature(C)',
                                 'Humidity(%)', 'Pressure(hPa)'],
                        help='Set data graphed')
    parser.add_argument('--start_time', nargs='?', const='08:00', default='08:00',
                        help='Start time hh:mm - default [08:00]')
    parser.add_argument('--end_time', nargs='?', const='17:00', default='17:00',
                        help='Start time hh:mm - default [17:00]')
    args = parser.parse_args()
    
    main(args)
    sys.exit(0)





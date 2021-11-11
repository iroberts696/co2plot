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
import plotly.express as px

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
            USED = " ".join(used_str)
            print("Locations already used ["+USED+"]")

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

        figure = px.line(working_hours,
                         y=args.graphtype,
                         title='Room: ['+location+'] '+args.graphtype +
                         '/Time on '+str(reading_date)+' ( from '+infile+')',
                         ).update_traces(line_color='darkblue')

        figure.update_layout(xaxis_title="Time",  xaxis_tickformat='%H:%M')

        if args.graphtype == 'CO₂(ppm)':

            try:
                maxc02 = working_hours['CO₂(ppm)'].max()
                CO2LIMIT = int(maxc02+0.1*maxc02)
            except:
                CO2LIMIT = 2000

            if CO2LIMIT < 1500:
                CO2LIMIT = 2000

            figure.add_hrect(
                xref="paper", y0=1500, y1=CO2LIMIT, yref="y",
                fillcolor="red", opacity=0.25,
                layer="below", line_width=0,
            )
            figure.add_hrect(
                xref="paper", y0=750, y1=1500, yref="y",
                fillcolor="Yellow", opacity=0.25,
                layer="below", line_width=0,
            )

            figure.add_hrect(
                xref="paper", y0=0, y1=750, yref="y",
                fillcolor="Green", opacity=0.25,
                layer="below", line_width=0,
            )

        figure.write_image(outdir+'/'+
                           location+'-'+
                           args.graphtype+'-' +
                           str(reading_date)+
                           '.'+args.imgformat)

    click.clear()
    print(os.path.basename(__file__))
    if len(used_locations) != 0:
        used_str = [str(i) for i in used_locations]
        USED = " ".join(used_str)
        print("Created graphs for ["+USED+"]\n\tThese can be found in [" +
              outdir+"] in directory containg the CSV file")


def confirm_use_date(rundate):
    '''Confirm we want to process a date'''
    reply = str(
        input('\tConfirm wish to use readings on ['+rundate+'] (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False

    return confirm_use_date("Uhhhh... please enter ", rundate)


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
        llocation = input(
            "Please enter location for readings on ["+rundate+"]: ")
        if len(llocation) >= 3 and confirm_location(llocation, rundate):
            return llocation

# main
if __name__ == "__main__":
    """ This is executed when run from the command line """

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=argparse.FileType('r'))
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




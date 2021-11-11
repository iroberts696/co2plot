# co2plot
script to plot csv data derived from an Aranet4 CO2 sensor / logger

usage: co2plot.py [-h] [--nocheck [NOCHECK]] [--allweek [ALLWEEK]] [--imgformat [{png,jpg,webp,svg,pdf}]]
                  [--graphtype [{CO₂ppm),Temperature(C),Humidity(%),Pressure(hPa}]] [--start_time [START_TIME]] [--end_time [END_TIME]]
                  csv_data_file

a script to plot CSV data from an Aranet4 device

positional arguments:
  csv_data_file         Name of file containing aranet4 csv data

optional arguments:
  -h, --help            show this help message and exit
  --nocheck [NOCHECK]   If [--nocheck] set locations will not be confirmed
  --allweek [ALLWEEK]   [--allweek] offer weekend readings
  --imgformat [{png,jpg,webp,svg,pdf}]
                        Choose output format, default png
  --graphtype [{CO₂(ppm),Temperature(C),Humidity(%),Pressure(hPa)}]
                        Set data graphed
  --start_time [START_TIME]
                        Start time hh:mm - default [08:00]
  --end_time [END_TIME]
                        Start time hh:mm - default [17:00]


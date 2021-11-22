# co2plot

python3 script to plot csv data derived from an Aranet4 CO2 sensor / logger



## command and options

usage: co2plot.py [-h] 
                  [--nocheck [True|False] default True dont confirm location names
                  [--allweek [True|False] default False - ignore weekend readings
                  [--imgformat [{png,jpg,webp,svg,pdf}]]
                  [--graphtype [{CO₂ppm),Temperature(C),Humidity(%),Pressure(hPa}]] 
                  [--start_time [START_TIME]] default 08:00
                  [--end_time [END_TIME]]  default 17:00
                  csv_data_file

a script to plot CSV data from an Aranet4 device

Script developed prmarily to plot readings from CO2 sensor in png fromat and

co2plot CSV-file-name

will produce a directory named after the CSV file containg png plots of CO2

## Windows Users

There is an exe in the dist folder produced vy pyinstaller and allows plotting without installation of python 

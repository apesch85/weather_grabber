#! /usr/bin/python3

from datetime import datetime
from io import BytesIO
import os
import gspread
import pycurl

# Store the thing in an environment variable for security.
service_account = os.getenv('robo_location')


def GetStats():
    """ Get weather stats from NOAA.

    Parse the response into individual stats, and return a list.

    Returns:
        stats_list: A list containing values for temperature, wind speed, and atmospheric pressure.
    """

    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, "ftp://tgftp.nws.noaa.gov/data/observations/metar/decoded/KGRR.TXT")
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform()
    crl.close()

    # Split the string into a list, and figure out where the stats we care about are located and pull
    # only those stats out.
    get_body = b_obj.getvalue().decode('utf-8').split()

    temperature = get_body[get_body.index('Temperature:') + 1]
    wind_list = get_body[get_body.index('Wind:') + 1: get_body.index('MPH') + 1]
    wind = [detail for detail in wind_list if not detail.startswith('(') and not detail.endswith(')')]
    wind_string = ' '.join(wind)
    pressure = get_body[get_body.index('Hg') + 1][1:]

    stats_list = [temperature, wind_string, pressure]

    return stats_list


def WriteSheet(stats):
    """ Writes weather stats to Google Sheet.
    
    Establishes connection and authenticates to the Google Sheet, finds the next empty row, and 
    writes weather stats to it.
    
    Args:
        stats: A list containing values for temperature, wind speed, and atmospheric pressure.
    """
    
    count = 1
    populated_cell = True
    today_date = datetime.now().strftime("%m-%d-%Y")
    today_time = datetime.now().strftime("%H:%M:%S")
    
    gc = gspread.service_account(filename=service_account)
    sheet = gc.open('Jackson Weather Tracker')
    worksheet = sheet.worksheet('Weather')
    
    # Find the next empty row.
    while populated_cell == True:
        count += 1
        populated_cell =  bool(worksheet.acell('A%s' % count).value)

    # Update the spreadsheet.
    worksheet.update('A%s' % count, today_date)
    worksheet.update('B%s' % count, today_time)
    worksheet.update('C%s' % count, stats[0])
    worksheet.update('D%s' % count, stats[1])
    worksheet.update('E%s' % count, stats[2])

def main():
    weather_stats = GetStats()
    WriteSheet(weather_stats)
  
if __name__ == '__main__':
    main()
  
  

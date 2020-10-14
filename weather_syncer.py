#! /usr/bin/python3

from datetime import datetime
from io import BytesIO
import os
import gspread
import pycurl

service_account = os.getenv('robo_location')


def GetStats()
    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL,
               "ftp://tgftp.nws.noaa.gov/data/observations/metar/decoded/KDTW.TXT")
    crl.setopt(crl.WRITEDATA,
               b_obj)
    crl.perform()
    crl.close()

    get_body = b_obj.getvalue().decode('utf-8').split()

    temperature = get_body[get_body.index('Temperature:') + 1]
    wind_list = get_body[get_body.index('Wind:') + 1: get_body.index('MPH') + 1]
    wind = [detail for detail in wind_list if not detail.startswith('(') and not detail.endswith(')')]
    pressure = get_body[get_body.index('Hg') + 1][1:]

    stats_list = [temperature, wind, pressure]

    return stats_list


def WriteSheet(stats):
  gc = gspread.service_account(filename=service_account)
  sheet = gc.open('Jackson Weather Tracker')
  worksheet = sheet.worksheet('Weather')
  val = worksheet.acell('A1').value
  print(val)


def main():
  weather_stats = GetStats()
  WriteSheet(weather_stats)
  
if __name__ == '__main__':
  main()
  
  

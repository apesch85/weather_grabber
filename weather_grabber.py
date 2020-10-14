#!/usr/bin/python3

"""
"""

import re
import os

def getwx():
  # access wttr.in with custom formatting and temporarily dump it into /tmp/wx.txt
  wxstr = os.system('curl -s ftp://tgftp.nws.noaa.gov/data/observations/metar/decoded/KDTW.TXT > /tmp/wx.txt')

  outstr = ''

  # grab the info out of our temp file...
  with open("/tmp/wx.txt","r") as wxish:
    wxlst = [''] * 9
    for line in wxish:
      if line != '':
        line = line.rstrip()
        line = line.lstrip()
        if 'United' in line:
          pass
        elif 'ob:' in line:
          pass
        elif 'cycle:' in line:
          pass
        elif 'UTC' in line:
          timeval = re.search('([A-Za-z]{1,3}) (\d\d), (\d{1,4}) - (\d\d:\d\d [A-P]M [A-Z]{1,2}T)',line)
          month = timeval.group(1)
          date = timeval.group(2)
          year = timeval.group(3)
          time = timeval.group(4)
        elif 'Wind' in line:
          if 'from the' in line:
            windval = re.search('(?:Wind: from the )([A-Z]{1,3})(?: \(\d{1,3} degrees\) at )(\d{1,3})(?:.*$)',line)
            winddir = windval.group(1)
            windspeed = windval.group(2)
          elif 'alm:' in line:
            winddir = 'calm/'  # This is to accomodate "Wind: Calm:0" corner case
            windspeed = '0'
        elif 'Visibility' in line:
          vizval = re.search('(?:Visibility: )(\d{1,3})',line)
          viz = vizval.group(1)
        elif 'conditions' in line:
          condxval = re.search('(?:Sky conditions: )(?=)(.*)(?=$)',line)
          condx = condxval.group(1)
        elif 'Temperature' in line:
          tempval = re.search('(?:Temperature: )(\d{1,3}\.?\d?)( F)(?:.*$)',line)
          temp = tempval.group(1)
        elif 'Dew Point' in line:
          dewval = re.search('(?:Dew Point: )(\d\d\.?\d?)(?:.*$)',line)
          dew = dewval.group(1)
        elif 'Relative Humidity' in line:
          humval = re.search('(?:Relative Humidity: )(\d{1,2})(?:.*$)',line)
          relhum = humval.group(1)
        elif 'Pressure (altimeter)' in line:
          airpresval = re.search('(?:Pressure \(altimeter\): )(\d{1,2}\.?\d{1,2}?)(?:.*$)',line)
          airpres = airpresval.group(1)
        else:
          pass

  wxish.close()
  outstr = year+'.'+month+'.'+date+'_'+time+','+temp+'F,'+relhum+'%,'+airpres+'in/Hg,'+viz+'Mi,Wind:'+winddir+'@'+windspeed+','+condx+',dewpnt:'+dew+'\n'
  return outstr


def main():
  wx = getwx()

  myhomedir = os.getenv("HOME") # find out the user's home directory
  os.chdir(myhomedir) # change to that directory

# append information string to ~/wx.log file
  
  with open("wx.log","a") as logish:
    logish.write(wx)
  logish.close()

if __name__ == '__main__':
  main()

def randomcrap():
  myhomedir = os.getenv("HOME")
  # change to user's home dir
  os.chdir(myhomedir)

###############################################################################################
# DiDmap
# Made by  -  InfiniteFor
#
# 
# Version: 0.1
# Date:    07-08-2016
#
# Version: 0.2
# Date:    20-09-2016
#
# This tool downloads all files from a webpage which uses the aps.net file download (".asp?id="). 
################################################################################################

import urllib2
import cgi
import datetime
import signal
import re
import sys
import os

# exit DiDmap when ctrl+c is pressed
def signal_handler(signal, frame):
        print("\n-------- DiDmap: Process aborted by user --------\n")
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

count = 1
stopcnt = 1
killcnt = 250
#startURL = sys.argv[1]
startURL = raw_input("Enter URL : ")
now = datetime.datetime.now()

# add "http://" if it isn't present in startURL
if startURL[:4]!="http":
    startURL = "http://" + startURL

# regex for domainname to use as pathname
pat = r'((https?):\/\/)?(\w+\.)*(?P<domain>\w+)\.(\w+)(\/.*)?'
m = re.match(pat, startURL)
path =m.group('domain')

if not os.path.exists(path):
    os.makedirs(str(path))

print "-------- " + now.strftime("%Y-%m-%d %H:%M") + "  Starting DiDMap on " + startURL + " --------\n"

while (count > -1):
    url = startURL + str(count)
    u = urllib2.urlopen(url)
    _,params = cgi.parse_header(u.headers.get('Content-Disposition',''))

    if not params:
        # if params is empty current id contains no file
        print "[-] id " + str(count) + ":  contains no file"
        stopcnt = stopcnt + 1
        count = count +1
        if stopcnt > killcnt:
            print "Reached 250 empty ID's"
            break
    

    else:
        # downloading the file and showing the status
        stopcnt = 1
        file_name = path+"/id_" + str(count) + ":" + params['filename']
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "[+] id " + str(count) + ":  Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            d_buffer = u.read(block_sz)
            if not d_buffer:
                break

            file_size_dl += len(d_buffer)
            f.write(d_buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()
        count = count + 1

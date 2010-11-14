#!/usr/bin/env python
"""
Copyright (c) 2010, Jonathan Beluch 
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Jonathan Beluch nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import json
import time
from xml.dom.minidom import parse
from urllib import urlopen

"""google latitude badge url, you must enable the public badge in latitude settings
a sample URL is below without a userid"""
GOOGLE_URL = 'http://www.google.com/latitude/apps/badge/api?user=<USERID>&type=json'
LOG_NAME = '/path/to/location/log'
#url for reverse address lookup from latitude and longitude
FS_GEOCODE = 'http://ws.geonames.org/findNearestAddress?lat=%s&lng=%s'

def get_text(node):
    """Returns all of the children text nodes concatenated together"""
    return ''.join(node.data for node in node.childNodes if node.nodeType == node.TEXT_NODE)

def get_address_from_coords(lng, lat):
    """Looks up and returns and address string from a given latitude and longitude
    coordinate pair"""
    #download address xml and parse
    dom = parse(urlopen(FS_GEOCODE % (lat, lng)))

    #these are the names of the tags to extract
    #order of this list is important for the output string
    taglist = ['streetNumber', 'street', 'placename', 'adminCode1', 'postalcode']
    
    #getElementsByTagName returns a node list so get the first instance for each tagname
    nodes = map(lambda t: dom.getElementsByTagName(t)[0], taglist)
    addr = map(get_text, nodes)
    return '{2} {3}, {4}, {5} {6} [{0}, {1}]'.format(lat, lng, *addr)

def log_location(address):
    """Takes an address string and logs to LOG_NAME with the current date and time"""
    with open(LOG_NAME, 'a') as f:
        f.write(time.strftime('[%H:%M] %m/%d/%y: ') + address + '\n')

def main():
    #download current location from google latitude
    location = json.load(urlopen(GOOGLE_URL))
    lng, lat = location['features'][0]['geometry']['coordinates']
    address = get_address_from_coords(lng, lat)
    log_location(address) 

if __name__ == '__main__':
    main()

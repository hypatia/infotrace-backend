#!/usr/bin/python
### collect all the requests from the infotrace server, and process them


import mechanize
import os
import sys
import popen2
import re

allowed_types = ['monthly', 'weekly', 'daily', 'hourly']

request_type = os.environ.get("SSH_ORIGINAL_COMMAND")

if request_type in allowed_types:
    #set BASE_URL appropriately here?
    print "timed requests"
elif re.match('instant', request_type):
    #will need additional parameters for the instant requests, unsure how to proceed
    print "instant request"
else:
    print "OMG HAX"

BASE_URL = "http://infotrace.citizenlab.org/requests.txt"
br = mechanize.Browser()
data = br.open(BASE_URL).get_data()

for line in data.split("\n"):
    if line == "": pass
    elif line[0] =="#": pass
    else:
        (id,owner_id,name,type,node,destination) = line.split(",")
        proc = popen2.Popen3("ssh utoronto_infotrace@" + node + " sudo " + type + " " + destination)
        fromchild = proc.fromchild.readline()
        sys.stdout.write(fromchild)
        while fromchild:
            fromchild = proc.fromchild.readline()
            sys.stdout.write(fromchild) 
        print fromchild

#!/usr/bin/env bash

# Script the content of tweets inside 'arr' array

arr=("1575576254480207872.xml"
     "1577654135180124161.xml"
     "1577574914558775302.xml"
     "1576690411082780672.xml"
     "1576533010371219456.xml"
     "1457091474575794183.xml"
     "1562825718819868674.xml"
     "1574949079141912576.xml"
     "1515678524870438916.xml"
     "1577930810979762176.xml"
     "1577406067646074956.xml"
     "1564898677616934914.xml")

for i in ${arr[@]};
do
    python3 print_xml.py ../dataset/20221006121322/pilot_two/ | egrep '$i'
done

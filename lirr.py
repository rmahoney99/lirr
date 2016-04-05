import csv
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from collections import defaultdict


#TODO
#Get the route numbers for each route using routes.txt
#hardcode to Babylon for now
route_id="1"

#TODO
#Get the stop_ids from stops.txt

# get the valid service ids for today's date from calendar_dates.txt
def getDates():
        dates = csv.reader(open('calendar_dates.txt'))
        svc_ids=[]

        for row in dates:
           if row[1]==today:
                svc_ids.append(row[0])

        global service_ids
        service_ids=[]
        service_ids=dict.fromkeys(svc_ids)



#get the trip ids from trips.txt for the requested destination
def getTrips(destination):
        trip_ids={}
        trip_lst=[]
        trips = csv.reader(open('trips.txt'))
        for row in trips:
           if row[1] in service_ids:
             if row[3]==destination and row[5]=='1':
               trip_ids[row[2]]=row[3]
        return(trip_ids)       
   
#get the stop_times from stop_times.txt
def getStopTimes():
   global stops_lst
   stops = csv.reader(open('stop_times.txt'))
   stops_lst=[]

   for row in stops:
     stops_lst.append(row)
   return

def getTrains(trips,origin_stop_id):
        
        times_dct={}
        for row in stops_lst:
           if row[0] in trips and ( row[3]==origin_stop_id):
              arrival_dtm=getDatetime(row[1])
              depart_dtm=getDatetime(row[2])
              if depart_dtm > curr_time:
                times_dct[row[0]]=[depart_dtm,arrival_dtm]
        return(times_dct)
        
def getDatetime(time):
  offset=0
  hr=time[0:2]
  rest=time[2:8]
  if hr=="24" or hr=="25":
     hr="23"
     if hr=="24":
       offset=1
     if hr=="25":
       offset=2
     time=hr+rest
  return(datetime.strptime(today+time,"%Y%m%d%H:%M:%S")+timedelta(hours=offset))
   
def showTimes(times):

   times_list=[]
   times_list=times.values();
   times_list.sort()
   for row in times_list:
      print "arrival time "+row[0].strftime("%I %M") + " departure time "+row[1].strftime("%I %M")

   return 

def getEndStops(origin):
#        endStops={}
        endStops=defaultdict(list)
        trips = csv.reader(open('trips.txt'))
        for row in trips:
           if row[1] in service_ids:
              if row[5]=='1' and row[3] != origin:  #make sure the direction is westbound and the headsign is not the origin 
                 endStops[row[3]].append(row[2])  # for each endStop add a tuple of the trip ids
#                endStops[row[3]]=1
        return(endStops)      



today=date.today().strftime("%Y%m%d")
curr_time=datetime.now()
origin='Babylon'   
origin_stop_id='118' #Babylon
dest_station='Penn Station'
#dest_station='Atlantic Terminal'

getDates()
getStopTimes()
endStops=getEndStops(origin)
#for each of the endStops, get a list of trips
all_trips={}
for row in endStops:
   trips=getTrips(row)
   all_trips.update(trips)

#get all trips that stop at your origin
direct={}
times_dct=getTrains(all_trips,origin_stop_id)
for key in times_dct:
   if all_trips[key]==dest_station:
      direct[key]=times_dct[key]
showTimes(direct)      
#get connectors   
connector={}
for key in times_dct:
   if all_trips[key]!=dest_station:
      connector[key]=times_dct[key]
showTimes(connector)      
print endStops




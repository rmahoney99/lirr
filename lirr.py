import csv
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from collections import defaultdict


#TODO
#Get the route numbers for each route using routes.txt


#Get the stop_ids from stops.txt
def getStops():
    stops = csv.reader(open('stops.txt'))
    next(stops, None) #skip header
    stop_names={}
    stop_ids={}
    for row in stops:
      stop_names[row[1]]=row[0]
      stop_ids[row[0]]=row[1]
    return stop_names,stop_ids


# get the valid service ids for today's date from calendar_dates.txt
def getDates():
        dates = csv.reader(open('calendar_dates.txt'))
        next(dates, None) #skip header
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
        routes={}
        trip_lst=[]
        trips = csv.reader(open('trips.txt'))
        next(trips, None) #skip header
        for row in trips:
           if row[1] in service_ids:
             if row[3]==destination and row[5]=='1':
               trip_ids[row[2]]=row[3]
        return(trip_ids)       

   
#get the stop_times from stop_times.txt
def getStopTimes():
   global stops_lst
   stops = csv.reader(open('stop_times.txt'))
   next(stops, None) #skip header
   stops_lst=[]

   for row in stops:
     stops_lst.append(row)
   return

# get all trips for the requested station
def getTrains(trips,origin_stop_id):
        
        times_dct={}
        for row in stops_lst:
           if row[0] in trips and ( row[3]==origin_stop_id):
              arrival_dtm=getDatetime(row[1])
              depart_dtm=getDatetime(row[2])
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

        endStops=defaultdict(list)
        connectors=defaultdict(list)
        trips = csv.reader(open('trips.txt'))
        next(trips, None) #skip header
        for row in trips:
           if row[1] in service_ids:    # trip is valid today
              if row[5]=='1':          #make sure the direction is westbound  
                 endStops[row[3]].append(row[2])  # for each endStop add a tuple of the trip ids
              if row[3] not in connectors[row[0]]:  # for each route, create a unique list of headsigns
                 connectors[row[0]].append(row[3])  #which we will call connectors
        return endStops,connectors
        
#trips.txt - contains the route, service_id (relates to day_, trip id, trip headsign (final destination) and direction (1 for westbound)        
#stops.txt - contains the stop_id and stop_name
#stop_times.txt - trip id arrival time departure time stop id and stop sequence
#
# stop_names - dict - from stops.txt key is stop name, value is stop id
# stop_ids - dict - from stops.txt key is stop_id, value is stop_name
# stops_list - global list - from stop_times.txt All stop times values are the trip_id, arrival_time,departure_time,stop_id, stop_sequence
# end_stops - dict - from trips.txt key is headsign value is a list of trips for that headsign
# connectors - dict - from trips.txt key is route id, value is the unique list of headsigns for that route
#times_dct - dict - all trips that stop at the origin - key is trip_id, values are arrival time and depart time 
#direct  - dict - from times_dict where the key is the destination station

today=date.today().strftime("%Y%m%d")
curr_time=datetime.now()
origin='Babylon'   
dest_station='Penn Station'
#dest_station='Atlantic Terminal'

#get the valid service ids for today
getDates()
stop_names,stop_ids=getStops()
getStopTimes()

endStops, connectors=getEndStops(origin)
origin_stop_id=stop_names[origin]

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
     
#showTimes(direct)      
#get connectors   
connector={}
for key in times_dct:
   if all_trips[key]!=dest_station:
      connector[key]=times_dct[key]
#showTimes(connector)  
for key in connector:
   print all_trips[key]






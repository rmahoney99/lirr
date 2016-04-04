import csv
import time
from datetime import date
from datetime import datetime
from datetime import timedelta

#VARIABLES

global times_lst
global trip_lst
global trip_dct
global JAMAICA
global JAMAICA_STOP
global service_ids
global trip_ids

trip_lst=[]
times_lst=[]
times_dct={}
JAMAICA="Jamaica"
JAMAICA_STOP="15"

origin_station="BABYLON"
branch="BABYLON"


#TODO
#Get the route numbers for each route using routes.txt
#hardcode to Babylon for now
route_id="1"

#TODO
#Get the stop_ids from stops.txt 
#hardcode to Babylon (118) for now
#Syosset - 58
#hardcode destination to Penn Station(8)
#hardcode destination to Hunterspoint Ave(2)
#hardcode destination to Atlantic Terminal(12)
origin_stop_id="58"
dest_stop_id="8"
dest_station='PENN STATION'
#dest_stop_id="12"
#dest_station='ATLANTIC TERMINAL'


# get the valid service ids for today's date from calendar_dates.txt
def getDates():
	dates = csv.reader(open('calendar_dates.txt'))
	svc_ids=[]

	for row in dates:
	   if row[1]==today:
   		svc_ids.append(row[0])

   
	service_ids=dict.fromkeys(svc_ids)



#get the trip ids from trips.txt for the requested destination
def getTrips(destination):
	trip_lst=[]
	trips = csv.reader(open('trips.txt'))

	for row in trips:
	   if row[1] in service_ids:
		if row[3].upper()==destination:
		#if row[0]==route_id and row[3].upper()==dest_station:
		   trip_lst.append(row[2])
   
	trip_ids=dict.fromkeys(trip_lst)
   
#get the stop_times from stop_times.txt
def getStopTimes():
   global stops
   stops = csv.reader(open('stop_times.txt'))
   return

def getTrains():

	for row in stops:
	   if row[0] in trip_ids and ( row[3]==origin_stop_id):
	      #if row[0] in trip_ids and (row[3]==dest_stop_id or row[3]==origin_stop_id):
	      offset=0
	      time1=row[1]
	      hr=time1[0:2]
	      rest=time1[2:8]
	      if hr=="24" or hr=="25":
           hr="23"
		     if hr=="24":
		       offset=1
		     if hr=="25":
		       offset=2
		     time1=hr+rest
	      time2=row[1]
	      hr=time2[0:2]
	      rest=time2[2:8]
	      if hr=="24" or hr=="25":
		     if hr=="24":
		       offset=1
		     if hr=="25":
		       offset=2
		     hr="23"
		     time2=hr+rest
	      dtm=datetime.strptime(today+time2,"%Y%m%d%H:%M:%S")+timedelta(hours=offset)
	      if dtm > curr_time:
            times_dct{row[0]}=dtm
      		
      
         return
#def getPartial():
#  return 

today=date.today().strftime("%Y%m%d")
curr_time=datetime.now()#- timedelta(hours=2)

getDates()
getStopTimes()
#get all trains that go direct
getTrips(dest_station)
getTrains()
sorted_list = [(k,v) for v,k in sorted(
                 [(v,k) for k,v in times_dct.items()]
                 )
              ]

for row in sorted_list:
  print row[0].strftime("%I %M")
#get trains that stop at jamacia
#getTrips(JAMAICA)
#getTrains()

times_lst.sort()
for row in times_lst:
  print row.strftime("%I %M")







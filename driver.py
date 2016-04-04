import csv
import time
from datetime import date
from datetime import datetime
from datetime import timedelta

#VARIABLES

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
origin_stop_id="118"
dest_stop_id="8"
dest_station='PENN STATION'
#dest_stop_id="12"
#dest_station='ATLANTIC TERMINAL'
JAMAICA='JAMAICA'
jamaica_stop_id='15'

today=date.today().strftime("%Y%m%d")
curr_time=datetime.now()#- timedelta(hours=4)

getDates()
getStopTimes()

#get the names of the stations that have transfers
transfers=getTransfers()

#get all trains that go direct
trip_ids=getTrips(dest_station)
origin_stop_id='118' #Babylon
times_dct=getTrains(trip_ids,origin_stop_id)
print "Direct trains"
showTimes(times_dct)
#get trains that stop at jamacia
dest_station='JAMAICA'
trip_ids=getTrips(dest_station)
times_dct=getTrains(trip_ids,origin_stop_id)
print "Change at Jamaica"
showTimes(times_dct)
#get trains that start at Jamacia and stop at Penn
dest_station='PENN STATION'
origin_stop_id='15'
trip_ids=getTrips(dest_station)
times_dct=getTrains(trip_ids,origin_stop_id)
print "Jamacia to Penn"
#showTimes(times_dct)


#times_lst.sort()
#for row in times_lst:
#  print row.strftime("%I %M")







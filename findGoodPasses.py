"""
This program takes in stations from settings.py and, for each station, finds X amount of future passes and 
all scheduled SatNOGS passes. It then compares the two. If a pass is calculated and scheduled, it is returned
as a "good pass", with the station ID and timeMaxEl, which should be used as the TX Down Time.
"""

from satnogsAPIRequests import getScheduledObservations
from calculatePasses import calculatePasses
import settings as settings
import logging

# Set up logging
logger = logging.getLogger("automagic.findGoodPasses")

def findGoodPasses():
    # Master array for all calculated passes
    allCalculatedPasses = []

    # Master array for all scheduled SatNOGS passes
    allSatnogsPasses = []

    # Loops to calculate all passes over each ground station
    for i in range(0, len(settings.STATION_LIST)):
        # Pulls station data from each station in the STATION_LIST from settings.py
        stationID = settings.STATION_LIST[i]['id']
        isSatnogs = settings.STATION_LIST[i]['isSatnogs']
        stationLatitude = str(settings.STATION_LIST[i]['lat'])
        stationLongitude = str(settings.STATION_LIST[i]['lng'])
        stationMinEl = settings.STATION_LIST[i]['minEl']

        # Calculates each pass over a station, returning time of max elevation, max elevation, and pass duration
        calculatedPasses = calculatePasses(stationID,stationLatitude, stationLongitude, stationMinEl, settings.NUM_PASSES)
        # Stores each station's passes into an array with station ID
        eachCalculatedPasses = {'id':stationID, 'isSatnogs': isSatnogs, 'calculatedPasses':calculatedPasses}

        # Stores above's array into a master list for all stations' passes
        allCalculatedPasses.append(eachCalculatedPasses)

        # Finds currently scheduled SatNOGS passes for each SatNOGS station and stores them into the master array allSatnogsPasses
        if isSatnogs == 'Y':
            satnogsPasses = getScheduledObservations(stationID)
            eachSatnogsPass = {'id':stationID, 'satnogsPasses': satnogsPasses}
            allSatnogsPasses.append(eachSatnogsPass)

    # Master array for passes that are "good" - both calculated and scheduled on SatNOG (includes all non-SatNOGS passes)
    goodPasses = []

    # Comparison code, checking that a calculated pass is scheduled. If it is, the pass's station ID and maxElTime is added to the goodPasses master array.
    for station in range(0,len(allCalculatedPasses)):
        stationsCalculatedPasses = allCalculatedPasses[station]['calculatedPasses']
        for eachCalculatedPass in range(0, len(stationsCalculatedPasses)):
            # Checks if station is SatNOGS or not
            if allCalculatedPasses[station]['isSatnogs'] == 'Y':
                for eachSatnogsStation in range(0,len(allSatnogsPasses)):
                    stationsSatnogsPasses = allSatnogsPasses[eachSatnogsStation]['satnogsPasses']
                    for eachSatnogsPass in range(0,len(stationsSatnogsPasses)):
                        # If the maxElTime is in between the start and end of a SatNOGS scheduled pass, append to goodPasses
                        # Also check to make sure the Satnogs Pass actually belongs to our calculated pass, otherwise you get station overlap
                        # Note: this large loop could be made a lot more efficient by only checking for satnogs passes on the stations whose ID matches our ID
                        if (float(stationsCalculatedPasses[eachCalculatedPass]['maxElTime']) > stationsSatnogsPasses[eachSatnogsPass]['start'])\
                        and (float(stationsCalculatedPasses[eachCalculatedPass]['maxElTime']) < stationsSatnogsPasses[eachSatnogsPass]['end'])\
                        and (allCalculatedPasses[station]['id'] == allSatnogsPasses[eachSatnogsStation]['id']):
                            eachGoodPass = {'id':allCalculatedPasses[station]['id'], 'maxElTime': stationsCalculatedPasses[eachCalculatedPass]['maxElTime'], 'maxEl': stationsCalculatedPasses[eachCalculatedPass]['maxEl'], 'passDuration': stationsCalculatedPasses[eachCalculatedPass]['passDuration']}
                            goodPasses.append(eachGoodPass)
            # If not SatNOGS station, append all passes
            else:
                eachGoodPass = {'id':allCalculatedPasses[station]['id'], 'maxElTime': stationsCalculatedPasses[eachCalculatedPass]['maxElTime'], 'maxEl': stationsCalculatedPasses[eachCalculatedPass]['maxEl'], 'passDuration': stationsCalculatedPasses[eachCalculatedPass]['passDuration']}
                goodPasses.append(eachGoodPass)
    
    logger.debug("%d passes found that are ready for transmisions: %s\n", len(goodPasses), str(goodPasses))

    return goodPasses

if __name__ == "__main__":
    ### Console Logging Setup. When the code is not called by the parent script, logging must be setup up separately.
    # Set initial level - anything below this level will not be passed to the handlers.
    logger.setLevel(logging.DEBUG)
    # Set formatting
    formatter = logging.Formatter('%(asctime)s %(name)s %(message)s')
    # Log to console:
    consoleHandler = logging.StreamHandler()
    # Sets debug level for the console handler
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    ### End Logging Setup

    goodPasses = findGoodPasses()

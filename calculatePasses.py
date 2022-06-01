'''
This program is used to calculate upcoming passes over ground stations.
Pass in the latitude (str), longitude (str), minimum elevation (float/int), and number of passes to return (int)
Note: format for latitude and longitude is a string like: '32.9342'
Returns a list of the upcoming pass with the max elevation time (unix timestamp, int), max elevation (degrees, float), duration (minutes, float)
'''
import math
# import ephem
import urllib.request
import logging
from datetime import timezone

# Set up logging
logger = logging.getLogger("ASH.calculatePasses")

def calculatePasses(stationID,latitude,longitude,minEl,numPasses):
    logger.debug('started calculatePasses')

    # Counter for number of passes checked
    count = 0
    # Counter for number of errors, to exit loop if exceeds too many
    errorCount = 0

    # # Uncomment below to use manually input TLE.
    # #tle = [0,0,0]
    # #tle[0] = "GASPACS"
    # #tle[1] = "1 99430U          22027.51174303  .00000000  00000-0  14174-3 0    05"
    # #tle[2] = "2 99430  51.6451 313.2440 0006867  67.2904 106.1030 15.50184441    05"  

    # # Uncomment below to pull TLE from Celestrak (preferred method)
    # tle_url = 'https://celestrak.com/satcat/tle.php?CATNR=51439'
    # # Pulls text from TLE URL, decodes, and appends to tle list
    # tle = []
    # uf = urllib.request.urlopen(tle_url)
    # for line in uf:
    #     decoded_line = line.decode('utf-8')
    #     tle.append(str(decoded_line))

    # # Converts tle so that ephem can interpret it as a body
    # sat = ephem.readtle(tle[0], tle[1], tle[2])

    # # obs being where the observer is. Logan is 41.735210, -111.834862. 
    # obs = ephem.Observer()

    # # Set latitude and longitude for ephem
    # obs.lat = latitude
    # obs.lon = longitude

    listOfPasses = [{'maxElTime': 0, 'maxEl': 0, 'passDuration': 60}, {'maxElTime': 0, 'maxEl': 0, 'passDuration': 30}, {'maxElTime': 0, 'maxEl': 0, 'passDuration': 15}, {'maxElTime': 0, 'maxEl': 0, 'passDuration': 5}]

    # # This does all the magic in computing the passes
    # while len(listOfPasses) < numPasses:
    #     # next_pass returns a six-element tuple giving:
    #     # 0  Rise time
    #     # 1  Rise azimuth
    #     # 2  Maximum elevation time
    #     # 3  Maximum elevation
    #     # 4  Set time
    #     # 5  Set azimuth
    #     try:
    #         timeRise, azRise, timeMaxEl, maxEl, timeSet, azSet = obs.next_pass(sat)

    #         # Convert from ephem.Date to datetime.datetime unix timestamps
    #         timeRiseTimestamp = timeRise.datetime().replace(tzinfo=timezone.utc).timestamp()
    #         timeMaxElTimestamp = timeMaxEl.datetime().replace(tzinfo=timezone.utc).timestamp()
    #         timeSetTimestamp = timeSet.datetime().replace(tzinfo=timezone.utc).timestamp()

    #         # Calculates the duration of the transit, from rise to set, in minutes. 
    #         duration =  (timeSetTimestamp - timeRiseTimestamp)/60

    #         # Makes a list for each individual pass, adding the max elevation time, max elevation, and pass duration.
    #         eachPass = {'maxElTime':int(round(timeMaxElTimestamp,0)), 'maxEl':round(math.degrees(maxEl),1), 'passDuration':round(duration,1)}

    #         # Adds each individual pass into a single list to ease storage and exporting.
    #         # Note: pass is only added if its max elevation is above the input min elevation
    #         if math.degrees(maxEl) >= minEl:
    #             listOfPasses.append(eachPass)

    #         # This increments the time past the current pass start time, so the next pass is computed properly
    #         obs.date = timeRise + ephem.minute

    #         count +=1
    #         if count > 24:
    #             logger.warning("WARNING: only %d passes above min elevation found after checking 24 passes!",len(listOfPasses))
    #             break
            
    #     except:
    #         logger.warning("WARNING: Pyephem broke yet again!")
    #         errorCount +=1
    #         if errorCount > 50:
    #             logger.error("ERROR: Pyephem broke more than 50 times!")
    #             return listOfPasses
    #         # This increments the time an hour past the current pass start time, so the next pass is hopefully computed properly
    #         obs.date = timeRise + ephem.hour
            

    
    # logger.warning("List of passes for station: %s (lat: %s, long: %s)\n%s\n", stationID, latitude, longitude, listOfPasses)

    return listOfPasses

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
    
    # GAS Ground Station location
    latitude = '55.633'
    longitude = '12.6'
    minEl = 30
    numPasses = 5
    stationID = 'test'
    listOfPasses = calculatePasses(stationID,latitude,longitude,minEl,numPasses)

#!/usr/bin/env
'''
On start, grabs next pass over our GS, counts down to the pass 
10 mins before the start of pass over our GS: 
    Calculates all of the upcoming passes over all of the ground stations 
    Calculates delta-T's 
    Generates packets 
    Gets desired data from list.  
Sends up Clear TX Windows 30 secs before TCA (time can be changed once tested), then sends all of the upcoming windows starting at TCA.  
Sends take picture command on sunny passes 
After pass: grab next pass 
'''
import logging
from logging.handlers import TimedRotatingFileHandler
# import calculatePasses
# import settings
import time
from time import sleep
import findGoodPasses
import createPackets
import sendPackets
import RPi.GPIO as GPIO

# Set up logging
logger = logging.getLogger("ASH")
logging.basicConfig(level=logging.DEBUG)

def main():
    logger.debug("Starting ASH program")

    # GPIO Pin for enabling transceiver. Pull the pin high to enable transceiver
    EN_UHF_GPIO = 18

    #Set up the GPIO pins for use
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(EN_UHF_GPIO, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(EN_UHF_GPIO, GPIO.HIGH)

    takePicCommand = createPackets.createCommandPacket(takePic=True)

    """NOTE: SET THE DATA TYPE AND COMMANDS IN THIS SECTION"""

    # Choose tx duration, data type, pic number, and line number for all the upcoming passes
    # Data types: 0 - Attitude, 1 - TTNC, 2 - Deploy, 3 - HQ, 4 - LQ
    txDuration = 10
    dataType = 0
    picNumber = 0
    lineNumber = 0

    selectedCommand = [{'packetData':takePicCommand}]
    logger.debug('Selected command: %s', selectedCommand)

    """END DATA/COMMAND SELECTION"""

    preBuffer = 2 * 60

    while True:
        # Flag for if the passes have been calculated and packets generated
        prepared = False
        # Flag for if the commands have been sent
        commandTXSent = False
        # Flag for if the windows have been sent
        windowTXSent = False

        transmissionTiming = 1 * 60
        nextPassTime = round(time.time() / transmissionTiming) * transmissionTiming + transmissionTiming
        logger.info("Next Pass TCA: %s", nextPassTime)

        while True:
            timeUntilPass = nextPassTime - round(time.time())

            if timeUntilPass < preBuffer and not prepared:
                logger.info("Within buffer time, calculating passes and creating packets!")

                # calculate good passes
                goodPasses = findGoodPasses.findGoodPasses()

                # calculate delta-t
                passesWithDeltaT = createPackets.calculateDeltaT(goodPasses, nextPassTime)

                # Add packet info to passes dictionary
                # Note: this will need to be improved for a queue-type system eventually
                passesWithPacketInfo = passesWithDeltaT
                for eachPass in passesWithPacketInfo:
                    eachPass.update({'txDuration':txDuration, 'dataType':dataType, 'picNumber':picNumber, 'lineNumber':lineNumber})

                dataType = 1 - dataType

                # Create packet data, add the final packet data to the dictionary
                passesWithPacketData = passesWithPacketInfo
                for eachPass in passesWithPacketData:
                    logger.debug("Packet info: %d %d %d %d %d", eachPass.get('deltaT'),eachPass.get('txDuration'),eachPass.get('dataType'),eachPass.get('picNumber'),eachPass.get('lineNumber'))
                    eachPassPacketData = createPackets.createWindowPacket(eachPass.get('deltaT'),eachPass.get('txDuration'),eachPass.get('dataType'),eachPass.get('picNumber'),eachPass.get('lineNumber'))
                    eachPass.update({'packetData':eachPassPacketData})

                logger.debug("%d Passes with Packet Data Ready To Send: %s\n", len(passesWithPacketData), passesWithPacketData)

                prepared = True

            # Transmit up command packets 30 secs before TCA
            elif timeUntilPass <= 32 and timeUntilPass >= 28 and not commandTXSent:
                logger.info("Time to transmit commands!")
                # Send up command packet
                sendPackets.sendPackets(selectedCommand)
                commandTXSent = True
                
            # Transmit up window packets at TCA
            elif timeUntilPass <= 2 and timeUntilPass >= -2 and not windowTXSent:
                logger.info("Time to transmit windows!")
                # Send up window packets
                sendPackets.sendPackets(passesWithPacketData)

                windowTXSent = True
                
            # The current window is over, break the loop to calculate the next window and do it all again
            elif timeUntilPass < -5:
                break

            else:
                sleep(1)




if __name__ == "__main__":
    ## Console Logging Setup. When the code is not called by the parent script, logging must be setup up separately.
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

    # # Log to file. Note this swaps files to a new file every day (old file is saved with date extension).
    # timedFileHandler = TimedRotatingFileHandler('logFiles/automagic/automagic.log', when="D", interval=1)
    # # Sets debug level for the files
    # timedFileHandler.setLevel(logging.DEBUG)
    # timedFileHandler.setFormatter(formatter)
    # logger.addHandler(timedFileHandler)
    # ### End Logging Setup

    main()
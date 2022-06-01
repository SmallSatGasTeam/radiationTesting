"""
This program takes in a a packet, or list of packets (for tx windows) and then sends them to Endurosat radio.
Puts the local radio in pipe mode, then the remote radio in pipe mode, then loops through the inputted packets to send them up 
"""
import logging
import createPackets
from time import sleep
import serial

# Set up logging
logger = logging.getLogger("ASH.sendPackets")

def sendPackets(packetList):
    serialPort = serial.Serial('/dev/serial0', 115200)

    # Set ground radio pipe mode to 60 sec timeout (in case satellite signal is weak)
    logger.info("Setting local radio pipe mode timeout to 60 seconds")
    serialPort.write(b'ES+W23060000003C\r')
    logger.info(b'ES+W23060000003C\r')
    sleep(.5)

    # Put ground radio in pipe mode
    logger.info("Putting local radio in pipe mode")
    serialPort.write(b'ES+W23003321 10E2651B\r') #Changed based on which is transmitting
    logger.info(b'ES+W23003321 10E2651B\r')
    sleep(.5)

    # Transmits command to disable audio beacon 5 times in a row
    # This allows the amplifier to "charge up"
    logger.info("disabling audio beacon")
    for i in range(5):
        serialPort.write(b'ES+W220800000000\r')
        logger.info(b'ES+W220800000000\r')
        sleep(.120)

    # Transmits command to put satellite radio in pipe mode, an enables or disables AX.25 beacon
    # Enable AX Beacon
    """
    for i in range(5):
        logger.info("enabling ax beacon, putting sat radio into pipe mode")
        serialPort.write(b'ES+W22003361\r')
        logger.info(b'ES+W22003361\r')
        sleep(.120)
    """
    # Disable AX Beacon, put satellite radio in pipe mode
    for i in range(5):
        logger.info("disabling ax beacon, putting sat radio into pipe mode")
        serialPort.write(b'ES+W22003321\r')
        logger.info(b'ES+W22003321\r')
        sleep(.120)

    # Transmit packet data
    for eachPacket in packetList:
        packetData = eachPacket.get('packetData')
        logger.debug("Sending packet data: %s", packetData)
        serialPort.write(packetData)
        sleep(.120)

    #serialPort.close()
    return

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

    clearTXWindowsCommand = createPackets.createCommandPacket(clearWindows=True,takePic=False,deployBoom=False,reboot=False,skipToPost=False,deletePics=False,deleteData=False)
    selectedCommand = [{'packetData':clearTXWindowsCommand}]
    sendPackets(selectedCommand)

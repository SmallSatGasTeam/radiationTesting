'''
This program is used to create the hex packets to send to GASPACS for either tx windows or commands.
Pass in the desired parameters like data type, delta-t, duration, etc. 
It returns the tx window command. 
Also creates and returns command packets. 
'''
import logging
from logging.handlers import TimedRotatingFileHandler
import hmac
import hashlib

# Set up logging
logger = logging.getLogger("automagic.createPackets")


"""
This function creates the packets for TX Windows.
IMPORTANT: all values must be passed in as integers!
Inputs:
deltaT        Number of seconds until window start
duration      Duration of the window in seconds
dataType      Number from 0-4 corresponding to requested data type. 0 - Attitude, 1 - TTNC, 2 - Deploy, 3 - HQ, 4 - LQ
picNum        Number of the picture that is requested. Pass in zero if not requesting a picture.
lineNum       Line number you want to index from or 0 to go from the last transmission
Output:
packet        Hex data of full packet to send to the radio, including carriage return
"""
def createWindowPacket(deltaT,duration,dataType,picNum,lineNum):
    logger.debug("started createWindowPacket")

    # Window packet
    packet = '00000000'
    packet += int4tobin(deltaT)
    packet += int2tobin(duration)
    packet += int1tobin(dataType)
    packet += int2tobin(picNum)
    packet += int4tobin(lineNum)
    packet = hex(int(packet, 2))[2:].zfill(28)
    logger.debug("Window packet content: %s", packet)

    # Packet encryption
    encryptedPacket = encrypt(packet)
    logger.debug("Encrypted Window packet content: %s", encryptedPacket)

    # Add GASPACS header, footer, and carriage return
    fullPacket = bytearray.fromhex(b'GASPACS'.hex() + encryptedPacket + b'GASPACS'.hex())+ b'\r'
    logger.debug("Full Window packet hex: %s", b'GASPACS'.hex() + encryptedPacket + b'GASPACS'.hex() + '\r')

    return fullPacket

"""
This function creates the packets for Commands.
IMPORTANT: all values must be passed in as booleans!
Inputs:
clearWindows    Clears TX windows and TX flags (last line number) file
takePic         Takes a picture
deployBoom      Triggers boom deployment driver
reboot          Sends "sudo reboot" command to Pi
skipToPost      Skip to Post Boom Deploy Mode
deletePics      Deletes all pictures on GASPACS
deleteData      Delete Attitude, TTNC, and Deploy Data
Output:
packet        Hex data of full packet to send to the radio, including carriage return
"""
def createCommandPacket(clearWindows=False,takePic=False,deployBoom=False,reboot=False,skipToPost=False,deletePics=False,deleteData=False):
    commandsList = []
    content = '00000001'
    # Append True to set flag file to enable satellite transmissions
    commandsList.append(True)
    commandsList.append(clearWindows)
    commandsList.append(takePic)
    commandsList.append(deployBoom)
    commandsList.append(reboot)
    # Append False because we don't have the AX.25 digipeater on GASPACS but still need to add the bits
    commandsList.append(False)
    commandsList.append(skipToPost)
    commandsList.append(deletePics)
    commandsList.append(deleteData)

    for command in commandsList:
        if command == False:
            content += '00000000'
        else:
            content += '00000001'

    # Convert to hex and zfill to add the leading 0
    packet =  hex(int(content, 2))[2:].zfill(20)
    logger.debug("Command packet content: %s", packet)
    
    # Packet encryption
    encryptedPacket = encrypt(packet)
    logger.debug("Encrypted Command packet content: %s", encryptedPacket)
    
    # Add GASPACS header, footer, and carriage return
    fullPacket = bytearray.fromhex(b'GASPACS'.hex() + encryptedPacket + b'GASPACS'.hex())+ b'\r'
    logger.debug("Full Command packet hex: %s", b'GASPACS'.hex() + encryptedPacket + b'GASPACS'.hex() + '\r')

    return fullPacket

'''
This function calculates the delta-T for packets given a dictionary list of the passes and the TCA.
It appends the delta-T to the dictionary for each pass, and appends the passes with positive delta-T to a new list, which it returns.
'''
def calculateDeltaT(goodPasses,nextPassTime):
    # List of passes with positive delta-T
    goodDeltaTPasses = []
    for eachPass in goodPasses:
        txDownTime = eachPass['maxElTime']
        deltaT = txDownTime - nextPassTime
        # Don't append pass if it has a negative deltaT (this happens for some west coast stations where their minElTime is before ours)
        if deltaT < 0:
            continue
        # Accounting for scheduling a TX window during the current pass
        elif eachPass['id'] == 2550:
            deltaT += 35
        eachPass.update({'deltaT':deltaT})
        goodDeltaTPasses.append(eachPass)

    logger.debug("%d Good passes with Delta-T: %s\n", len(goodDeltaTPasses), goodDeltaTPasses)
    return goodDeltaTPasses

def int4tobin(num):
	"""takes a 4 byte int, returns a binary representation of it"""
	return str(format(num, '032b'))[-32:]

def int1tobin(num):
	"""takes a 1 byte integer, returns a binary representation of it"""
	return str(format(num, '08b'))[-8:]

def int2tobin(num):
	"""takes a 2 byte integer, returns a binary representation of it"""
	return str(format(num, '016b'))[-16:]

def encrypt(packet):
	"""encrypt packet using hmac and append hash to the end of the packet"""
	key = b'SECRETKEY'
	binaryPacketLength = len(packet) * 4
	binaryPacket = bytes(format(int(packet,16), 'b').zfill(binaryPacketLength), 'utf8')
	hash = hmac.new(key, binaryPacket, digestmod=hashlib.md5)
	hashhex = hash.hexdigest()
	encryptedPacket = packet + hashhex
	return encryptedPacket

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

    windowPacket = createWindowPacket(30,30,0,0,1)
    logger.info("Window packet: %s", windowPacket)
    clearTXWindowsPacket = createCommandPacket(clearWindows=True)
    logger.info("Clear TX Windows Packet: %s", clearTXWindowsPacket)

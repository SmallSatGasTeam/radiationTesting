import asyncio
import serial
from time import sleep
import hmac
import hashlib
""" Creates packets in proper formats for transmission and requests that format from satellite """
    
def packetSelect(typeOfPacket, dataType):
    if(typeOfPacket == 'Window'):
        # Window packet
        packet = '00000000'
        packet += int4tobin(30) # 'Input the number of seconds until window start: '
        packet += int2tobin(10) # 'Input the duration of the window in seconds: '
        packet += int1tobin(dataType) 
        # 'Number from 0-4 corresponding to requested data type.\n0 - Attitude, 1 - TTNC, 2 - Deploy, 3 - HQ, 4 - LQ: '
        packet += int2tobin(0) # picture number
        packet += int4tobin(1) # start from line 1
        print(packet)
        print(hex(int(packet, 2))[2:].zfill(28))
        return hex(int(packet, 2))[2:].zfill(28)

    else:
        #Command Packet
        commandsList = []
        content = '00000001'
        commandsList.append(1) # 'Input 0 for disable TX, 1 for enable TX: '
        commandsList.append(0) # 'Input 0 for do nothing, 1 for erase all TX windows and progress: '
        commandsList.append(1) # input('Input 0 for do nothing, 1 for take a picture: ')
        commandsList.append(0) # dont deploy boom
        commandsList.append(0) # dont reboot
        commandsList.append(0) # dont enable AX25
        commandsList.append(1) # skip to postBoomDeploy
        commandsList.append(0) # don't delete pictures
        commandsList.append(0) # dont delete data
        commandsList.append(0) # disable beacon
        commandsList.append(0) # disable audio beacon
        commandsList.append(0)
        commandsList.append(0)
        commandsList.append(0)
        commandsList.append(0)
        #If more commands are added, we must take out some of the dead bits
        for command in commandsList:
            if command == '0':
                content += '00000000'
            else:
                content += '00000001'
        #This adds 4 dead bits to the end
        return hex(int(content, 2))[2:].zfill(32)
		


def transmitPacket(packet, AX25):
	serialPort = serial.Serial('/dev/serial0', 115200)
	serialPort.write(b'ES+W23003321\r') #Changed based on which is transmitting
	sleep(1)
	for i in range(50):
		serialPort.write(b'ES+W22003321\r')
		sleep(.120)
	print(packet)
	if AX25:
		data = bytearray.fromhex(packet)
	else:
		data = bytearray.fromhex(b'GASPACS'.hex() + packet + b'GASPACS'.hex())
		print(b'GASPACS'.hex() + packet + b'GASPACS'.hex())
	print('Sending Data')
	print(data)
	serialPort.write(data)

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
	fullpacket = packet + hashhex
	return fullpacket

def main():
    print("Started running program")
    timeBetweenPasses = 3 * 60
    print(str(timeBetweenPasses) + " seconds between passes")
    timeElasped = 0
    typeOfPacket = "Window"
    dataType = 0
    while True:
        if (timeElasped >= timeBetweenPasses - 2 and timeElasped <= timeBetweenPasses + 2):
            packet = packetSelect(typeOfPacket, dataType)

            encryptedPacket = encrypt(packet)
            transmitPacket(encryptedPacket, False)

            timeElasped = 0
        else:
            sleep(1)
            timeElasped += 1
            print("Time Elapsed: " + str(timeElasped))

if __name__ == '__main__':
	main()
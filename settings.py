from hashlib import sha3_384
import logging

# Set up logging
logger = logging.getLogger("automagic.settings")

# Station data
GAS_ROT = {'id': 2550, 'isSatnogs':'N', 'lat':'41.743', 'lng':'-111.807', 'minEl':0}
K4KDR = {'id': 'Scott K4KDR', 'isSatnogs':'N', 'lat':'35.665', 'lng':'-77.718', 'minEl':40}
W7KKE = {'id': 488, 'isSatnogs':'Y', 'lat':'45.010', 'lng':'-124.010', 'minEl':25}
DL4PD = {'id': 37, 'isSatnogs':'Y', 'lat':'50.75', 'lng':'6.216', 'minEl':60}
OM7AAK = {'id': 2138, 'isSatnogs':'Y', 'lat':'48.336', 'lng':'17.448', 'minEl':60}
OZ7SAT = {'id': 49, 'isSatnogs':'Y', 'lat':'55.633', 'lng':'12.6', 'minEl':60}
XV9PID = {'id': 2401, 'isSatnogs':'Y', 'lat':'21.023', 'lng':'105.542', 'minEl':60}
TOKOROZAWA =  {'id': 2152, 'isSatnogs':'Y', 'lat':'35.797', 'lng':'139.483', 'minEl':60}
ITRUHF = {'id': 1382, 'isSatnogs':'Y', 'lat':'-34.813', 'lng':'138.620', 'minEl':25}
TBC = {'id': 981, 'isSatnogs':'Y', 'lat':'-34.480', 'lng':'-58.780', 'minEl':70}
BOB_KELLER_TX = {'id': 'BOB KELLER TX', 'isSatnogs':'N', 'lat':'32.934', 'lng':'-97.229', 'minEl':25}
BOB_BRISTOL_RI = {'id': 'BOB BRISTOL RI', 'isSatnogs':'N', 'lat':'41.677', 'lng':'-71.266', 'minEl':25}
MAUSYAGI = {'id': 2134, 'isSatnogs':'Y', 'lat':'42.288', 'lng':'-73.33', 'minEl':15}
PISZKESTETO = {'id': 2380, 'isSatnogs':'Y', 'lat':'47.917', 'lng':'19.895', 'minEl':25}
NEWULM = {'id': 853, 'isSatnogs':'Y', 'lat':'29.855', 'lng':'-96.527', 'minEl':25}
N9CQQ = {'id': 1539, 'isSatnogs':'Y', 'lat':'42.918', 'lng':'-88.131', 'minEl':35}
#MALYI = {'id': 1585, 'isSatnogs':'Y', 'lat':'48.018', 'lng':'20.797', 'minEl':25}
LW2DYB = {'id': 1861, 'isSatnogs':'Y', 'lat':'-38.280', 'lng':'-57.854', 'minEl':70}

# Spoofed stations for testing
# S1 = {'id': 'S1', 'isSatnogs':'N', 'lat':'41.304634', 'lng':'-71.273608', 'minEl':0}
# S2 = {'id': 'S2', 'isSatnogs':'N', 'lat':'40.583192', 'lng':'-66.672104', 'minEl':0}
# S3 = {'id': 'S3', 'isSatnogs':'N', 'lat':'38.825266', 'lng':'-59.770673', 'minEl':0}
# Stations to calculate and set up passes over. Uses SatNOGS Station ID.
STATION_LIST = [GAS_ROT, K4KDR, W7KKE, DL4PD, OM7AAK, OZ7SAT, XV9PID, TOKOROZAWA, ITRUHF, TBC, MAUSYAGI, PISZKESTETO, NEWULM, N9CQQ, LW2DYB]
#STATION_LIST = [S1,S2,S3]
# Minimum elevation for each pass over a station
MIN_EL = 10

# Number of future passes to schedule
NUM_PASSES = 5

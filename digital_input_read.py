#Benjamin Cary, bencary@mit.edu
#some code by Peter N. Saeta, Harvey Mudd College Professor, 2011 July 2

# Commands you need before you can use the labjack with linux:
    # $ sudo apt-get install build-essential
    # $ sudo apt-get install libusb-1.0-0-dev
    # $ sudo apt-get install git-core
    # $ git clone git://github.com/labjack/exodriver.git
    # $ cd exodriver/
    # $ sudo ./install.sh
    # $ cd ..
    # $ git clone git://github.com/labjack/LabJackPython.git
    # $ cd LabJackPython/
    # $ sudo python setup.py install

import u3, time
from math import sqrt

# Prepare the u3 interface for streaming

d = u3.U3()		# initialize the interface; assumes a single U3 is plugged in to a USB port
d.configU3()	# set default configuration
d.configIO(FIOAnalog = 0)		# ask for digital inputs
d.setFIOState(0, state = 0) #sets state low and sets as output (which is fixed by next function
d.getDIState(0) #sets digital input


# requests digital I/O channels to be scanned,
# more special terminals here: https://labjack.com/support/datasheets/u3/operation/stream-mode/digital-inputs-timers-counters
# negative channel should almost always be set 31. The sampling frequency is 5000 samples (of each channel)
# per second. The Resolution parameter sets the effective quality of the
# samples. See http://labjack.com/support/u3/users-guide/3.2
d.streamConfig( NumChannels = 1,
	PChannels = [193],
	NChannels = [31],
	Resolution = 3,
	SampleFrequency = 5000 )

d.packetsPerRequest = 1   # you can adjust this value to get more or less data

# Try to measure a data set.
def measure():
	try:
		d.streamStart()

		for r in d.streamData():
			if r is not None:
				if r['errors'] or r['numPackets'] != d.packetsPerRequest or r['missed']:
					print "error"
				break
	finally:
		d.streamStop()
	return r

# Write a set of data to a file "lmao.txt"
def writeData( r ):
	f = open( 'lmao.txt', 'w' )

	for i in range(0, len(r)):
		f.write(str(r['AIN193'])+'\n')
	f.close()

def findComplete(r):
    for i in range(0, len(r)):
        if (r['AIN193'][i] == (255, 255)):
            print r['AIN193'][i]
            print "complete"
            return False
        else:
            return True

not_complete = True
while(not_complete):
    not_complete = findComplete( measure() )

# for writing scanned data into a file
# for i in range(1,5):
#     writeData(measure())
#     sleep(1)

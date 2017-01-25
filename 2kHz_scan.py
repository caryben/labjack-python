#Benjamin Cary, bencary@mit.edu

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

# This program scans bits from a file in the same folder and outputs them with trailing clock signals

# IMPORTANT: Have a text file called 'bits_to_send.txt' in the same folder that you run this code

import u3, time
b = u3.U3()
b.configIO()

# Test code for 2kHz digital stream out
stream = open('bits_to_send.txt', 'r') #file should have same name in the same folder
total_stream = stream.read()

x = 0
while(x<len(total_stream)-1):
    stream.seek(x)
    i = stream.read(1) #returns the value at that location and goes to the next byte when called again
    if(i == ''):
        break

    val = int(str(i))
    b.setFIOState(0, state = i)

    #changing clock values
    b.setFIOState(1, state = 1)
    time.sleep(.00005)#speed determined from max frequency of changing from one period
    b.setFIOState(1, state = 0)

    #changing second clock values
    b.setFIOState(2, state = 1)
    time.sleep(.00005)
    b.setFIOState(2, state = 0)

    x+=1

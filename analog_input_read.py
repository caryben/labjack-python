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

#info on function used: https://labjack.com/support/datasheets/u3/low-level-function-reference/feedback/bitstateread

import u3, time


def read(IO_val, voltage_level):
    b = u3.U3()#creates labjack interface object

    #which IO location you're using

    # using analog
    b.configIO(FIOAnalog = 255)#sets all FIO pins to analog

    init_time = 0

    not_complete = True

    while(not_complete):
        analog_val = b.getAIN(IO_val ,32)
        if(analog_val >= voltage_level):
            not_complete = False
        print str(init_time) + ": " + str(analog_val)
        init_time += 1
        time.sleep(.1)

    b.close()

    print("It is complete.")



#IO values
# 0-7    FIO0-FIO7
# 8-15   EIO0-EIO7
# 16-19  CIO0-CIO3

#calls the function
read(0, 0.5) #(IO value, voltage read threshhold)

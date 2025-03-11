####################################################################################################
#
# PMFLtest - 2/5/2025 - Tyler Frischknecht
# Pennathur Microfluidics Lab Keithley Test Commands
#
####################################################################################################
# Import Libraries
from helper.pmflmail import sendEmail
from helper.pmflfile import makeAllFiles 
import pyvisa
import numpy
import time
#
####################################################################################################
# Global Variables
keithleyGPIB = 20
#
####################################################################################################
#
def runTest(voltage, testTime, emails, name, info):
    voltage = float(voltage)
    testSuccess = False
    try:
        keithley = connectToKeithley()
        print("Setting limits.")
        setLimits(keithley, voltage)
        print("Running the test right now! Check back in ", testTime, " minutes!")
        data = sourceAndRead(keithley, voltage, testTime)
        testSuccess = True
    except pyvisa.VisaIOError as e:
        print(f"VisaIOError: {e}")
        print(f"Sorry about that, please run the test again!")
    except Exception as e:
        print(f"Exception: {e}")
        print(f"Sorry about that, please run the test again!")
    finally:
        if 'keithley' in locals() and keithley is not None:
            try:
                keithley.close()
                print("Connection with Keithley terminated.")
            except Exception as e:
                print(f"Failed to close connection with Keithley - {e}")
    if testSuccess == True:
        # put data into file here!
        makeAllFiles(data, 1)
        sendEmail(emails, f"({voltage} V) "+ name, info)
        print("Thank you for using my code!! Program end.")
        print("-"*100)
#
####################################################################################################
# Connects to Keithley and returns keithley as object to write to with pyvisa
def connectToKeithley():
    rm = pyvisa.ResourceManager()  # This will manage the connection
    keithley = rm.open_resource(f'GPIB::{keithleyGPIB}::INSTR')  # Open connection to the Keithley
    keithley.write("*CLS")
    keithley.write("*RST")
    print("-"*100)
    print("Connected to Keithley Model:", keithley.query("*IDN?"), end="")
    print("-"*100, end="\n\n")
    time.sleep(1)
    return(keithley)
#
####################################################################################################
#
def setLimits(keithley, sourceVoltage):
    # Enable Voltage and Current Limit
    keithley.write("SOUR:VOLT:LIM:STAT 1")      # Turns voltage limiting on
    # Applies numerical limits
    keithley.write("SOUR:VOLT:LIM " + str(abs(sourceVoltage)+5))
    keithley.write("SENS:FUNC 'CURR:DC'")       # Sets the current measuring value to current
    keithley.write("SENS:CURR:RANG:AUTO 1")     # Enables auto range for current
    keithley.write("SENS:CURR:DIG 6")           # Sets float decimal digits to max (6)
    keithley.write("SYST:ZCH 1")                # Turns zero check off
    keithley.write("SYST:ZCH 0")                # Turns zero check off
    keithley.write("SYST:ZCOR 1")               # Turns zero correction on
#
####################################################################################################
#
def sourceAndRead(keithley, voltage, testTime):
    data = []
    numReadings = 0
    zeroTime = 0
    zeroCount = 0
    nextReading = time.time()
 
    keithley.write("SOUR:VOLT " + str(voltage)) # Sets voltage output to voltage           
    keithley.write("OUTP 1")

    while numReadings < int(testTime*120)+1:
        nowTime = time.time()
        if (nowTime >= nextReading): 
            keithley.write("INIT")
            newData = keithley.query("FETCH?")
            newData = newData.strip().split(',')
            newData[0] = newData[0][:-4]
            newData[1] = float(newData[1][:-4]) - zeroTime
            newData[2] = int(newData[2][:-5]) - zeroCount
            # Set Zeroes if Zero
            if zeroTime == 0:
                zeroTime = newData[1]
                newData[1] = 0.0
                zeroCount = newData[2]
                newData[2] = 0
            data.append(newData)
            print(newData)
            numReadings += 1
            nextReading = nowTime + 0.5
   
    keithley.write("OUTP 0") # Turns voltage output off
    return(data)
#
####################################################################################################
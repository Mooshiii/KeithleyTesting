####################################################################################################
#
# Pennathur Laboratory Keithley 6517a Test Software
# Most Recent Rev: 2/19/2025
#
####################################################################################################
# The good stuff starts here!
#
# Put email(s) you want data sent to here seperated by commas:
# Ex.          = "email@gmail.com, email2@gmail.com, email3@gmail.com"
emailAddresses = "tfrischknecht@ucsb.edu, tbrooksdf@gmail.com"
#
# Put the title of your test here:
# Voltage is automatically added to the front! "Test1" -> "(5V) Test1"
# Ex.    = "100mM NaCl Test 1"
testName = "1.2k Resistor"
#
# If you have any additional comments you would like to include, please include them here!
# Otherwise, you may leave the quotation marks blank:
# Ex.              = "We re-ran the test because the first chip was broken :("
testAdditionalInfo = "Current Test!"
#
# Put the voltage you'd like to source here (in V):
voltage = []
for i in range(-19,21):
    voltage.append(i)
#
# Put the time you'd like the test to run here (in min):
testTime = 2
#
#
####################################################################################################
# Please don't touch this part, its important!!
from helper.pmfltest import runTest
for i, v in enumerate(voltage):
    runTest(v, testTime, emailAddresses, testName, testAdditionalInfo)
#
####################################################################################################
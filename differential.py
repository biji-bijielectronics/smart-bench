# Simple demo of reading the difference between channel 1 and 0 on an ADS1x15 ADC.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15
#import numpy as np


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()



# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1
  #  ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
  # //ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
  # // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  # // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
  # // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  # // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV
gain = 0.125

current_list = []
previous_time = 0
voltage_list=[]

print('Press Ctrl-C to quit...')
while True:
    # Read the difference between channel 0 and 1 (i.e. channel 0 minus channel 1).
    # Note you can change the differential value to the following:
    #  - 0 = Channel 0 minus channel 1
    #  - 1 = Channel 0 minus channel 3
    #  - 2 = Channel 1 minus channel 3
    #  - 3 = Channel 2 minus channel 3
    v = (adc.read_adc(2,gain=1,data_rate=128)*0.000125)/10/0.01
    voltage_reading = (adc.read_adc(3,gain=1,data_rate=128)*0.000125)/10
    # Note you can also pass an optional data_rate parameter above, see
    # simpletest.py and the read_adc function for more information.
    # Value will be a signed 12 or 16 bit integer value (depending on the ADC
    # precision, ADS1015 = 12-bit or ADS1115 = 16-bit).
    # print 'Channel 0 minus 1: ' , round(value * gain/1000,3), round(value * gain /  0.01 /1000,3),v 
    
    current_time = time.time()

    #    print current_time - previous_time
    if current_time - previous_time > 0.0001:
       previous_time = current_time
       
 
       if len(current_list) < 40:
          current_list.append(v)
          
          # print current_list 
       else:
          averaged_current = sum(current_list)/40

          # print round(averaged_current,3)
          current_list = []
          current_list.insert(0,round(averaged_current,1))
         
        


       if len(voltage_list) < 40:
          voltage_list.append(voltage_reading)

          # print current_list
       else:
          averaged_voltage = sum(voltage_list)/40

          print round(averaged_voltage*100,1),round(averaged_current,1)
          voltage_list = []
          voltage_list.insert(0,round(averaged_voltage,1))

  
       
     
    
    # Pause for half a second.
    

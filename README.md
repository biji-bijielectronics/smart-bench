# smart-bench
##Introduction
A lab bench energy calculator that takes in input for various DC sources such as solar panels, charge controllers, bicycle generators and measures the voltage and current to calculate power.
##
The Smart Bench Energy Calculator utilises a RaspberryPi to read an ADS1115 Analog-to-Digital module that has bene setup to operate as a current and voltage meter.
It streams the output of the ADC to Flask-based webserver with websockets

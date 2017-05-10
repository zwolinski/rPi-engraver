#!/usr/bin/python
# -*- coding: utf-8 -*-
# drv.py - Obsluga graweru

import sys
import RPi.GPIO as gpio
import time

# m1 - OY
# m2 - OX
OXmaxSteps = 600
OYmaxSteps = 850
OXSteps = 0
OYSteps = 0

engrTime = 0.2
idleTime = 0.004

m1StepPin = 17
m1DirPin = 27
#m1StepPin = 1
#m1DirPin = 2
m2StepPin = 24
m2DirPin = 23

laserOnOffPin = 1
atxOnOffPin = 16

#silnik 1
gpio.setmode(gpio.BCM)
gpio.setup(m1DirPin, gpio.OUT)
gpio.setup(m1StepPin, gpio.OUT)
#silnik 2
gpio.setup(m2DirPin, gpio.OUT)
gpio.setup(m2StepPin, gpio.OUT)
#przekaźnik lasera
gpio.setup(laserOnOffPin, gpio.OUT)
#gpio.output(laserOnOffPin, True)
#przekaźnik zasilania
gpio.setup(atxOnOffPin, gpio.OUT)

#Funkcja rozdziela linię zawierającą ciąg instrukcji na listę pojedynczych operacji
#text - linia postaci "0 0 0 0 0 0" lub "end" lub "new"
def split_line(text):
	instructions = text.split()
	return instructions

def predict_time(line):
	etime = 0
	itime = 0
	for op in line:
		if (op == "1" or op == "3"):
			etime += 4*engrTime
		else:
		 	itime += 4*idleTime 
	return [etime, itime]

total = len(sys.argv)
cmdargs = str(sys.argv)
if total > 1:
	fileName = str(sys.argv[1])
else:
	fileName = "gcode.txt"
print "Graweruje ", fileName, "total: ", total 
#plik z instrukcjami dla grawera
pt = 0
et = 0
it = 0
with open(fileName, 'r+') as f:
	lst = []
	for line in f:
		l = split_line(line)
		[e, i] = predict_time(l)
		et+=e
		it+=i
		lst.append(l)
		
f.closed

et += (et/90)*30
pt = et + it
pt *= 1.222
print "Szacowany czas grawerowania: ", pt, "s (", pt/60, "m)\n"

#Oznaczenia kodów cyfrowych
#0 - ruch w prawo bez grawerowania
#1 - ruch w prawo z grawerowaniem
#2 - ruch w lewo bez grawerowania
#3 - ruch w lewo z grawerowaniem
#4 - ruch w dół bez grawerowania
#5 - ruch w górę bez grawerowania
#new - plik nieprzetworzony
#END - koniec pracy

try:
	gpio.output(atxOnOffPin, False)
	print "Zasilanie włączone"
	t = time.time()
	for elt in lst:

		if time.time()>t+110:
			#wyłącz laser
			gpio.output(laserOnOffPin, True)
			time.sleep(30)
			t = time.time()
			#włącz laser
			gpio.output(laserOnOffPin, False)
		for instr in elt:
			#obsługa ruchu lewo-prawo
			if (instr == "0" and OYSteps < OYmaxSteps):
				gpio.output(m1DirPin, True)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(idleTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(idleTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(idleTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				OYSteps += 1
				time.sleep(idleTime)
			elif (instr == "1" and OYSteps < OYmaxSteps):
				#włącz laser
				gpio.output(laserOnOffPin, False)
				#wykonaj krok
				gpio.output(m1DirPin, True)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(engrTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(engrTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(engrTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				#wyłącz laser
				gpio.output(laserOnOffPin, True)
				OYSteps += 4
				time.sleep(engrTime)
			elif (instr == "2" and OYSteps < OYmaxSteps):
				#wykonaj krok
				gpio.output(m1DirPin, False)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(idleTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(idleTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(idleTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				OYSteps -= 1
				time.sleep(idleTime)
			elif (instr == "3" and OYSteps < OYmaxSteps):
				#włącz laser
				gpio.output(laserOnOffPin, True)
				#wykonaj krok
				gpio.output(m1DirPin, False)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(engrTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(engrTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				time.sleep(engrTime)
				gpio.output(m1StepPin, True)
				gpio.output(m1StepPin, False)
				#wyłącz laser
				gpio.output(laserOnOffPin, False)
				OYSteps -= 4
				time.sleep(engrTime)
			#obsługa ruchu góra-dół
			elif (instr == "4" and OXSteps < OXmaxSteps):
				#wykonaj krok
				gpio.output(m2DirPin, True)
				gpio.output(m2StepPin, True)
				gpio.output(m2StepPin, False)
				time.sleep(idleTime)
				gpio.output(m2StepPin, True)
				gpio.output(m2StepPin, False)
				time.sleep(idleTime)
				gpio.output(m2StepPin, True)
				gpio.output(m2StepPin, False)
				time.sleep(idleTime)
				gpio.output(m2StepPin, True)
				gpio.output(m2StepPin, False)
				OXSteps += 4
				time.sleep(idleTime)
			elif (instr == "5" and OXSteps < OXmaxSteps):
				#wykonaj krok
				gpio.output(m2DirPin, False)
				gpio.output(m2StepPin, True)
				gpio.output(m2StepPin, False)
				gpio.output(m2StepPin, True)
				gpio.output(m2StepPin, False)
				OXSteps -= 2
				time.sleep(idleTime)
			else:
				print "command"

	print "X: ",  OXSteps, "\nY: ", OYSteps
	print "Program zakonczyl dzialanie\n"
	gpio.output(atxOnOffPin, True)
	print "Zasilanie wyłączone"
except KeyboardInterrupt:
	print "\n\nKeyboard interrupt.\n"
	print "Anulowano pracę\n"
	gpio.output(atxOnOffPin, True)
	print "Zasilanie wyłączone - przerwanie"
except:  
	print "Other error or exception occurred!"  
finally:
	gpio.cleanup()

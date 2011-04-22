# Bryant Haley
# Alexander Pfeiffenberger
# Spring 2011

# Timescale
intTime = 0 # SSsss
time = 0 # 0x0000
ptime = 0 # Time previous message was received
minutes = 0 # Minute counter

# This buffer is used to account for roll-overs
timeBuffer = 40000 
# The counter increments once per mS
# and rolls over at 0xEA5F (59999mS)
#
# Format MMM SS.sss
# 
# M = Minutes
# S = Seconds
# s = miliseconds
#

# Open input and output files
fileR = open("04_10_2011_13_40.txt","r")
fileW = open("output.dat", "w")

# Write File Header
line = "Time Pedal ERPM Ibat\n"
fileW.write(line)

# Screen and File output formatting
# Pedal is shown as a DEC
# Erpm is shown as a scaled DEC
# iBat is shown as a DEC (Discharge -, Charge +)

def printAndWrite():
	divTime = float(intTime)/1000
	print '%03d' % minutes+" "+'%02.3f' % divTime+" "+str(pedal)+" "+str(Erpm)+" "+str(iBat)
	line = '%03d' % minutes+" "+'%02.3f' % divTime+" "+str(pedal)+" "+str(Erpm)+" "+str(iBat)+"\n"
	fileW.write(line)
	return

# Functional Variables
count = 0

while(1):
	nextChar = fileR.read(1)

	## Reset data for each loop
	tach = 0 # Bolt pulses per 500ms period
	Erpm = 0 # = 60*(tach*2)
	pedal = 0 # Position 0% to 100%
	iBat = 0 # Current wrt batteries

	# Received CAN frames begin with t
	if(nextChar == "t"):
		ptime = intTime # intTime will be overwritten. Store value now
		ID = fileR.read(3) # Every message has an 11bit ID stored in three characters

		if(ID == "0E0"): # Electric Motor Tachometer
			### Skips the length bit, for now, this info can be used later to handle all the data
			nextChar = fileR.read(1)
			tach = fileR.read(2)
			tach = int(tach, 16)
			Erpm = (tach*2)*60
			nextChar = fileR.read(2)
			time = fileR.read(4)
			intTime = int(time,16)
			if (intTime+timeBuffer < ptime):
				minutes = minutes+1
			printAndWrite()

		elif(ID == "0A0"): # Accelerator Pedal
			### Skips the length bit
			nextChar = fileR.read(1)
			pedal = fileR.read(2)
			pedal = int(pedal, 16)
			time = fileR.read(4)
			intTime = int(time,16)
			if (intTime+timeBuffer < ptime):
				minutes = minutes+1
			printAndWrite()

		elif(ID == "0C1"): # BMS
			### Skips the length bit
			nextChar = fileR.read(3)
			LS = fileR.read(2) # Least sig. bits
			MS = fileR.read(2) # Most sig. bits
			temp = MS + LS
			iBat = int(temp, 16)
			iBat = iBat - 32768
			### Skips the other data 
			nextChar = fileR.read(10)
			time = fileR.read(4)
			intTime = int(time,16)
			if (intTime+timeBuffer < ptime):
				minutes = minutes+1
			printAndWrite()
### CLOSE TEXT
fileR.close()
fileW.close()

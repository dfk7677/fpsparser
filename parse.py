#!/usr/bin/env python
import numpy as np
import sys, argparse

def result(date, fr, ft, framenum):
	print("Date: " + date)
	print("Total frames: " + str(framenum))

	print("Framerates:")
	print("Average (FpS): " + str(round(np.average(fr),1)))
	print("Median (FpS): " + str(round(np.median(fr),1)))
	print("1% Low  (FpS): " + str(round(np.percentile(fr, 1),1)))
	print("Standard deviation (FpS): " + str(round(np.std(fr),1)))

	if len(ft) > 0:
		print("Frametimes:")
		print("Average (ms): " + str(round(np.average(ft),1)))
		print("Median (ms): " + str(round(np.median(ft),1)))
		print("1% High  (ms): " + str(round(np.percentile(ft, 99),1)))
		print("Standard deviation (ms): " + str(round(np.std(ft),1)))


parser = argparse.ArgumentParser(description='Parse an MSI Afterburner monitoring log file.')
parser.add_argument('-i', metavar='<inputfile>', help='Log filename', required=True)
parser.add_argument('--frametime', help='Parse frametime', action="store_true")

data = []
index = []

args = parser.parse_args()

framerates = []
frametimes = []
index = [0, 0]
log = open(args.i, "r", encoding="ISO-8859-1")

frames = 0
for line in log:
	temp = line.split(',')
	fields = list(map(str.strip, temp))
	
	if fields[0] == '00':
		if fields[2] != "Hardware monitoring log v1.5":
			print("Incompatible MSI Afterburner version")
			sys.exit(2)
		if frames > 1000:
			result(fields[1], data, frames)
		elif frames > 0:
			print('Not enough data')
		frames = 0
		
	elif fields[0] == '01':
		if frames > 1000:
			print("GPU:" + fields[2])
	elif fields[0] == '02':
		if 'Framerate' in fields:
			index[0] = fields.index("Framerate")
			framerates = []
		else:
			print("The logfile must contain framerates")
			sys.exit(2)
		if 'Frametime' in fields and args.frametime:
			index[1] = fields.index("Frametime")
			frametimes = []
	elif fields[0] == '80':		
		if fields[index[0]] != 'N/A' and fields[index[0]] != '0.000':
			frames += 1
			framerate = float(fields[index[0]])				
			framerates.append(framerate)
			if args.frametime:					
				frametime = float(fields[index[1]])				
				frametimes.append(frametime)

		
if frames > 1000:
	result(fields[1], framerates, frametimes, frames)
log.close()




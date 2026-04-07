#!/usr/bin/env python
import numpy as np
from scipy.io import wavfile
import random
import sys
import argparse

# parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--string", "-s", nargs='?', default="")
parser.add_argument("--file", "-f", nargs='?', default="")
args = parser.parse_args()


######## CONFIG / constants ########

markBitFrequency = 2200
markBitPhase = 0
markBitAmplitude = 1
markBitTime = 1.0 / (1200)
spaceBitFrequency = 2200
spaceBitPhase = 180
spaceBitAmplitude = 1
spaceBitTime = 1.0 / (1200)

# NOTE: the bit times may not align with the frequency, make sure to check

sampleRate = 48000 # sample rate

print (args)

# t = 1.0 / (520 + (5/6))


# f = 2083.33333
	
samples = np.zeros(0)

def markBit():
	# f = 2083.33333
	f = markBitFrequency
	t = markBitTime
	p = markBitPhase*np.pi/180
	samples = np.arange(t * sampleRate) / sampleRate

	return np.sin(2 * np.pi * f * samples - p) * markBitAmplitude

def spaceBit():
	# f = 1562.5
	f = spaceBitFrequency
	t = spaceBitTime
	p = spaceBitPhase*np.pi/180

	samples = np.arange(t * sampleRate) / sampleRate

	return np.sin(2 * np.pi * f * samples - p) * spaceBitAmplitude

def byte(inByte):
	sys.stdout.write(chr(inByte))
	sys.stdout.write(" ")
	byte_data = np.zeros(0)
	for i in range(0, 8):
		if inByte >> i & 1:
			sys.stdout.write("1")
			byte_data = np.append(byte_data, markBit())
		else:
			sys.stdout.write("0")
			byte_data = np.append(byte_data, spaceBit())

	sys.stdout.write("\n")
	sys.stdout.flush()

	return byte_data

if args.string:
    data = args.string.encode("utf-8")
elif args.file:
	with open(args.file, "rb") as file:
		data = file.read()

signal = np.zeros(0)

for octet in data:
	signal = np.append(signal, byte(octet))

signal *= 32767

signal = np.int16(signal)

wavfile.write(str("encoded.wav"), sampleRate, signal)

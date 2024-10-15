import numpy as np
import pygame
import math
import time


pygame.mixer.init(44100,-16,2,512)
pygame.mixer.set_num_channels(24)
# sampling frequency, size, channels, buffer

# Sampling frequency
# Analog audio is recorded by sampling it 44,100 times per second, 
# and then these samples are used to reconstruct the audio signal 
# when playing it back.

# size
# The size argument represents how many bits are used for each 
# audio sample. If the value is negative then signed sample 
# values will be used.

# channels
# 1 = mono, 2 = stereo

# buffer
# The buffer argument controls the number of internal samples 
# used in the sound mixer. It can be lowered to reduce latency, 
# but sound dropout may occur. It can be raised to larger values
# to ensure playback never skips, but it will impose latency on sound playback.

class Tone(object):
	"""
	Plays a tone comprised of all frequencies and durations

	:freqs:		list of float frequency values
	:durations:	list of float duration values
	"""
	sampleRate = 44100	# [Hz]
	freqs = [] 			# [Hz]
	duration = 1 		# [seconds] 
	tempo = 107//2			# in bpm; goes as low as 60 bpm

	def __init__(self, freqs: list[int], durations: list[int]):
		self.durations = durations
		self.freqs = freqs
		self.sounds = []
		for i in range(len(self.freqs)):
			sineWave = np.array([4096 * np.sin(2.0 * np.pi * self.freqs[i] * x / self.sampleRate) for x in range(0, int(self.sampleRate*self.durations[i]*(113/60)*(60/Tone.tempo)))]).astype(np.int16)
			stereoSineWave = np.c_[sineWave,sineWave]
			self.sounds.append(pygame.mixer.Sound(stereoSineWave))

	def playTone(self) -> None:
		startTime = time.time()
		numSounds = len(self.sounds)
		for num in range(numSounds):
			pygame.mixer.Channel(num).play(self.sounds[num])

		# cycle around through channels and check if note has passed its duration
		channelNum = 0
		while pygame.mixer.get_busy():
			currTime = time.time()
			if (currTime - startTime) >= self.durations[channelNum]*(113/60)*(60/Tone.tempo):
				pygame.mixer.Channel(channelNum).fadeout(50)
			channelNum += 1
			channelNum %= numSounds


AFreq = 440
exponent = -4
pitchClasses = {}
# no flats/sharps between BC and EF
keys = ['A', ('A#','Bb'), 'B', 'C', ('C#','Db'), 'D', ('D#','Eb'), 'E', 'F', ('F#','Gb'), 'G', ('G#','Ab')]
while AFreq*math.pow(2,exponent) < 20000:
    freqA = AFreq*math.pow(2,exponent)
    for num in range(12):
        octave = 4+exponent
        if type(keys[num]) == type((0,)):
            if keys[num][0] >= 'C':
                octave += 1
            pitchClasses.update({keys[num][0]+str(octave) : freqA*math.pow(2, num/12)})
            pitchClasses.update({keys[num][1]+str(octave) : freqA*math.pow(2, num/12)})
        else:
            if keys[num] >= 'C':
                octave += 1
            pitchClasses.update({keys[num]+str(octave) : freqA*math.pow(2, num/12)})
    exponent += 1
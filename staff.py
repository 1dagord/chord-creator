from settings import *
from clef import Clef
from note import Note
import pygame as pg
import mode


class Staff(object):
	lines = [0,0,0,0,0]			# y-coordinate of lines from bottom to top
	spaces = [0,0,0,0]			# y-coordinate of spaces from bottom to top
	notes = []					# stores notes placed on Staff
	timeSignature = [0,0]		# top: number of beats per measure, bottom: inverse duration of each beat
	ledgerLines = []			# list of list of coordinates of left and right points of ledger lines attached to Staff
	numberOfMeasures = 4
	clef = None					# Clef attached to Staff
	staffId = 0

	def __init__(self,
				 tl: list[int, int],
				 br: list[int, int],
				 timeSig=[4,4],
				 clefName="treble"):
		self.topLeft = tl
		self.bottomRight = br
		self.timeSignature = timeSig
		self.staffId = Staff.staffId
		self.clef = Clef(self, clefName)
		self.isFull = False
		Staff.staffId += 1

	def __str__(self):
		noteGroups = []
		for group in self.notes:
			if len(group) == 1:
				noteGroups.append(str(group[0]))
			else:
				noteGroups.append([])
				for note in group:
					noteGroups[-1].append(str(note))
		return "Staff " + str(self.staffId) + " with " + mode.getActive() + " containing Notes " + str(noteGroups)

	def drawStaff(self) -> None:
		"""
		Draws staff and spaces lines evenly based on
		top-left and bottom-right corners
		"""
		xCoords = [self.topLeft[0], self.bottomRight[0]]
		yCoords = [self.topLeft[1], self.bottomRight[1]]
		lineSpace = (yCoords[1]-yCoords[0])/5
		for n in range(5):
			pg.draw.line(screen, (0,0,0), [xCoords[0], yCoords[0]], [xCoords[1], yCoords[0]], width=2)
			self.lines[n] = yCoords[0]
			if n < 4:
				self.spaces[n] = yCoords[0] + lineSpace/2
			yCoords[0] += lineSpace

		# ----- TIME SIGNATURE DEPENDENT BELOW -----
		"""
		lineLoc = 220
		measureSpace = (self.timeSignature[0]/self.timeSignature[1])*(self.bottomRight[0]-self.topLeft[0]-200)//self.timeSignature[1]
		while lineLoc < self.bottomRight[0]:
			pg.draw.line(screen, (0,0,0), [lineLoc, self.topLeft[1]], [lineLoc, (self.bottomRight[1]-lineSpace)], width=2)
			lineLoc += measureSpace
		"""

		for x in range(self.numberOfMeasures):
			measureSpace = (self.bottomRight[0]-self.topLeft[0]-200)//(self.numberOfMeasures)
			pg.draw.line(screen, (0,0,0), [220+x*measureSpace, self.topLeft[1]], [220+x*measureSpace, (self.bottomRight[1]-lineSpace)], width=2)

		for lineGroup in self.ledgerLines:
			for line in lineGroup:
				pg.draw.line(screen, (0,0,0), line[0], line[1], width=2)


	def writeTimeSignature(self) -> None:
		"""
		Write time signature of current Staff object on staff
		"""
		yCoords = [self.topLeft[1], self.bottomRight[1]]
		lineSpace = (yCoords[1]-yCoords[0])/5
		font = pg.font.SysFont("devanagarimt", int(3*lineSpace), pg.font.Font.bold)
		topText = font.render(str(self.timeSignature[0]), True, (0,0,0))
		bottomText = font.render(str(self.timeSignature[1]), True, (0,0,0))
		topTextRect = topText.get_rect()
		topTextRect.center = (self.topLeft[0]+100, self.topLeft[1]+1.5*lineSpace)
		bottomTextRect = topText.get_rect()
		bottomTextRect.center = (self.topLeft[0]+100, self.topLeft[1]+3.5*lineSpace)
		screen.blit(topText, topTextRect)
		screen.blit(bottomText, bottomTextRect)

	def addNote(self, dur: str, k: str, oc: int, acc="natural", aMode=None) -> None:
		"""
		Add Note to Staff based on attached Clef

		:dur:	duration of note
		:k:		pitch class of note
		:oc:	octave of note
		:acc:	accidental of note
		:aMode:	mode of the GUI ("Create" or "Place")
		"""
		noteSpace = (self.bottomRight[1]-self.topLeft[1])/5 		# 3.5 note spaces between octaves (3/4 lines and 4/3 spaces)
		octaveSpace = 3.5*noteSpace

		# interleaves y-positions of lines and staffs
		staffPositions = sum(zip(self.lines, self.spaces+[0]), ())[:-1]
		
		# pitchToStaff Format: [down-shift, no shift, up-shift]
		pitchToStaff = {}
		noteToPos = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
		bottomNote = 'e'

		if self.clef.name == "bass":
			bottomNote = 'g'
		elif self.clef.name in ["alto", "tenor", "soprano"]:
			bottomNote = 'f'
			if self.clef.name == "tenor":
				bottomNote = 'd'
			elif self.clef.name == "soprano":
				bottomNote = 'c'

		pitchToStaff.update({noteToPos[(ord(bottomNote)-ord('a'))%7]:[staffPositions[8]+octaveSpace, staffPositions[8], staffPositions[1]]})
		pitchToStaff.update({noteToPos[(ord(bottomNote)-ord('a')+1)%7]:[staffPositions[7]+octaveSpace, staffPositions[7], staffPositions[0]]})
		pitchToStaff.update({noteToPos[(ord(bottomNote)-ord('a')+2)%7]:[staffPositions[6]+octaveSpace, staffPositions[6], staffPositions[6]-octaveSpace]})
		pitchToStaff.update({noteToPos[(ord(bottomNote)-ord('a')+3)%7]:[staffPositions[5]+octaveSpace, staffPositions[5], staffPositions[5]-octaveSpace]})
		pitchToStaff.update({noteToPos[(ord(bottomNote)-ord('a')+4)%7]:[staffPositions[4]+octaveSpace, staffPositions[4], staffPositions[4]-octaveSpace]})
		pitchToStaff.update({noteToPos[(ord(bottomNote)-ord('a')+5)%7]:[staffPositions[3]+octaveSpace, staffPositions[3], staffPositions[3]-octaveSpace]})
		pitchToStaff.update({noteToPos[(ord(bottomNote)-ord('a')+6)%7]:[staffPositions[2]+octaveSpace, staffPositions[2], staffPositions[2]-octaveSpace]})

		n = Note(self, duration=dur, key=k, octave=oc, accidental=acc)
		n.addMode = aMode or mode.active

		noteOffset = 185

		if len(self.notes) == 0:
			n.position = [self.topLeft[0]+noteOffset, pitchToStaff[k][n.octave-self.clef.octave+1]]	
		else:
			lastNote = self.notes[-1][-1]
			staffHeight = self.bottomRight[1] - self.topLeft[1]

			noteXPos = lastNote.trailingSpace
			if n.addMode == mode.createMode:
				noteXPos = 0

				# if next note will run over width of staff ...
			if lastNote.position[0]+noteXPos+30 > self.bottomRight[0]:
				self.isFull = True
				return
			else:
				n.position = [lastNote.position[0]+noteXPos, pitchToStaff[k][n.octave-self.clef.octave+1]]	

		# increase octave at C instead of upward shifted bottom note
		if (k >= 'c' and ord(k) < ord(bottomNote)):
			n.octave += 1

		# adds ledger lines if necessary
		if n.position[1] < self.topLeft[1]:
			n.hasLedgerLine = True
			lineY = self.topLeft[1]
			lineGroup = []
			while lineY >= n.position[1]:
				lineGroup.append([[n.position[0]-25, lineY], [n.position[0]+25, lineY]])
				lineY -= noteSpace
			self.ledgerLines.append(lineGroup)
		elif n.position[1] >= self.bottomRight[1]:
			n.hasLedgerLine = True
			lineY = self.bottomRight[1]
			lineGroup = []
			while lineY <= n.position[1]:
				lineGroup.append([[n.position[0]-25, lineY], [n.position[0]+25, lineY]])
				lineY += noteSpace
			self.ledgerLines.append(lineGroup)

		# ensures no duplicate Notes get added during Create Mode
		if self.notes and n.addMode == mode.createMode:
			if (lastNote.duration, lastNote.key, lastNote.octave) != (n.duration, n.key, n.octave):
				self.notes[-1].append(n)
				n.drawNote(n.position)
			return

		for lineGroup in self.ledgerLines:
			for line in lineGroup:
				pg.display.update(pg.draw.line(screen, (0,0,0), line[0], line[1], width=2))

		self.notes.append([n])
		n.drawNote(n.position)


		
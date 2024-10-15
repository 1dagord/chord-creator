from settings import *
import pygame as pg

class Clef(object):
	name = ""			# name of Clef
	octave = 0			# octave of base note in Clef
	pitch = ""			# pitch class of base note
	position = [0,0]	# position of base note
	sheet = None

	# [name of clef] : [[key of base note], [octave of note on lowest line]]
	clefOptions = {"treble":['g', 4], "soprano":['c', 4], "alto":['c', 3], "tenor":['c', 3], "bass":['f', 2]}

	def __init__(self, sheet, name: str, position=[0,0]):
		Clef.sheet = sheet
		self.name = name
		self.position = position
		self.pitch = Clef.clefOptions[name][0]
		self.octave = Clef.clefOptions[name][1]

	def __str__(self):
		return self.name.title() + " Clef on Staff " + str(self.sheet.staffId)

	def changeClef(self, name: str) -> None:
		"""
		On Clef click, cycle between clefs and redraw staff
		"""
		oldClef = self.sheet.clef
		if name == oldClef.name:
			return
		self.sheet.clef = Clef(self.sheet, name)

		initScreen()

		previousNotes = [note for noteGroup in self.sheet.notes for note in noteGroup]
		self.sheet.notes.clear()
		self.sheet.ledgerLines.clear()
		self.sheet.drawStaff()

		bottomNotes = {"treble":"e4", "bass":"g2", "alto":"f3", "tenor":"d3", "soprano":"c4"}

		clefMax = {"treble"  : ["e3", "d6"],
		           "soprano" : ["c3", "b5"],
		           "alto"    : ["f2", "e5"],
		           "tenor"   : ["d2", "c5"],
		           "bass"    : ["g1", "f4"]}

		clefOverlaps = {("treble", "soprano"):  ("e3", "a5"),
						("treble", "alto"):  ("e3", "d5"),
						("treble", "tenor"):  ("e3", "b4"),
						("treble", "bass"):  ("e3", "e4"),
						("soprano", "alto"):  ("c3", "d5"),
						("soprano", "tenor"):  ("c3", "b4"),
						("soprano", "bass"):  ("c3", "e4"),
						("alto", "tenor"):  ("f2", "c5"),
						("alto", "bass"):  ("f2", "e4"),
						("tenor", "bass"):  ("d2", "e4")}

		newClef = self.sheet.clef
		allShift = 0
		allNotes = list(toneGen.pitchClasses)
		safeRange = None

		try:
			safeRange = clefOverlaps[(oldClef.name, newClef.name)]
		except KeyError:
			safeRange = clefOverlaps[(newClef.name, oldClef.name)]
		finally:
			# lowest and highest notes placed on staff
			highestNote = allNotes[0]
			lowestNote = allNotes[-1]
			for note in previousNotes:
				if allNotes.index(note.key.upper()+str(note.octave)) < allNotes.index(lowestNote):
					lowestNote = note.key.upper()+str(note.octave)
				if allNotes.index(note.key.upper()+str(note.octave)) > allNotes.index(highestNote):
					highestNote = note.key.upper()+str(note.octave)

				isAboveLow = allNotes.index(note.key.upper()+str(note.octave)) >= allNotes.index(safeRange[0].upper())
				isBelowHigh = allNotes.index(note.key.upper()+str(note.octave)) <= allNotes.index(safeRange[1].upper())
				if isAboveLow and isBelowHigh:
					continue
				else:
					# shift by octave difference if nonzero, note to safe range difference otherwise
					if not isAboveLow:
						allShift = 1
					if not isBelowHigh:
						allShift = -1
					break

			# check if all notes in range after allShift, remove if not
			if allShift:
				toBeRemoved = []
				minNote = clefMax[newClef.name][0].upper()
				maxNote = clefMax[newClef.name][1].upper()
				if not isAboveLow:
					while allNotes.index(lowestNote) <= allNotes.index(minNote):
						lowestNote = lowestNote[0]+str(int(lowestNote[1])+1)
						allShift += 1
				elif not isBelowHigh:
					while allNotes.index(highestNote) >= allNotes.index(maxNote):
						highestNote = highestNote[0]+str(int(highestNote[1])-1)
						allShift -= 1

				allShift -= allShift//abs(allShift)

				for i in range(len(previousNotes)):
					note = previousNotes[i]
					shiftedNote = note.key.upper()+str(note.octave+allShift)

					# check if notes fit on staff with allShift
					if (allNotes.index(shiftedNote) >= allNotes.index(minNote)) and (allNotes.index(shiftedNote) <= allNotes.index(maxNote)):
						continue
					else:
						toBeRemoved.append(i)
				for i in toBeRemoved[::-1]:
					previousNotes.pop(i)

		for note in previousNotes:
			if allShift:
				note.octave += allShift
			if (note.key >= 'c' and ord(note.key) < ord(bottomNotes[self.sheet.clef.name][0])):
				note.octave -= 1
			self.sheet.addNote(note.duration, note.key, note.octave, note.accidental, note.addMode)

		del self


	def drawClef(self) -> None:
		rootLine = 0
		clefXCoord = (self.sheet.topLeft[0]+50)
		lineSpace = (self.sheet.bottomRight[1] - self.sheet.topLeft[1])/5

		if self.name == "treble":
			rootLine = self.sheet.lines[3]
			bottomLoopBoundingBox = (clefXCoord-20, rootLine-lineSpace, 40, 2*lineSpace)
			bigCurveBoundingBox = (clefXCoord-35, rootLine-2*lineSpace, 70, 3*lineSpace)
			smallCurveBoundingBox = (clefXCoord-12, rootLine-4*lineSpace+13, lineSpace, 1.6*lineSpace)
			endCurveBoundingBox = (clefXCoord-25, rootLine+0.6*lineSpace, 30, 1.5*lineSpace)
			pg.draw.arc(screen, (0,0,0), bottomLoopBoundingBox, -1.6, 3.3, width=7)
			pg.draw.arc(screen, (0,0,0), bigCurveBoundingBox, 1.6, 4.7, width=6)
			pg.draw.arc(screen, (0,0,0), smallCurveBoundingBox, -1.3, 2.6, width=5)
			pg.draw.line(screen, (0,0,0), (clefXCoord-9, rootLine-3*lineSpace), (clefXCoord, rootLine+1.7*lineSpace), width=5)
			pg.draw.arc(screen, (0,0,0), endCurveBoundingBox, 3.6, 5.6, width=6)
		elif self.name == "bass":
			rootLine = self.sheet.lines[1]
			pg.draw.circle(screen, (0,0,0), (clefXCoord, rootLine-lineSpace/2), 5)
			pg.draw.circle(screen, (0,0,0), (clefXCoord, rootLine+lineSpace/2), 5)
			pg.draw.arc(screen, (0,0,0), (clefXCoord-50, rootLine-lineSpace, 45, lineSpace*2), -0.5, 2.9, width=6)
			pg.draw.line(screen, (0,0,0), (clefXCoord-10, rootLine+5), (clefXCoord-30, rootLine+2*lineSpace), width=6)
		elif self.name in ["alto", "tenor", "soprano"]:
			rootLine = self.sheet.lines[2]
			if self.name == "tenor":
				rootLine = self.sheet.lines[1]
			elif self.name == "soprano":
				rootLine = self.sheet.lines[4]
				
			pg.draw.line(screen, (0,0,0), (clefXCoord-50, rootLine-2*lineSpace), (clefXCoord-50, rootLine+2*lineSpace), width=8)
			pg.draw.line(screen, (0,0,0), (clefXCoord-40, rootLine-2*lineSpace), (clefXCoord-40, rootLine+2*lineSpace), width=2)
			pg.draw.arc(screen, (0,0,0), (clefXCoord-40, rootLine-2*lineSpace, 30, 2*lineSpace-5), -2.1, 2.1, width=6)
			pg.draw.arc(screen, (0,0,0), (clefXCoord-40, rootLine+7, 30, 2*lineSpace-5), -2.1, 2.1, width=6)
			pg.draw.arc(screen, (0,0,0), (clefXCoord-48, rootLine-2*lineSpace, 20, 2*lineSpace), 4.7, 5.8, width=5)
			pg.draw.arc(screen, (0,0,0), (clefXCoord-48, rootLine, 20, 2*lineSpace), 0.5, 1.6, width=5)


			
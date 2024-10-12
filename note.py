from settings import *
import pygame as pg
import mode


class Note(object):

	accidentals = {"flat" : 0, "natural" : 1, "sharp" : 2}

	def __init__(self, sheet, duration: str, key: str, octave: int, position=None, accidental="natural", addMode=None):
		self.sheet = sheet
		self.duration = duration
		self.key = key
		self.octave = octave
		self.position = position or [0,0]
		self.accidental = accidental
		self.hasLedgerLine = False
		self.addMode = addMode or mode.active
		if self.sheet:
			# ----- TIME SIGNATURE DEPENDENT BELOW -----
			# self.trailingSpace = (durationMultiplier[self.duration]*((self.sheet.timeSignature[0]/self.sheet.timeSignature[1])*(self.sheet.bottomRight[0]-self.sheet.topLeft[0]-200)//self.sheet.timeSignature[1]))
			self.trailingSpace = (self.sheet.timeSignature[1]/self.sheet.timeSignature[0])*(durationMultiplier[self.duration]*(self.sheet.bottomRight[0]-self.sheet.topLeft[0]-200))/(self.sheet.numberOfMeasures)

	def __str__(self):
		accSymbols = {0 : "b", 1 : "", 2 : "#"}
		return self.key.upper() + str(accSymbols[Note.accidentals[self.accidental]]) + str(self.octave) + " " + self.duration.title() + " Note"

	def drawNote(self, pos: list, color=(0,0,0)) -> None:
		"""
		Draws Note centered at position given and
		updates Note's position
		PROBLEM: 64th note does not print for A and C
				 16th note does not print for D
				(Note Duration Problem)
		"""
		self.position = pos
		blackBoundingBox = (pos[0]-15, pos[1]-10, 30, 20)
		whiteBoundingBox = (pos[0]-6, pos[1]-9, 12, 18)
		staffCenter = (self.sheet.bottomRight[1] + self.sheet.topLeft[1])//2
		staffYDim = self.sheet.bottomRight[1] - self.sheet.topLeft[1]

		pg.draw.ellipse(bgLayer, color, (blackBoundingBox))																				# base note shape
		if self.duration in ["w", "whole", "h", "half"]:																					# if note has hole
			pg.draw.ellipse(fgLayer, (255,255,255), (whiteBoundingBox))
			if pos[1] in self.sheet.lines: 
				pg.draw.line(fgLayer, color, (pos[0]-10, pos[1]), (pos[0]+10, pos[1]), width=2)
		if self.duration in ["h", "half", "q", "quarter", "e", "eighth", "s", "sixteenth", "ts", "thirty-second", "sf", "sixty-fourth"]:	# if notes require stem
			if (pos[1] < staffCenter):
				pg.draw.line(bgLayer, color, (pos[0]-14, pos[1]), (pos[0]-14, pos[1]+0.45*staffYDim), width=3)
			else:
				pg.draw.line(bgLayer, color, (pos[0]+14, pos[1]), (pos[0]+14, pos[1]-0.45*staffYDim), width=3)
		if self.duration in ["e", "eighth", "s", "sixteenth", "ts", "thirty-second", "sf", "sixty-fourth"]:									# if notes require flag(s)
			if self.duration in ["e", "eighth"]:
				numStems = 1
			elif self.duration in ["s", "sixteenth"]:
				numStems = 2
			elif self.duration in ["ts", "thirty-second"]:
				numStems = 3
			elif self.duration in ["sf", "sixty-fourth"]:
				numStems = 4

			deltaY = 0
			for _ in range(numStems):
				if (pos[1] < staffCenter):
					stemBoundingBox = (pos[0]-30, pos[1]+0.05*staffYDim-deltaY, 33, 0.4*staffYDim)
					pg.draw.arc(bgLayer, (0,0,0), stemBoundingBox, 4.7, 6.4, width=3)
				else:
					stemBoundingBox = (pos[0], pos[1]-0.45*staffYDim+deltaY, 33, 0.6*staffYDim)
					pg.draw.arc(bgLayer, color, stemBoundingBox, -0.05, 1.7, width=3)
				deltaY += 10

		if self.accidental == "flat":
			flatLoopBoundingBox = (pos[0]-40, pos[1]-7, 20, 18)
			pg.draw.line(bgLayer, color, [pos[0]-30, pos[1]-30], [pos[0]-30, pos[1]+10], width=3)
			pg.draw.arc(bgLayer, color, flatLoopBoundingBox, -1.6, 1.6, width=3)
		elif self.accidental == "sharp":
			pg.draw.line(bgLayer, color, [pos[0]-28, pos[1]-20], [pos[0]-28, pos[1]+20], width=3)
			pg.draw.line(bgLayer, color, [pos[0]-21, pos[1]-23], [pos[0]-21, pos[1]+17], width=3)
			pg.draw.line(bgLayer, color, [pos[0]-33, pos[1]-4], [pos[0]-18, pos[1]-7], width=5)
			pg.draw.line(bgLayer, color, [pos[0]-33, pos[1]+9], [pos[0]-18, pos[1]+6], width=5)

		pg.display.update(screen.blit(bgLayer, (0,0), special_flags=pg.BLEND_RGBA_MIN))
		pg.display.update(screen.blit(fgLayer, (0,0), special_flags=pg.BLEND_RGBA_MAX))
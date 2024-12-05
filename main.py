from button import Button
from staff import Staff
from settings import *
from clef import Clef
from note import Note
from menu import Menu
import toneGenerator as toneGen
import pygame as pg
import mode


"""
	chordCreator_v1.2.py
	IMPROVEMENTS OVER PREVIOUS VERSIONS:
		- allow changing clefs and note transfer

	TODO:
		| | adjust space between notes across measures when notes in measures begin overlapping
		| | draw/delete ledger lines correctly in Create mode
		| | on note delete, update the screen from last note to right edge of window ONLY
		| | add multiple Staffs on staff overflow
			POSSIBLE SOLUTION:
				variables defined outside constructor are CLASS variables (shared across all instances)
				not INSTANCE variables (contained within one standalone instance)
				Source: https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables

	PROBLEMS:
		- Note Duration Problem
		- ledger lines on first note do not disappear on delete in Create mode
		- note redraw on delete has visible delay with lots of notess
"""

pg.init()
pg.font.init()
pg.display.set_caption("Chord Creator")


staff = Staff([0.05*width, (height//2)-50], [0.95*width, (height//2)+50], clefName="treble", timeSig=[4,4])

buttonXCoords = [(width//2)-(1.5*200)-20+220*x for x in range(3)]
Button(buttonXCoords[0], height-70, 200, 50, "Create Mode", mode.activateCreateMode, staff=staff)
Button(buttonXCoords[1], height-70, 200, 50, "Place Mode", mode.activatePlaceMode, staff=staff)
Button(buttonXCoords[2], height-70, 200, 50, "Play", mode.activatePlayMode, staff=staff)
bWidth = 130
clefXCoords = [(width//2)-(2.5*bWidth)-(30*2.5)+(bWidth+30)*x for x in range(5)]
Button(clefXCoords[0], 10, bWidth, 50, "Treble", Menu.toTreble, "menu", staff)
Button(clefXCoords[1], 10, bWidth, 50, "Soprano", Menu.toSoprano, "menu", staff)
Button(clefXCoords[2], 10, bWidth, 50, "Alto", Menu.toAlto, "menu", staff)
Button(clefXCoords[3], 10, bWidth, 50, "Tenor", Menu.toTenor, "menu", staff)
Button(clefXCoords[4], 10, bWidth, 50, "Bass", Menu.toBass, "menu", staff)


def initScreen() -> None:
	screen.fill("white")
	bgLayer.fill("white")
	fgLayer.fill("black")

	for button in Button.buttonDict:
		button.drawBackground()
		button.activate()

	staff.drawStaff()
	staff.clef.drawClef()
	staff.writeTimeSignature()

	pg.display.flip()


def main() -> None:
	initScreen()

	done = False
	while not done:
		clk = pg.time.Clock()
		clk.tick(60)

		width, height = pg.display.get_surface().get_size()
		lastPopulatedStaff = staff

		for event in pg.event.get():
			if event.type == pg.QUIT:
				print(lastPopulatedStaff)
				done = True

			if event.type == pg.MOUSEBUTTONUP or event.type == pg.MOUSEBUTTONDOWN:
				for button in Button.buttonDict:
					button.activate()
			if event.type == pg.MOUSEMOTION:
				for button in Button.buttonDict:
					button.checkForHover()

			if event.type == pg.KEYDOWN:
				if event.key in majorScale:
					durationShift = 0
					octaveShift = 0
					noteAccidental = "natural"
					keysPressed = pg.key.get_pressed()
					if pg.key.get_mods() & pg.KMOD_LMETA:
						durationShift += 1
					if pg.key.get_mods() & pg.KMOD_LALT:
						durationShift += 2
					if pg.key.get_mods() & pg.KMOD_LCTRL:
						durationShift += 3
					if pg.key.get_mods() & pg.KMOD_LSHIFT:
						octaveShift = -1
					if pg.key.get_mods() & pg.KMOD_RSHIFT:
						octaveShift = 1
					if keysPressed[pg.K_z]:
						noteAccidental = "flat"
					if keysPressed[pg.K_x]:
						noteAccidental = "sharp"
					lastPopulatedStaff.addNote(noteDurations[(1<<durationShift)], majorScale[event.key],
															lastPopulatedStaff.clef.octave+octaveShift,
															noteAccidental)
				if event.key == pg.K_BACKSPACE:
					if lastPopulatedStaff.notes:
						if pg.key.get_mods() & pg.KMOD_SHIFT:
							lastPopulatedStaff.notes.clear()
							lastPopulatedStaff.ledgerLines.clear()
						else:
							if lastPopulatedStaff.ledgerLines:
								if mode.active == mode.createMode:
									lastPopulatedStaff.ledgerLines.remove(lastPopulatedStaff.ledgerLines[-1])
								else:
									for n in lastPopulatedStaff.notes[-1]:
										if n.hasLedgerLine:
											lastPopulatedStaff.ledgerLines.remove(lastPopulatedStaff.ledgerLines[-1])
											break
							lastPopulatedStaff.notes.remove(lastPopulatedStaff.notes[-1])
					initScreen()

					# redraw remaining notes
					for noteGroup in lastPopulatedStaff.notes:
						for note in noteGroup:
							note.drawNote(note.position)

		if mode.active == mode.playMode:
			for noteGroup in lastPopulatedStaff.notes:
					notesList = []
					dursList = [note.duration for note in noteGroup]
					dursList = [durationMultiplier[dur] for dur in dursList] 
					# assigns each note a name and octave
					for note in noteGroup:
						noteName = str(note).split(" ")[0]
						halfSteps = {'B#':'C', 'Cb':'B', 'E#':'F', 'Fb':'E'}
						if noteName[:2] in halfSteps:
							octave = int(noteName[-1])
							if noteName[0] == 'C':
								octave -= 1
							if noteName[0] == 'B':
								octave += 1
							noteName = halfSteps[noteName[:2]] + str(octave)
						notesList.append(toneGen.pitchClasses[noteName])
					tone = toneGen.Tone(notesList, dursList)
					tone.playTone()
			mode.active = mode.placeMode

	pg.quit()

if __name__ == "__main__": main()



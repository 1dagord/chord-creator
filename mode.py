"""
Determines whether multiple Notes can be placed
	Create Mode: mode for creating chords (Notes not placed until Enter key pressed)
	Place Mode: mode for placing Notes/chords (Notes places individually upon creation) *default*
	Play Mode: mode for playing tones for each note placed
"""
createMode = 1 << 1
placeMode = 1 << 2
playMode = 1 << 3
active = placeMode
modes = {createMode : "Create Mode Enabled",
			 placeMode : "Place Mode Enabled",
			 playMode : "Play Mode Enabled"}

def getActive() -> str:
	global createMode, placeMode, playMode, active
	if active:
		return modes[active]
	else:
		return "No Mode Selected"

def getCurrent() -> int:
	return active

def activatePlaceMode() -> None:
	global active, placeMode
	active = placeMode

def activateCreateMode() -> None:
	global active, createMode
	active = createMode

def activatePlayMode() -> None:
	global active, playMode
	active = playMode
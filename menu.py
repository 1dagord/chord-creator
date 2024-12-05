from clef import Clef


class Menu(object):

	def toTreble(clef: Clef):
		clef.changeClef("treble")

	def toSoprano(clef: Clef):
		clef.changeClef("soprano")

	def toAlto(clef: Clef):
		clef.changeClef("alto")

	def toTenor(clef: Clef):
		clef.changeClef("tenor")

	def toBass(clef: Clef):
		clef.changeClef("bass")
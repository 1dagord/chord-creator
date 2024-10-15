from settings import *
import pygame as pg
import mode


class Button(object):
	buttonDict = {}
	fillColors = {
        'normal': '#dddddd',
        'hover': '#666666',
        'pressed': '#333333',
        'selected': '#eb3b3b',
        'selectedHover': '#950505',
        'selectedPressed': '#670707'
    }
	funcToMode = {mode.activateCreateMode : mode.createMode,
				  mode.activatePlaceMode : mode.placeMode,
				  mode.activatePlayMode : mode.playMode, 
				  None: None}

	def __init__(self,
				 left: int,
				 top: int,
				 width: int, 
				 height: int,
				 text="BUTTON",
				 clickFunction=None,
				 buttonType="mode"):
		self.left = left
		self.top = top
		self.buttonWidth = width
		self.buttonHeight = height
		self.clickFunction = clickFunction
		self.buttonType = buttonType
		self.isPressed = False

		self.buttonSurface = pg.Surface((self.buttonWidth, self.buttonHeight))
		self.buttonRect = pg.Rect(self.left, self.top, self.buttonWidth, self.buttonHeight)
		self.buttonMsg = text
		self.buttonText = pg.font.SysFont('Arial', 32).render(text, True, (20, 20, 20))

		self.drawBackground()

		self.buttonDict.update({self: self.buttonText})

	def drawBackground(self) -> None:
		self.buttonBGSurface = pg.Surface((self.buttonWidth, self.buttonHeight))
		self.buttonBGSurface.fill('#222222')
		self.buttonBGRect = pg.Rect(self.left+3, self.top+4, self.buttonWidth, self.buttonHeight)
		pg.display.update(screen.blit(self.buttonBGSurface, self.buttonBGRect))

	def checkForHover(self) -> None:
		mousePos = pg.mouse.get_pos()
		if self.buttonType == "mode":
			if mode.active == Button.funcToMode[self.clickFunction]:
				self.buttonSurface.fill(self.fillColors['selected'])
			else:
				self.buttonSurface.fill(self.fillColors['normal'])
			
			if self.buttonRect.collidepoint(mousePos):
				if mode.active == Button.funcToMode[self.clickFunction]:
					self.buttonSurface.fill(self.fillColors['selectedHover'])
				else:
					self.buttonSurface.fill(self.fillColors['hover'])
		else:
			if self.buttonRect.collidepoint(mousePos):
				self.buttonSurface.fill(self.fillColors['hover'])
			else:
				self.buttonSurface.fill(self.fillColors['normal'])

		pg.display.update(self.buttonSurface.blit(self.buttonText, [self.buttonRect.width/2 - self.buttonText.get_rect().width/2,
												  self.buttonRect.height/2 - self.buttonText.get_rect().height/2]))
		pg.display.update(screen.blit(self.buttonSurface, self.buttonRect))

	def activate(self) -> None:
		mousePos = pg.mouse.get_pos()

		if self.buttonType != "mode":
			self.buttonSurface = pg.Surface([self.buttonWidth, self.buttonHeight])
			self.buttonSurface.fill(self.fillColors['normal'])
			if self.buttonRect.collidepoint(mousePos):
				self.buttonSurface.fill(self.fillColors['hover'])
				if pg.mouse.get_pressed()[0]:
					self.buttonSurface.fill(self.fillColors['pressed'])
					if not self.isPressed:
						self.isPressed = True
						self.clickFunction()
			else:
				if not pg.mouse.get_pressed()[0]:
					self.isPressed = False
		else:
			if mode.active == Button.funcToMode[self.clickFunction]:
				self.buttonSurface.fill(self.fillColors['selected'])
			else:
				self.buttonSurface.fill(self.fillColors['normal'])
			self.buttonBGSurface.fill('#222222')
			if self.buttonRect.collidepoint(mousePos):
				if mode.active == Button.funcToMode[self.clickFunction]:
					self.buttonSurface.fill(self.fillColors['selectedHover'])
				else:
					self.buttonSurface.fill(self.fillColors['hover'])
				if pg.mouse.get_pressed()[0]:
					if mode.active == Button.funcToMode[self.clickFunction]:
						self.buttonSurface.fill(self.fillColors['selectedPressed'])
					else:
						self.buttonSurface.fill(self.fillColors['pressed'])
					if not self.isPressed:
						self.isPressed = True
						if self.clickFunction:
							self.clickFunction()
			if not pg.mouse.get_pressed()[0]:
				self.isPressed = False

		self.buttonSurface.blit(self.buttonText, [self.buttonRect.width/2 - self.buttonText.get_rect().width/2,
													  self.buttonRect.height/2 - self.buttonText.get_rect().height/2])
		
		pg.display.update(screen.blit(self.buttonSurface, self.buttonRect))


		
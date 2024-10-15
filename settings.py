import pygame as pg

width = 1200
height = 600
screen = pg.display.set_mode([width, height])
bgLayer = pg.Surface((width,height))
fgLayer = pg.Surface((width,height))

majorScale = {pg.K_a : 'a', 
			  pg.K_b : 'b',
			  pg.K_c : 'c',
			  pg.K_d : 'd',
			  pg.K_e : 'e',
			  pg.K_f : 'f',
			  pg.K_g : 'g'}

noteDurations = {1 : "whole",
				 2 : "half",
				 4 : "quarter",
				 8 : "eighth",
				 16 : "sixteenth",
				 32 : "thirty-second",
				 64 : "sixty-fourth"}

durationMultiplier = {"whole" : 1,
					  "half" : 0.5,
					  "quarter" : 0.25,
					  "eighth" : 0.125,
					  "sixteenth" : 0.0625,
					  "thirty-second" : 0.03125,
					  "sixty-fourth" : 0.015625}


					  
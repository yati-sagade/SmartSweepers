#!/usr/bin/env python

from controller import Controller
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, MY_NAME
import sys
import pygame

icon = pygame.image.load('resources/icon1.gif')
pygame.display.set_icon(icon)
pygame.display.set_caption(MY_NAME)
scr = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

c = Controller(scr)
gen = c.generations + 1
while 1:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            sys.exit()
    
    c.update()
    c.render()



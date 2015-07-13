#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import fabs
import sys

import numpy
import pygame
from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)
GREY = (133, 133, 133)
WHITE = (255, 255, 255)

SCALE = 20
CELLS_W = 106
CELLS_H = 17
WIDTH = CELLS_W * SCALE
HEIGHT = CELLS_H * SCALE
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
ba = numpy.zeros((CELLS_H, CELLS_W), dtype="int8")

def get_cell(x, y):
    # koordinatenursprung ist unten links
    # und bei pygame rechts oben. deswegen muss
    # die y-koordinate umgerechnet werden
    return (x // SCALE,
            int(fabs((y // SCALE) - CELLS_H + 1)))

def draw_grid():
    # malt zur besseren orientierung ein grid auf das display 
    # vertikale linien
    for i in range(1, CELLS_W):
        pygame.draw.line(DISPLAY, GREY, (i * SCALE, 0), (i * SCALE, HEIGHT))
    # horizontale linien
    for j in range(1, CELLS_H):
        pygame.draw.line(DISPLAY, GREY, (0, j * SCALE), (WIDTH, j * SCALE))

def invert_cell(cell):
    # invertiert die geklickte zelle. war sie schwarz ist sie jetzt weiss
    x, y = cell
    if ba[y][x]:
        to_set = 0
    else:
        to_set = 1
    ba[y][x] = to_set

def split_by_n(seq, n):
    while seq:
        yield seq[:n]
        seq = seq[n:]

def export_number():
    # 2-dim Array transponieren und in 1d umwandeln
    flat = ba.T.flatten()
    flat_str = "".join(["{}".format(i) for i in flat])
    # Von Base 2 zu Base 10 * 17
    b10 = int(flat_str, 2) * CELLS_H
    # in 70 Zeichen lange Zeilen aufteilen
    line_len = 70
    splitted = list(split_by_n(str(b10), line_len))
    for i in splitted:
        print(i)
    print()

def draw_cell(cell):
    # fuellt die angegebene zelle schwarz
    # Koordinaten in cell sind vertauscht!
    y, x = cell
    pygame.draw.rect(DISPLAY, BLACK,
            (x * SCALE, fabs(y - CELLS_H + 1) * SCALE, SCALE, SCALE))

def update_grid():
    # Malt das Grid neu
    DISPLAY.fill(WHITE)
    draw_grid()

    it = numpy.nditer(ba, flags=["multi_index"])
    while not it.finished:
        if it[0] == 1:
            draw_cell(it.multi_index)
        it.iternext()

    export_number()

update_grid()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            cell = get_cell(mouse_x, mouse_y)
            #print("Clicked cell {}".format(cell))
            invert_cell(cell)
            update_grid()

    pygame.display.update()

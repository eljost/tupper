#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Vgl. http://mathworld.wolfram.com/TuppersSelf-ReferentialFormula.html
# Vgl. https://www.youtube.com/watch?v=_s5RFgd59ao
# Braucht pygame and python3

from decimal import *
from math import floor
from re import sub

import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCALE = 10 # Finales Bild wird 106 * SCALE, 17 * SCALE Pixel groß

scaled_surf = pygame.Surface((106 * SCALE, 17 * SCALE))
scaled_surf.fill(WHITE)
ac_dipl = """
149343668566216596446190485711247034162117892972418407098829907762220
444173176870166848098123043596604981577825764114127265221780613607706
904476082738404861552890067049703651330711618413056742872798520354929
633804806626650647040099651230564279310307794569452219014817231465672
587824113422528936842996082572417597705406846318968898418700382661667
990983094693699443442226292277455846853397721888347020183546566978425
03268696064"""

pr0gramm = """
1337714535382728133813809959399514640235259621127073342338691207526699
7803825909898698338263458509361602654288421843298178601054719818212564
8354337310807292021666625341660743659604063995423062872715507850076885
3842794241060254456331128682008728009426815604789907705336855245145282
2485758932866266710174831702740706515875478280499751715114029755908968
2694494703676971542503748375843229688794246017662902283162420728413554
8132884804563791735381462379511305419014566748614390700594175708125381
13522072510428849923314823763700907769856"""

def int_from_str(long_str):
    return int(sub("\s+", "", long_str))

def tupper(x, y):
    with localcontext() as ctx:
        # Wichtig. Modulo funktioniert nicht mit Standard-Praezision
        ctx.prec=600
        return 0.5 < floor(
            (floor(Decimal(y) / 17) *
            ctx.power(2, -17 * floor(x) - (floor(y) % 17))) % 2)

def scaled_pixel(x, y):
    # Skaliert einzelne Pixel auf SCALE * SCALE hoch
    # und malt sie auf scaled_surf
    pygame.draw.rect(scaled_surf, BLACK, (x * SCALE, y * SCALE, SCALE, SCALE))

k = int_from_str(pr0gramm)
for x in range(106):
    for y in range(17):
        if tupper(x, k + y):
            # Pixel malen wenn er Ungleichung erfuellt
            scaled_pixel(x, y)

# horizontal spiegeln
pygame.image.save(
    pygame.transform.flip(scaled_surf, True, False), "tupper.png")

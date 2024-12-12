#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
import pyfiglet

fonts = pyfiglet.FigletFont.getFonts()

for fonty in fonts:
    print("Testing font " + fonty)
    f = pyfiglet.Figlet(font=fonty, width=40)
    print(f.renderText("FooBar"))
    # sleep(0.8)

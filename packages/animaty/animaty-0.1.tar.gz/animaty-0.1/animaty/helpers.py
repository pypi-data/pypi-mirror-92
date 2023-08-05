"""This file contains helpful functions for the animaty workflow"""
from animaty.animate import Frame
import curses

"""getFramesFromFile lets you extract frames from a file"""
def getFramesFromFile(file) -> Frame:
    frames = []
    with open(file) as f:
        #split the file contents on every doubled new line
        contents = f.read().split("\n\n")
        for content in contents:
            frame = Frame(content)
            frames.append(frame)
    return frames

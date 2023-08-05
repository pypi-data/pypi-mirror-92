"""This is the main file of the animaty package"""
import curses
from time import sleep
from curses import wrapper

"""The Frame class is used to represent each frame in an animation."""
class Frame:
    
    __frametime__ = None
    __framecontent__ = None

    def __init__(self, content, time=1) -> None:
        self.__framecontent__ = content
        self.__frametime__ = time

    ##########getters############

    """getFramecontent gives back the content of a frame"""
    def getFramecontent(self):
        return self.__framecontent__
    
    """getFrametime gives back the time of a frame"""
    def getFrametime(self):
        return self.__frametime__
    
    ##########setters#############

    """setFrametime changes the time the frame is displayed on the screen"""
    def setFrametime(self, time):
        self.__frametime__ = time

"""The Animator class is responsible for animating the previously created frames"""
class Animator:

    __animatorframes__ = None
    __fps__ = None


    def __init__(self, frames, fps=None) -> None:

        self.__animatorframes__ = frames

        #check if fps is an integer
        if isinstance(fps, int):
            self.__fps__ = fps
        elif fps is not None:
            raise AttributeError("Please enter an integer as fps")

    """animate starts an animation based on previously entered frames"""
    def animate(self):
        wrapper(self.__animationfunc__)
    
    """animationLoop starts an infinite animation based on previously entered frames"""
    def animationLoop(self):
        while True:
            self.animate()

    def __animationfunc__(self, stdscr):
        stdscr.clear()
        for frame in self.__animatorframes__:

            stdscr.addstr(0, 0, frame.getFramecontent())

            #if we want to us a fixed fps count, ignore the frametime
            if self.__fps__ != None:

                #sleep for a calculated time (count of frames divided by the fps we want to have)
                sleep(len(self.__animatorframes__)/self.__fps)

            else:

                sleep(frame.getFrametime())

            stdscr.refresh()
        #sleep so that the last frame wont just disappear
        sleep(0.5)
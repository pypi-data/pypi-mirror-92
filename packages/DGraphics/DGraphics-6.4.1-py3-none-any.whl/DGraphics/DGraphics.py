"""
DGraphics v6.4x86_01.

This module contains all the modules from the package DGraphics
and all of them have been grouped into classes, except for the private
_x functions and Wraper Classes that are not part of the package.


info:

-sprites:
--max number of sprites in a program is 7158.

"""

import os
HIDEWELCOM = False
try:
    if True:#os.environ['dgwelcom'] == 'hide':
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        HIDEWELCOM = True
except KeyError:
    pass
import pygame
from math import sin, cos, radians, atan, degrees, ceil, floor, sqrt
from pygame.locals import *
import random
from random import choice
import tkinter
from time import sleep, time as getTime
from PIL import Image
import threading
from weakref import WeakKeyDictionary
from base64 import b64encode
import multiprocessing


"""
Env variables
"""

Networking = False



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  --------------------------------- mod ------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #


helptxt = \
"""
help text for DGraphics vX.

info:
  1 - max number of sprites in a program is 7156.

  2 - do not rotate the 3D camera < 0 or > 180.

  3 - available bit depths for BaseProgram are currently 8, 16, 24, and 32.
      These are passed to the -b flag when running a Program in USO form e.g. -b16.

"""


def dummy():
    pass
class Dummy:
    pass
class TPDS(Dummy):
    removed = False
    def update(self): pass
class TPD(Dummy):
    sprites = [] #hold type TPDS
    quit = False


def timeit(func, rep=100):
	t = time()
	for i in range(rep):
		func()
	return time() - t
def compare(func1, func2, rep=100):
	a = timeit(func1, rep)
	b = timeit(func2, rep)
	return "%s faster by %s."%(str(func1 if a < b else func2), str(a - b if a > b else b - a))



def ljoin(l):
    buffer = ""
    for string in l:
        buffer = "%s%s"%(buffer, string)
    return buffer

def invert(x, y):
    """Small hack to convert pymunk to pygame coordinates"""
    return x, y+600

def check_bit_depth(flags):
    if "-b8" in flags:
        return 8
    elif "-b16" in flags:
        return 16
    elif "-b24" in flags:
        return 24
    elif "-b32" in flags:
        return 32
    else:
        return False
def check_precision(flags):
    if "-p0" in flags:
        return 1
    elif "-p1" in flags:
        return 3
    elif "-p2" in flags:
        return 6
    else:
        return 3


def LI(file):
    """
    Accessibility: private
    Discription: return a pygame image surface.
    E.g. -
    Overridable: false
    Errors: None
    """

    return pygame.image.load(file)

def loadImg():
    """
    Accessibility: private
    Discription: return locimg.bmp from python Lib.
    E.g. -
    Overridable: false
    Errors: None
    """

    return pygame.image.load("locimg.bmp")

def zsort(sl):
    sorted = False
    while not sorted:
        i = -1
        sorted = True
        for s in sl:
            if i+2 == len(sl): break
            i += 1
            if s.z > sl[i+1].z:
                sorted = False
                old = s
                sl[i] = sl[i+1]
                sl[i+1] = old
    return list(sl.__reversed__())
def ysort(sl):
    sorted = False
    while not sorted:
        i = -1
        sorted = True
        for s in sl:
            if i+2 == len(sl): break
            i += 1
            if s.y > sl[i+1].y:
                sorted = False
                old = s
                sl[i] = sl[i+1]
                sl[i+1] = old
    return list(sl.__reversed__())



class GliderError(Exception):
    """
    Accessibility: private
    Discription: extends Exception for use in DGraphics.Sprite.glide and DGraphics.Sprite2D.
    E.g. raise GliderError(GliderError.err)
    Notes: for static use only. err object for passing when raising.
    """

    err = "Cannot glide because this Sprite is already gliding."

class IDError(Exception):
    """
    Accessibility: private
    Discription: extends Exception for use in DGraphics.Sprite.
    E.g. raise IDError(IDError.err)
    Notes: for static use only. err objects for passing when raising.
    """

    err = "ID is already taken!"
    stid = "'static id'"
    err2 = "Cannot locate sprite with static id %s."%str(stid)

class SpriteError(Exception):
    """
    Accessibility: private
    Discription: extends Exception for use in DGraphics.Sprite, DGraphics.extentions.ThreadedSprite2D
    and DGraphics.extentions.CameraSprite2D.
    E.g. raise SpriteError(SpriteError.err)
    Notes: for static use only. err objects for passing when raising.
    """

    err1 = "Only a subclass of DGraphics.Sprite2D\n\
    can be added to DGraphics.Program."
    err2 = "Only a subclass of DGraphics.extentions.ThreadedSprite2D\n\
    can be added to DGraphics.extentions.ThreadedProgram."
    err3 = "Only a subclass of DGraphics.extentions.CameraSprite2D\n\
    can be added to DGraphics.extentions.CameraProgram."


class AnimationError(Exception):
    """
    Accessibility: private
    Discription: extends Exception for use in DGraphics.Sprite.
    E.g. raise AnimationError(AnimationError.err)
    Notes: for static use only. err objects for passing when raising.
    """

    err1 = "Animation is already stoped."
    err2 = "Could not remove sprite from animation."

class DisplayModeError(Exception):
    """
    Accessibility: private
    Discription: extends Exception for use in DGraphics.BaseProgram.
    E.g. raise DisplayModeError(DisplayModeError.err1)
    Notes: for static use only. err objects for passing when raising.
    """

    err1 = "There was an error when selecting an optimal display mode for a\
    Program (BaseProgram). This could be caused by invalid bit depth or because\
    there are currently no available display mode to choose from. see pythons\
    built-in help() documentation on DGraphics for available bit depths."


class DisplayFrequencyError(Exception):
    """
    Accessibility: private
    Discription: extends Exception for use in DGraphics.BaseProgram.
    E.g. raise DisplayModeError(DisplayModeError.err1)
    Notes: for static use only. err objects for passing when raising.
    """
    error = "None"

    err1 = "There was an error in setting the display frequency for Program: 'Unknown Program'.\
    More info on the cause of the exception: %s."%error


class CompileError(Exception):
    """
    Accessibility: private
    Discription: extends Exception for use in DGraphics.extentions.AdaptedSprite2D.
    E.g. raise CompileError(CompileError.err1)
    Notes: for static use only. err objects for passing when raising.
    """

    err1 = "DGraphics.extentions.AdaptedSprite2D.update cannot be called."

class SocketClassError(Exception):
    """
    Accessibility: private
    Discription: extends Exception for use in DGraphics.extentions.AdaptedSprite2D.
    E.g. raise CompileError(CompileError.err1)
    Notes: for static use only. err objects for passing when raising.
    """

    err = "DGraphics.extentions.AdaptedSprite2D.update cannot be called."

class ChannelClassError(Exception):
    """
    Accessibility: private
    Discription: extends Exception for use in DGraphics.extentions.AdaptedSprite2D.
    E.g. raise CompileError(CompileError.err1)
    Notes: for static use only. err objects for passing when raising.
    """

    err = "DGraphics.extentions.AdaptedSprite2D.update cannot be called."

class ClientClassError(Exception):
    """
    Accessibility: private
    Discription: extends Exception for use in DGraphics.extentions.AdaptedSprite2D.
    E.g. raise CompileError(CompileError.err1)
    Notes: for static use only. err objects for passing when raising.
    """

    err = "DGraphics.extentions.AdaptedSprite2D.update cannot be called."



class ThreadProcess2D(threading.Thread):
    inst = TPD()
    def run(self):
        self.loaded = 0
        self.loadedT = True
        while not self.inst.quit:
            for sprite in self.inst.sprites.__reversed__():
                sleep(1/self.inst.fps)
                if not sprite.removed:
                    self.loadedT = False
                    sprite.update()
                    self.loadedT = True
                else:
                    self.inst.sprites.remove(sprite)
            self.loaded += 1




class CollisionHandlerProccess(threading.Thread):
    prog = None
    _sprites = {}
    def __init__(self, prog):
        super().__init__()
        self.prog = prog

    def run(self):
        prog = self.prog
        collision = extentions.Collision3D.CollisionXYZ
        sps = prog.sprites
        while True:
            if not prog.lock:
                prog.lock = True
                for sprite in sps:
                    self._sprites.update({sprite: []})
                    for sprite2 in sps:
                        if collision(sprite, sprite2):
                            self._sprites[sprite].append(sprite2)
                        sleep(0.00001)
            sleep(0.0001)

    def get(self, sprite):
        try:
            return self._sprites[sprite]
        except KeyError:
            return []



class ThreadProcess3D(threading.Thread):
    inst = TPD()
    def run(self):
        while not self.inst.quit:
            break


class FPSController(threading.Thread):
    inst = TPD()
    def run(self):
        pass



class Camera:
    x=0
    y=0
    _angle = 45
    sincam = 0
    coscam = 0

    def __init__(self):
        self.rotate(0)

    def move(self, x, y):
        self.x += x*TIME.dt
        self.y += y*TIME.dt

    def rotate(self, deg):
        self._angle += round(deg)
        self.sincam = sin(SINLIST[self._angle])
        self.coscam = cos(COSLIST[self._angle])
    def setRotation(self, deg):
        self._angle = round(deg)
        self.sincam = sin(SINLIST[deg])
        self.coscam = cos(COSLIST[deg])
    def angle(self):
        return self._angle

    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y


class T:
    dt = 1



def checkID(id, uidl):
    if id in uidl:
        raise IDError(IDError.err)
    else:
        return id

""" Vector lambdas for calculationg sprite Normal Vector """
hVec = lambda deg: -deg
vVec = lambda deg: 180 - deg
cVec = lambda deg: deg - 180

SINLIST = ()
COSLIST = ()
for i in range(-360, 360):
    SINLIST = SINLIST + (sin(radians(i)),)
    COSLIST = COSLIST + (cos(radians(i)),)


imagetobytes = pygame.image.tostring
imagefrombytes = pygame.image.fromstring

ids = iter(range(1024, 8182))
uids = []
TIME = T()
R = range(64)
DEG = degrees
Font = pygame.font.SysFont





# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  ----------------------------- Color ----------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

class Color:
    r = 0
    g = 0
    b = 0

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (122, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    LIGHTBLUE = (0, 122, 255)
    AUQUA = (0, 255, 122)
    ORANGE = (255, 122, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, color=BLACK):
        """
        Accessibility: public
        Discription: constructor for Color.
        E.g. myColor = Color(Color.RED)
        Overridable: false
        Errors: None
        """


        self.r, self.g, self.b = color


    def getColorRGB(self):
        """
        Accessibility: public
        Discription: returns the red, green and blue values of this Color.
        E.g. myOtherColor.setColor(myColor.getColorRGB())
        Overridable: false
        Errors: None
        """

        return (self.r, self.g, self.b)

    def getColor(self):
        """
        Accessibility: public
        Discription: returns the color as a Color object, which can be passed
        to Color.setFromColor(color).
        E.g. myOtherColor = myColor.getColor()
        Overridable: false
        Errors: None
        """

        return self

    def setColorRGB(self, r, g, b):
        """
        Accessibility: public
        Discription: sets color from r, g and b values which can be 1 to 255.
        E.g. myColor.setColorRGB(255, 40, 0)
        Overridable: false
        Errors: None
        """

        self.r, self.g, self.b = (r, g, b)

    def setFromColor(self, color):
        """
        Accessibility: public
        Discription: sets the color from a Color object.
        E.g. myColor.setFromColor(myOtherColor)
        Overridable: false
        Errors: None
        """

        self.r, self.g, self.b = (color.r, color.g, color.b)

    def setColor(self, color):
        """
        Accessibility: public
        Discription: sets the color from a constant defined in the Color class.
        E.g. myColor.setColor(Color.BLUE)
        Overridable: false
        Errors: None
        """

        self.r, self.g, self.b = color

    def random():
        return Color(choice((Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.BLACK, Color.CYAN, Color.LIGHTBLUE, Color.PURPLE, Color.WHITE, Color.ORANGE, Color.AUQUA)))








# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  ----------------------------- Core ---------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #


class BaseProgram:
    sprites = []
    resolution = (800, 600)
    backgroundcolor = None
    fps = 36
    quit = False
    BITDEPTH = 24
    FPS_controll = False
    texts = []
    display_frequency = (800, 600)
    DF = (1, 1)
    DFS = True
    dt = 0
    widgets = True

    def __init__(self):
        """
        Accessibility: private
        Discription: constructor for BaseProgram.
        E.g. -
        Overridable: false
        Errors: -
        """

        self.backgroundcolor = Color()
        if self.widgets:
            self.window = pygame.display.set_mode(self.resolution, 0, BaseProgram.BITDEPTH)
        else:
            self.window = None
            self.main = self.main2
        if self.FPS_controll:
            # Disable or reasign Program.setFPS()
            # For example setFPS calls a variable with a function for setting fps,
            # here change that variable is changed to set the fps regularity (or something).
            ## FPSC = FPSController()
            ## FPSC.inst = self
            ## FPSC.start()
            pass


    def finnish(self):
        """
        Accessibility: public
        Discription: this function is called at the end of your program
        (not when an exception is raised). Your program terminates after
        Program.stop() has been called.
        E.g.
        class myProgram(DGraphics.BaseProgram):
            def finnish(self):
                print("!GAME OVER!")
                input()
        
        Overridable: true
        Errors: -
        """

        print("Program {} ended.".format(self))


    def build(self):
        """
        Accessibility: public
        Discription: this function is called once before the first
        call to BaseProgram/*or Program*/.main() at the start of your program.
        E.g.
        class myProgram(DGraphics.BaseProgram):
            def build(self):
                self.addSprite(mySprite)
        
        Overridable: true
        Errors: -
        """

    def update(self):
        """
        Accessibility: public
        Discription: this function is called once per frame update
        and is where the main handeling of your program should go.
        E.g.
        class myProgram(DGraphics.BaseProgram):
            def update(self):
                self.mySprite.doSomething()
        Overridable: true
        Errors: -
        """


    def main(self):
        """
        Accessibility: private
        Discription: iterates through self.sprites and calls Sprite.update(). Updates pygame display
        and calles pygame.event.pump(). Fills screen with BaseProgram.backgroundcolor and calls BaseProgram.update().
        E.g. None
        Overridable: false
        Errors: -

        dfx, dfy = self.DF
        if self.DFS:
            for sprite in self.sprites.__reversed__():
                if not sprite.removed:
                    sprite.updateDFS(dfx, dfy)
                else:
                    self.sprites.remove(sprite)
        else:
            for sprite in self.sprites.__reversed__():
                if not sprite.removed:
                    sprite.update()
                else:
                    self.sprites.remove(sprite)

        if self.DFS:
            for text in self.texts:
                text.updateDFS(dfx, dfy)
        else:
            for text in self.texts:
                text.update(self)

        """

        [sprite.updateDFS() for sprite in self.sprites]
        [text.updateDFS() for text in self.texts]


        self.update()
        pygame.event.pump()
        pygame.display.update()
        self.window.fill(self.backgroundcolor.getColorRGB())

    def main2(self):
        """
        Accessibility: private
        Discription: unwidget version of BaseProgram.main, calls self.update (thats it).
        E.g. None
        Overridable: false
        Errors: -
        """

        self.update()
        

    def getSprite(self, index):
        """
        Accessibility: public
        Discription: returns the index'th sprite added to the program. !remember, starts at 0!
        E.g. sprite3 = self.getSprite(2)
        Overridable: false
        Errors: None
        """

        return self.sprites[index]

    def getLastSprite(self):
        """
        Accessibility: public
        Discription: returns the last sprite added to the program.
        E.g. sprite = self.getLastSprite()
        Overridable: false
        Errors: None
        """

        return self.sprites[self.sprites.__len__()-1]

    def getSpritesByName(self, Name):
        """
        Accessibility: public
        Discription: returns a list of all the sprites in the program of class Name.
        E.g.
        for sp in self.getSpritesByName(Block):
            sp.doSomething()
        Overridable: false
        Errors: None
        """

        buffsprites = []
        for sprite in self.sprites:
            if isinstance(sprite, Name):
                buffsprites.append(sprite)
        return buffsprites

    def getSpriteByID(self, id):
        """
        Accessibility: public
        Discription: returns the sprite with the id specified. If no
        sprite is found with the given id, IDError is raised.
        E.g.
        car2 = getSpriteByID("car 2")
        Overridable: false
        Errors: None
        """

        for sprite in self.sprites:
            if sprite.id == id:
                return sprite
        IDError.stid = id
        raise IDError(IDError.err2)

    def setWindowSize(self, w, h, *flags):
        """
        Accessibility: public
        Discription: sets the size of the program window
        E.g. self.setWindowSize(800, 600)
        Overridable: false
        Errors: None
        Flags: flags, e.g. -n[native resolution] -f[fullscreen]
        """

        if len(flags) > 0:
            if "-n" in flags:
                try:
                    w, h = pygame.display.list_modes()[0]
                except IndexError:
                    try:
                        print("There was an error in selecting an optimal display resolution. Applying native settings...")
                        w, h = (0, 0)
                    except Exception:
                        raise DisplayModeError(DisplayModeError.err1)
            if "-f" in flags:
                self.window = pygame.display.set_mode((w, h), pygame.FULLSCREEN if not "-w" in flags else pygame.FULLSCREEN | pygame.NOFRAME,
                                                      BaseProgram.BITDEPTH)
                self.resolution = (self.window.get_width(), self.window.get_height())
                return;
        self.window = pygame.display.set_mode((w, h), pygame.NOFRAME if "-w" in flags else 0, BaseProgram.BITDEPTH)
        self.resolution = (self.window.get_width(), self.window.get_height())

    def setDisplayFrequency(self, frequencyx, frequencyy):
        try:
            resx, resy = self.resolution
            self.display_frequency = (frequencyx, frequencyy)
            self.DF = (resx/frequencyx, resy/frequencyy)
        except Exception as ex:
            DisplayFrequencyError.inf = ex
            raise DisplayFrequencyError(DisplayFrequencyError.err1)
    def getDisplayFrequency(self):
        return self.display_frequency

    def enableDisplayFrequencyScalling(self):
        self.DFS = True
        resx, resy = self.resolution
        self.DF = (resx/self.display_frequency[0], resy/self.display_frequency[1])
    def disableDisplayFrequencyScalling(self):
        self.DFS = False
        self.DF = (0, 0)


    def setWindowName(self, name):
        """
        Accessibility: public
        Discription: sets the name of the window in the top left corner.
        E.g. self.setWindowName("Big Fun Game")
        Overridable: false
        Errors: None
        """

        pygame.display.set_caption(name)

    def setBackgroundColor(self, color):
        """
        Accessibility: public
        Discription: sets the background color from a Color object.
        E.g. self.setBackgroundColor(myColor)
        Overridable: false
        Errors: None
        """

        self.backgroundcolor = color

    def setFPS(self, fps):
        """
        Accessibility: public
        Discription: sets the program fps - time to wait between program update calls.
        E.g. self.setFPS(46)
        Overridable: false
        Errors: None
        """

        self.fps = fps

    def getFPS(self):
        """
        Accessibility: public
        Discription: returns the program fps.
        E.g. self.setFPS(self.getFPS() - 5)
        Overridable: false
        Errors: None
        """

        return self.fps

    def getSprites(self):
        """
        Accessibility: public
        Discription: returns a list of all the sprites in the program.
        E.g.
        for sp in self.getSprites():
            sp.doSomething()
        Overridable: false
        Errors: None
        """

        return self.sprites

    def getResolution(self):
        """
        Accessibility: public
        Discription: returns the size of the program screen.
        E.g. self.setWindowSize(self.getResolution()[0] - 200, 600)
        Overridable: false
        Errors: None
        """

        return self.resolution

    def keyDown(key):
        """
        Accessibility: public
        Discription: returns True if the key 'key' is being pressed.
        keys name are constants represented by a 'K_' followed by the name of the key.
        these are stored directly in DGraphics.
        (For a list of all key codes call DGraphics.key_codes())
        E.g.
        if Program.keyDown(DGraphics.K_f):
            self.doSomething()
        Overridable: false
        Errors: None
        """

        if pygame.key.get_pressed()[key]:
            return True
        return False


    def log(self, text):
        """
        Accessibility: public
        Discription: log text from the current program to console.
        E.g. self.log("hello world!")
        Overridable: false
        Errors: None
        """

        print("<%s>LOG: {}".format(text)%self.__str__())
    def debug(self, text):
        """
        Accessibility: public
        Discription: log debug text from the current program to console.
        E.g. self.debug("sprite1 x is: "+sprite1.getX())
        Overridable: false
        Errors: None
        """

        print("<%s>DEBUG: {}".format(text)%self.__str__())

    def random(a, b):
        """
        Accessibility: public
        Discription: returns a random number between a and b.
        E.g. ranNum = Program.random(0, 200)
        Overridable: false
        Errors: None
        """

        return random.randint(a, b)

    def stop(self):
        """
        Accessibility: public
        Discription: finnishes program execution as soon as posible,
        cleaning up and ending any discarded threads of dump files.
        E.g.
        if MyProgram.game_over:
            MyProgram.stop()
        Overridable: false
        Errors: None
        """

        self.quit = True

    def drawImage(self, image, xy):
        """
        Accessibility: public
        Discription: blits a DGraphics.Image to the current programs display. Image is
        buffered imediatly (befor the function exits), though not actualy
        displayed on the screen until the next call to Program.update.
        uses display frequency, making it a little bit slower than BaseProgram.drawImageFast, wich
        is exactly the same except a little faster, and does not use display frequency scalling.
        E.g. MyProgram.drawImage(MyImage, (200, 300))
        Overridable: false
        Errors: None
        """

        self.window.blit(image.image, (round(xy[0]*self.DF[0]), round(xy[1]*self.DF[1])))
    def drawImageFast(self, image, xy):
        """
        Accessibility: public
        Discription: basicaly the same as BaseProgram.drawImage, except does not use display frequency scalling, so
        it is a little bit faster, depending on how you use it.
        E.g. MyProgram.drawImageFast(MyImage, (200, 300))
        Overridable: false
        Errors: None
        """

        self.window.blit(image.image, (round(xy[0]*self.DF[0]), round(xy[1]*self.DF[1])))

    def drawRect(self, pos, size=(1, 1), color=Color()):
        """
        Accessibility: public
        Discription: draws a buffer rectangle to the current programs display, with
        the top left corner positioned as "pos", the size of the rectangle determined
        by "size", and color of the rectangle (must be a three value rgb tuple. This can be
        handeled by DGraphics.Color.getColorRBG). The rectangle is buffered imediatly, though not actualy
        displayed on the screen until the next call to Program.update.
        E.g. MyProgram.drawRect((200, 300), size=(50, 40), color=MyColor.getColorRGB())
        Overridable: false
        Errors: None
        """

        dfx, dfy = self.DF
        self.window.fill(color.getColorRGB(), (round(pos[0]*dfx), round(pos[1]*dfy), round(size[0]*dfx), round(size[1]*dfy)))
    def drawRectFast(self, pos, size=(1, 1), color=Color()):
        """
        Accessibility: public
        Discription: exactly the same as BaseProgram.drawRect except it does not use display frequency scalling.
        so it's a little bit faster depending on how you use it
        E.g. MyProgram.drawRectFast((200, 300), size=(50, 40), color=MyColor.getColorRGB())
        Overridable: false
        Errors: None
        """

        self.window.fill(color.getColorRGB(), (pos[0], pos[1], size[0], size[1]))


    def addText(self, text):
        """
        Accessibility: public
        Discription: adds a DGraphics.Text object !(not raw class)! to the program and returns it. Options
        and controlls for the Text objects are accessed through functions for the Text object.
        E.g. MyProgram.addText(myTextObject)
        Overridable: false
        Errors: None
        """

        text.window = self.window
        text.prog = self
        self.texts.append(text)
        return text

    def remove(self, sprite):
        self.sprites.remove(sprite)







class Program(BaseProgram):
    """
    Accessibility: public
    Discription: this class is what your game, animation, app, etc will extend and do all the processing in.
    extend it and override it's build and update methods to control your program. This extends DGraphics.BaseProgram.
    E.g.
    class myProgram(Program):
        def build(self):
            # build your program - initialize data, Sprites, Images, etc...
        def update(self):
            # update things in your program - altering sprites, changeing variables, controlling key input.
            
    Notes: do not access or change static variables.
    Extendable: True
    """


    def addSprite(self, sprite, x=0, y=0, id=b'0x0000', visable=True):
        """
        Accessibility: public
        Discription: adds a Sprite2D to the program and returns it.
        E.g. self.addSprite(mySprite, x=300, visable=False)
        Overridable: false
        Errors: None
        """

        if not issubclass(sprite, Sprite2D):
            raise SpriteError(SpriteError.err1)
        self.sprites.append(sprite(self.window, self, x, y, id, visable))
        return self.getLastSprite()


    def circleCollision(self, sprite1, sprite2):
        """
        Accessibility: public
        Discription: returns True if sprite1 and sprite2 collide. This collision
        is detected using a circle collider the diameter of the sprites height.
        E.g.
        if self.circleCollision(ballA, ballB):
            doSomthnig()
        Overridable: false
        Errors: None
        """

        return (sprite1.getSize()[1] + sprite2.getSize()[1] >=
                sqrt((sprite2.x - sprite1.x)**2 - (sprite2.y - sprite1.y)**2))






class Program3D(BaseProgram):
    """
    Accessibility: public
    Discription: this is the same as Program except it adds some 3d vectors, some 3d renderers
    and 2d vector transformations. This extends DGraphics.BaseProgram.
    E.g.
    class myProgram(Program3D):
        def build(self):
            # build your program - initialize data, Sprites, Images, etc...
        def update(self):
            # update things in your program - altering sprites, changeing variables, controlling key input.
            
    Notes: do not access or change static variables.
    Extendable: True
    """

    camera = Camera()
    collisionHandler = None
    lock = False

    def __init__(self):
        """
        Accessibility: private
        Discription: constructor for Program3D.
        E.g. -
        Overridable: false
        Errors: -
        """

        self.backgroundcolor = Color()
        self.window = pygame.display.set_mode(self.resolution, 0, BaseProgram.BITDEPTH)
        self.collisionHandler = CollisionHandlerProccess(self)
        self.collisionHandler.start()


    def addSprite(self, sprite, x=0, y=0, z=0, id=b'0x0000', visable=True, images="*", shadow=True, depth=6):
        """
        Accessibility: public
        Discription: adds a Sprite2D to the program and returns it.
        E.g. self.addSprite(mySprite, x=300, visable=False)
        Overridable: false
        Errors: None
        """

        if not issubclass(sprite, Sprite3D):
            raise SpriteError(SpriteError.err1)
        self.sprites.append(sprite(self.window, self, x, y, z, id, visable, images, shadow, depth))
        return self.getLastSprite()


    def main(self):
        """
        Accessibility: private
        Discription: iterates through self.sprites and calls Sprite.update(). Updates pygame display
        and calles pygame.event.pump(). Fills screen with BaseProgram.backgroundcolor and calls BaseProgram.update().
        E.g. None
        Overridable: false
        Errors: -
        """

        if self.camera.angle() >= 45 or self.camera.angle() <= -45:
            self.sprites = zsort(self.sprites)
        else:
            self.sprites = ysort(self.sprites)
            
        [sprite.updateDFS() for sprite in self.sprites]
        [text.updateDFS() for text in self.texts]
        self.lock = False


        self.update()
        pygame.event.pump()
        pygame.display.update()
        self.window.fill(self.backgroundcolor.getColorRGB())


    def getCamera(self):
        return self.camera







# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  ----------------------------- Image ----------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
TSCL = pygame.transform.scale
TRT = pygame.transform.rotate
TFP = pygame.transform.flip
class Image:
    rotation = 0

    def __init__(self, image=loadImg(), size=None, rotation=rotation):
        """
        Accessibility: public
        Discription: constructor for Image.
        E.g. myImage = Image(image="car.bmp", size=(25, 14))
        Overridable: false
        Errors: None
        """

        try:
            self._image = pygame.image.load(image)
        except (pygame.error, TypeError):
            self._image = image
        try:
            self._image.get_width
        except AttributeError:
            print("!failed to load image %s!"%image)
            self._image = loadImg()
        self._size = size if not size == None else (self._image.get_width(), self._image.get_height())
        self.rotation = rotation


    def loadImage(self, file):
        """
        Accessibility: public
        Discription: sets the the image from a file.
        E.g. myImage.loadImage("block.png")
        Overridable: false
        Errors: None
        """
        
        self._image = LI(file)
        self.rotation = 0

    @property
    def image(self):
        """
        Accessibility: public @property
        Discription: returns an image file,
        this can be used as arg for Image.loadImage(file).
        E.g. myOtherImage = myImage.image
        Overridable: false
        Errors: none
        """
        # sin(rot)*getSize()[0], sin(rot)*getSize()[1]
        return TSCL(TRT(self._image, -self.rotation), self._size)

    def rotate(self, deg):
        """
        Accessibility: public
        Discription: rotates image deg degrees.
        E.g. myImage.rotateImage(180)
        Overridable: false
        Errors: minor
        """
        
        self.rotation += deg
        return self

    def setRotation(self, angle, Arbt=False):
        """
        Accessibility: public
        Discription: sets the rotation of the image.
        E.g. myImage.setRotation(90)
        Overridable: false
        Errors: minor
        """

        self.rotation = angle
        return self

    def scale(self, x, y):
        """
        Accessibility: public
        Discription: sets the size of the image in pixels.
        E.g. myImage.scale(50, 50)
        Overridable: false
        Errors: None
        """

        self._size = (x, y)
        return self

    @property
    def size(self):
        """
        Accessibility: public @property
        Discription: get the size of the image in pixels.
        E.g. image_size = myImage.size
        Overridable: false
        Errors: None
        """

        return self._size

    def flip(self, x, y):
        """
        Accessibility: public
        Discription: flips the image horizonatly (x), and/or verticaly (y)
        E.g. myImage.flip(True, False) # flips along x.
        Overridable: false
        Errors: None
        """

        self._image = TFP(self._image, x, y)
        return self

    

    def setImage(self, image):
        self.image = image



    def Rotate(image, deg):
        return TRT(image, deg)
    def Scale(image, x, y):
        return TSCL(image, (x, y))

    def network_encode(image, sx, sy, DEF="RGB"):
        return b64encode(imagetobytes(Scale(image, sx, sy), DEF)).decode('iso-8859-1')
    def network_decode(imagedata, sx, sy, DEF="RGB"):
        return imagefrombytes(b64decode(image), (sx, sy), DEF)

    def copy(self):
        return Image(self._image, self._size, self.rotation)






class Animation:
    def __init__(self, sprites=None, start=False):
        super().__init__()
        self.sprites = sprites if not sprites == None else list()
        self.anim = []
        self.index = 0
        self.frame = 0
        self.fpt = 1
        self.assign(self.sprites)
        self.lf = 0
        self.running = start

    def update(self):
        if self.running:
            for i in range(len(self.anim)):
                if self.frame <= self.anim[i][1]:
                    for sprite in self.sprites:
                        sprite.image = self.anim[i][0]
                    self.index = i
                    break
            #try:
            self.frame += self.fpt#* round(TIME.dt, _PRECISION)/4
            #except NameError: self.frame += self.fpt * round(TIME.dt, PRECISION)/4
            if self.frame > self.anim[len(self.anim) - 1][1]:
                self.reset()

    def assign(self, sprites):
        for sprite in sprites:
            sprite.animation = self
            try:
                sprite.image = self.anim[self.index][0]
            except IndexError:
                sprite.image = Image()
        self.sprites = sprites
        return self
    def join(self, sprites):
        for sprite in sprites:
            sprite.animation = self
            try:
                sprite.image = self.anim[self.index][0]
            except IndexError:
                sprite.image = Image()
            if not sprite in self.sprites: self.sprites.append(sprite)
            return self
    def resign(self, sprites):
        try:
            for sprite in sprites:
                sprite.animation = None
                self.sprites.remove(sprite)
        except ValueError:
            raise AnimationError(AnimationError.err2)
        return self

    def forceAll(self):
        for sprite in self.sprites:
            self.force(sprite)
        return self
    def force(self, sprite):
        sprite.animation = self
        try:
            sprite.image = self.anim[self.index][0]
        except IndexError:
            sprite.image = Image()
        return self


    def start(self, force=False):
        if force:
            self.forceAll()
        self.running = True
        return self
    def stop(self):
        self.running = False
        return self
    def reset(self, _from=0):
        self.frame = _from
        try:
            self.lf = self.anim[_from - 1][1]
        except IndexError:
            self.lf = 0
            
    def setFPT(self, fpt):
        self.fpt = fpt
        return self

    def remove(self, index=-1):
        del self.anim[len(anim)-1 if index == -1 else index]
        return self
    def add(self, image, frames=1):
        self.anim.append([image, self.lf + frames])
        self.lf = frames + self.lf
        return self
    def addImages(self, *images__frames):
        for image, frames in images__frames:
            self.add(image, frames)
        return self

    def get(self, index=None):
        try:
            return self.anim[index][0]
        except TypeError:
            return self.anim[self.index][0]

    def rotateAll(self, deg):
        for img in self.anim:
            img[0].rotateImage(deg)
    def setRotationAll(self, deg):
        for img in self.anim:
            img[0].setRotation(deg)
    def scaleAll(self, x, y):
        for img in self.anim:
            img[0].scale(x, y)
    def copy(self):
        cpy = Animation(self.sprites, self.running)
        anim = [[a.copy(), f] for a, f in self.anim]
        cpy.anim, cpy.index, cpy.frame, cpy.fpt, cpy.lf = \
                  (anim, self.index, self.frame, self.fpt, self.lf)
        return cpy




class AnimationHandler(threading.Thread):
    def __init__(self, pause, *anims):
        self.anims = list(anims)
        self.kill = False
        super().__init__()
        self.pause = pause
        self.start()
    def run(self):
        while not self.kill:
            sleep(0.02)
            if not self.pause:
                for anim in self.anims:
                    anim.update()
    def getAnim(self, index):
        return self.anims[index]
    def add(self, *anim):
        for a in anim:
            if not a in self.anims: self.anims.append(a)
    def remove(self, *anim):
        [self.anims.remove(a) for a in anim]
    def removeByIndex(self, index):
        del self.anims[index]
    def pop(self):
        self.anims.pop()
    def kill(self):
        self.kill = True
    def pause(self):
        self.pause = True
    def resume(self):
        self.pause = False



"""
class Animation:
    def __init__(self, assign=None):
        self.anim = []
        self.started = False
        self.index=0
        self.frame = 0
        self.lf = 0
        self.fpt = 1
        self.assign(assign)
        sprite = None

    def assign(self, sprite):
        if sprite == None: return;
        sprite.animation = self
        try:
            sprite.image = self.anim[self.index][0]
        except IndexError:
            sprite.image = Image()
        self.sprite = sprite
    def resign(self, sprite):
        sprite.animation = None
        self.sprite = None

    def start(self):
        self.started = True
    def stop(self):
        self.started = False
    def reset(self, _from=0):
        self.frame = _from
        try:
            self.lf = self.anim[_from - 1][1]
        except IndexError:
            self.lf = 0
            
    def setFPT(self, fpt):
        self.fpt = fpt

    def remove(self, index=-1):
        del self.anim[len(anim)-1 if index == -1 else index]
    def add(self, image, frames=1):
        self.anim.append([image, self.lf + frames])
        self.lf = frames + self.lf

    def get(self, index):
        return self.anim[index][0]
        
    def update(self):
        if self.started:
            for i in range(len(self.anim)):
                if self.frame <= self.anim[i][1]:
                    self.index = i
                    break
            self.frame += self.fpt * TIME.dt/4
            if self.frame > self.anim[len(self.anim) - 1][1]:
                self.reset()

    def rotateAll(self, deg):
        for img in self.anim:
            img[0].rotateImage(deg)
    def setRotationAll(self, deg):
        for img in self.anim:
            img[0].setRotation(deg)
    def scaleAll(self, x, y):
        for img in self.anim:
            img[0].scale(x, y)
"""



class Images:
    images = {}

    def __init__(self, *groups):
        for tup in groups:
            self.images.update({tup[0]: tup[1]})
    def add(self, name, image):
        self.images.update({name: image})
    def get(self, name):
        return self.images[name]
    def getByIndex(self, index):
        return self.images[list(self.images)[index]]
    def remove(self, name):
        del self.images[name]







# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  ------------------------------- Mouse ----------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

MGP = pygame.mouse.get_pressed
MGXY = pygame.mouse.get_pos
MSXY = pygame.mouse.set_pos
MSV = pygame.mouse.set_visible
MGF = pygame.mouse.get_focused


class Mouse:
    """
    Static class for getting mouse info.
    """
    vis = True
    def mouseDown(button):
        """
        Accessibility: public
        Discription: returns True if the mouse button 1, 2 or 3 is pressed.
        1=Left mouse button, 2=Scroller, 3=Right mouse button.
        E.g.
        if Mouse.mouseDown(1):
            print("left mouse button clicked.")
        Overridable: false
        Errors: None
        """

        if MGP()[button - 1]:
            return True
        return False

    @property
    def x():
        """
        Accessibility: public @property
        Discription: returns the x position of the mouse.
        E.g.
        x = Mouse.x
        Overridable: false
        Errors: None
        """

        return MGXY()[0]
    @property
    def y():
        """
        Accessibility: public @property
        Discription: returns the y position of the mouse.
        E.g.
        y = Mouse.y
        Overridable: false
        Errors: None
        """

        return MGXY()[1]
    def getXY():
        """
        Accessibility: public
        Discription: returns a tuple with the x and y position of the mouse.
        E.g.
        x, y = Mouse.getXY()
        Overridable: false
        Errors: None
        """

        return MGXY()

    def setX(x):
        """
        Accessibility: public
        Discription: sets the x position of the mouse.
        E.g.
        Mouse.setX(200)
        Overridable: false
        Errors: None
        """

        MSXY((x, Mouse.getY()))
    def setY(y):
        """
        Accessibility: public
        Discription: sets the y position of the mouse.
        E.g.
        Mouse.setY(160)
        Overridable: false
        Errors: None
        """

        MSXY((Mouse.getX(), y))
    def setXY(x, y):
        """
        Accessibility: public
        Discription: sets the x and y position of the mouse.
        E.g.
        Mouse.setXY(200, 180)
        Overridable: false
        Errors: None
        """

        MSXY((x, y))
    def goto(pos):
        """
        Accessibility: public
        Discription: same as Mouse.setXY except takes a tuple.
        E.g.
        pos = (200, 180)
        Mouse.goto(pos)
        Overridable: false
        Errors: None
        """

        MSXY(pos)

    def show():
        """
        Accessibility: public
        Discription: shows the mouse.
        E.g.
        Mouse.show()
        Overridable: false
        Errors: None
        """

        MSV(True)
        Mouse.vis = True
    def hide():
        """
        Accessibility: public
        Discription: hides the mouse.
        E.g.
        Mouse.hide()
        Overridable: false
        Errors: None
        """

        MSV(False)
        Mouse.vis = False
    @property
    def visible():
        """
        Accessibility: public @property
        Discription: returns True or False for mouse visibility.
        E.g.
        if not Mouse.visible:
            Mouse.show()
        Overridable: false
        Errors: None
        """

        return Mouse.vis
    @property
    def focused():
        """
        Accessibility: public @property
        Discription: gets the window focus of the mouse.
        E.g.
        if Mouse.focused:
            Mouse.hide()
        Overridable: false
        Errors: None
        """

        return MGF()






# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  ----------------------------- __init__ ---------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

if not HIDEWELCOM:
    print("\nHello from the DGraphics community... oh, wait...\nThere isn't one.")
version = "6.4x86_01"

# init pygame sound                   c
# pygame.mixer.pre_init(44100, 16, ?-(2), 4096)
pygame.mixer.init()

BPKD = BaseProgram.keyDown
PRECISION = 2

def run(program, *flags):
    """
    Accessibility: public
    Discription: run a Program with given flags.
    E.g. DGraphics.run(myProgram)
    Overridable: false
    Errors: None
    """

    pygame.init()
    cq = "-q" in flags
    bd = check_bit_depth(flags)
    fpsc = "-f" in flags
    PRECISION = check_precision(flags)
    global _PRECISION
    _PRECISION = PRECISION

    if bd: BaseProgram.BITDEPTH = bd
    p = program()
    c = pygame.time.Clock()
    p.FPS_controll = fpsc

    p.build()
    while not p.quit:
        if cq:
            if BPKD(K_q): break
        p.main()
        TIME.dt = round(c.tick(p.fps)/(1/p.fps*1000), PRECISION) + 1
    p.finnish()
    pygame.quit()


def help():
    """
    Accessibility: public
    Discription: prints the help text.
    E.g. DGraphics.help()
    Overridable: false
    Errors: not finnished
    """

    print(helptxt)



def key_codes():
    """
    Accessibility: public
    Discription: prints key codes for Program.keyDown(key).
    E.g. DGraphics.key_codes()
    Overridable: false
    Errors: None
    """

    print("""
K_BACKSPACE   backspace
K_TAB         tab
K_RETURN      return
K_PAUSE       pause
K_ESCAPE      escape
K_SPACE       space
K_EXCLAIM     !   
K_QUOTEDBL    "     
K_HASH        #     
K_DOLLAR      $   
K_AMPERSAND   &   
K_LEFTPAREN   (     
K_RIGHTPAREN  )   
K_ASTERISK    *    
K_PLUS        +   
K_COMMA       ,  
K_MINUS       -     
K_PERIOD      .   
K_SLASH       /      
K_0           0       
K_1           1       
K_2           2       
K_3           3       
K_4           4       
K_5           5       
K_6           6       
K_7           7       
K_8           8       
K_9           9       
K_COLON       :     
K_SEMICOLON   ;     
K_LESS        <       
K_EQUALS      =     
K_GREATER     >       
K_QUESTION    ?       
K_AT          @       
K_LEFTBRACKET [       
K_BACKSLASH   \       
K_RIGHTBRACKET ]      
K_CARET       ^       
K_UNDERSCORE  _       
K_BACKQUOTE   `       
K_a           a       
K_b           b       
K_c           c       
K_d           d       
K_e           e       
K_f           f       
K_g           g       
K_h           h       
K_i           i       
K_j           j       
K_k           k       
K_l           l       
K_m           m       
K_n           n       
K_o           o       
K_p           p       
K_q           q       
K_r           r       
K_s           s       
K_t           t       
K_u           u       
K_v           v       
K_w           w       
K_x           x       
K_y           y       
K_z           z       
K_DELETE      delete
K_KP0         keypad 0
K_KP1         keypad 1
K_KP2         keypad 2
K_KP3         keypad 3
K_KP4         keypad 4
K_KP5         keypad 5
K_KP6         keypad 6
K_KP7         keypad 7
K_KP8         keypad 8
K_KP9         keypad 9
K_KP_PERIOD     .     keypad period
K_KP_DIVIDE     /     keypad divide
K_KP_MULTIPLY   *     keypad multiply
K_KP_MINUS      -     keypad minus
K_KP_PLUS       +     keypad plus
K_KP_ENTER            keypad enter
K_KP_EQUALS     =     keypad equals
K_UP                  up arrow
K_DOWN                down arrow
K_RIGHT               right arrow
K_LEFT                left arrow
K_F1                  F1
K_F2                  F2
K_F3                  F3
K_F4                  F4
K_F5                  F5
K_F6                  F6
K_F7                  F7
K_F8                  F8
K_F9                  F9
K_F10                 F10
K_F11                 F11
K_F12                 F12
K_F13                 F13
K_F14                 F14
K_F15                 F15
K_NUMLOCK             numlock
K_CAPSLOCK            capslock
K_SCROLLOCK           scrollock
K_RSHIFT              right shift
K_LSHIFT              left shift
""")





# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  ----------------------------- sound -----------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

class UnprotectedThread(threading.Thread):
    def stop(self):
        self._stop()

def fadeThreadCallback(data):
    o = False
    assert data.sounds[0].channel != data.sounds[1].channel, "DGraphics.Sound.Fader.faderThreadProcces.fadeThreadCallback:\
 fader sounds must be of different channels."

    orivols = data.sounds[0].volume, data.sounds[1].volume
    done = False
    stime = getTime()
    while not done:
        factor = (getTime() - stime)/data.factor
        if factor >= 1:
            done = True
        data.sounds[0].setVolume(orivols[0]*(1 - factor))
        data.sounds[1].setVolume(orivols[0]*factor)

class DetachedData(object):
    factor = 1
    sounds = []


class Sound:
    sound = None
    _channel = None
    _volume = 0.5
    def __init__(self, file, channelid=1):
        self.sound = pygame.mixer.Sound(file)
        self._channel = pygame.mixer.Channel(channelid)
        self.setVolume(self._volume)
        
    def play(self, loop=0):
        self._channel.play(self.sound, loop)
    def stop(self):
        self._channel.stop()
    def pause(self):
        self._channel.pause()
    def unpause(self):
        self._channel.unpause()
    def setVolume(self, vol):
        self._channel.set_volume(vol)
        self._volume = vol
    @property
    def volume(self):
        return self._volume
    def playing(self):
        return self._channel.get_busy()
    def setChannel(self, id):
        del self._channel
        self._channel = pygame.mixer.Channel(id)
        self.setVolume(self.volume)
    def setFromChannel(self, channel):
        del self._channel
        self._channel = channel
        self.setVolume(self.volume)
    @property
    def channel(self):
        return self._channel


    def push_channels(num_channels):
        pygame.mixer.set_num_channels(num_channels)

    class Fader:
        faderThreadProcces = None
        data = None
        def __init__(self):
            self.data = DetachedData()
            self.faderThreadProcces = UnprotectedThread(target=fadeThreadCallback, args=(self.data,))
        def fade(self, from_, to_, factor):
            self.data.factor = factor
            self.data.sounds = [from_, to_]
            self.faderThreadProcces.start()
        def reset(self):
            self.faderThreadProcces.stop()
            del self.faderThreadProcces
            self.faderThreadProcces = UnprotectedThread(target=fadeThreadCallback, args=(self.data,))




# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  ----------------------------- Network ----------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

"""
class MyServer(Server):
    def fum(self, foo):
        print(foo)

class MyChannel(Channel):
    def Network_fum(self, data):
        self._server.server.fum(data["foo"])

MyServer(MyChannel).launch()
"""

def getInverseDictItem(dict, item):
    for k, i in dict.items():
        if i == item:
            return k
    return False

try:
    from PodSixNet.Channel import Channel as ChannelPSN
    from PodSixNet.Server import Server as ServerPSN
    from PodSixNet.Connection import connection
    from PodSixNet.Connection import ConnectionListener



    class Channel(ChannelPSN):
        def __init__(self, *args, **kwargs):
            self.name = "anonymous%i"%BaseProgram.random(100000, 999999)
            ChannelPSN.__init__(self, *args, **kwargs)
            self.Send({"action": "name", "name": self.name})

            def Network_name(self, data):
                self.name = data['name']

            # BUILT-IN
            def Network_Close(self, data):
                self._server.Remove(self)



    class Socket(ServerPSN):
        channelClass = Channel
        delay = None

        def __init__(self, subserver, *args, **kwargs):
            ServerPSN.__init__(self, *args, **kwargs)
            self.clients = WeakKeyDictionary()
            self.server = subserver
            print("\nOpening PSNserver on %s:%s"%(kwargs["localaddr"][0], kwargs["localaddr"][1]))

        def Launch(self):
            print("\nlaunched Server!\n")
            d = self.delay
            while True:
                sleep(d)
                self.Pump()

        def Remove(self, channel):
            del self.clients[channel]
            print("%s has exited."%name)
            self.disconnection(channel, channel.name, channel.addr[0])

        def SendToAll(self, data):
            [c.Send(data) for c in self.clients]

        def connection(self, channel, name, addr):
            """
            Override to use channel, name and addr. Called when new connection made.
            """
            pass
        def disconnection(self, channel, name, addr):
            """
            Override to use channel, name and addr. Called when client disconnects.
            """
            pass
            

        # BUILT-IN
        def Connected(self, channel, addr):
            self.clients[channel] = channel.name
            print("\n%s has connected!"%channel.addr[0])
            self.connection(channel, channel.name, channel.addr[0])



    class Server:
        socket = None
        def __init__(self, ChannelClass, SocketClass=Socket, addr="localhost:3917", delay=0.0001):
            if not issubclass(SocketClass, Socket):
                raise SocketClassError(SocketClassError.err)
            if not issubclass(ChannelClass, Channel):
                raise ChannelClassError(ChannelClassError.err)
            SocketClass.channelClass = ChannelClass
            host, port = addr.split(":")
            self.socket = SocketClass(subserver=self, localaddr=(host, int(port)))
            self.socket.delay = delay
        def launch(self):
            launcher = threading.Thread(target=self.socket.Launch)
            launcher.start()

        def Send(self, name, data):
            try:
                getInverseDictItem(self.socket.clients, name).Send(data)
            except AttributeError:
                print("\nError: %s.Send: cannot send to %s. No such client."%(type(self), name))

        @property
        def connections(self):
            return self.socket.clients
        def getSocket(self):
            return self.socket
        




    class ClientSocket(ConnectionListener):
        delay = None
        _connected = False
        def __init__(self, host, port, connect=True):
            self.host, self.port = (host, port)
            self.name = None
            if connect:
                self.Connect((host, port))
                self._connected = True

        def connect(self):
            if not self._connected:
                self.Connect((self.host, self.port))
            else:
                print("\nAlready connected.")

        def Launch(self):
            if not self._connected:
                self.connect()
            print("\nestablishing connection to PodSixNet.Connection.ConnectionListener@%s:%s!\n"%(self.host, self.port))
            d=self.delay
            while True:
                connection.Pump()
                self.Pump()
                sleep(d)

        def Network_name(self, data):
            self.name = data['name']
            n= "\nyou were renamed %s"%self.name
            print(n)

        # BUILT-IN
        def Network_connected(self, data):
            print("\nConection Established!")
        
        def Network_error(self, data):
            print('\nerror:', data['error'][1])
            connection.Close()
        
        def Network_disconnected(self, data):
            print('\nServer disconnected <%s:%s>@localhost:'%(self.host, self.port))
            exit()



    class Client:
        client = None
        def __init__(self, addr="localhost:3917", ClientClass=ClientSocket, delay=0.0001, auto=True):
            if not issubclass(ClientClass, ClientSocket):
                raise ClientClassError(ClientClassError.err)
            host, port = addr.split(":")
            self.client = ClientClass(host, int(port), connect=auto)
            self.client.delay = delay
        def connect(self):
            launcher = threading.Thread(target=self.client.Launch)
            launcher.start()
            while self.client.name == None: pass
        def rename(self, name):
            connection.Send({"action": "name", "name": name})
            self.client.name = name
            n= "\nyou were renamed %s"%name
            print(n)
        def Send(self, data):
            connection.Send(data)
        def close(self):
            connection.Send({"action": "Close"})
except ImportError:
    print("Networking Disabled: Requiored Packages: PodSixNet")
    print("Install PodSixNet using pip install or the wheel.")







# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  ----------------------------- Text ----------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

class Text:
    size = 15
    color = Color.BLACK
    font = "Comic Sans MS"
    text = ""
    hidden = ""
    pos = 0, 0
    display = None
    visable = True
    surface = None
    window = None
    DF = (1, 1)
    ADFS = True
    prog = None

    def __init__(self, text, pos, size=size, color=color, font=font, visable=visable):
        self.size, self.color, self.font, self.text, self.pos, self.hidden, self.visable = \
                   (size, color, font, text, pos, text, visable)
        try:
            Font(font, 30)
        except Exception:
            print("!Invalid Font: %s. using default font type..."%font)
            font = Text.font
        self.display = Font(font, size)
        self.surface = self.display.render(text, False, color)
        if not visable: self.hide()

    def allowDisplayFrequencyScalling(self):
        self.ADFS = True
    def blockDisplayFrequencyScalling(self):
        self.ADFS = False

    def show(self):
        self.text = self.hidden
        self.visable = True
        self.surface = self.display.render(self.text, False, self.color)
    def hide(self):
        self.hidden = self.text
        self.text = ""
        self.visable = False
        self.surface = self.display.render(self.text, False, self.color)
    def isVisable(self):
        return self.visable

    def setText(self, text):
        if self.visable: self.text = text
        self.hidden = text
        self.surface = self.display.render(self.text, False, self.color)
    def getText(self):
        return self.hidden

    def setSize(self, size):
        self.size = size
        self.display = Font(self.font, size)
        self.surface = self.display.render(self.text, False, self.color)
        return self
    def getSize(self):
        return self.size

    def setPos(self, x, y):
        self.pos = x, y
    def move(self, x, y):
        dt = TIME.dt
        self.pos = (self.pos[0]+(x*dt), self.pos[1]+(y*dt))
    def getPos(self):
        return self.pos

    def setColor(self, color):
        self.color = color.getColorRGB()
    def setColorRGB(self, r, g, b):
        self.color = (r, g, b)
    def getColor(self):
        return Color(self.color)
    def getColorRGB(self):
        return self.color

    def setBold(self, bool):
        self.display.set_bold(bool)
        self.surface = self.display.render(self.text, False, self.color)
    def setUnderline(self, bool):
        self.display.set_underline(bool)
        self.surface = self.display.render(self.text, False, self.color)
    def setItalic(self, bool):
        self.display.set_italic(bool)
        self.surface = self.display.render(self.text, False, self.color)



    def setFont(self, font):
        self.font = font
        self.display = Font(font, self.size)
        self.surface = self.display.render(self.text, False, self.color)
    def getFont(self):
        return self.font
    def listFontNames():
        Text.Fonts.listnames()
    def listFonts():
        print("List of font statics from DGraphics.Text.Fonts:")
        font_dir_list = Text.Fonts().__dir__()
        for ref in font_dir_list:
            if not "__" in ref and ref != "listnames":
                if ref[0] == "s":
                    print(" (symbol font) %s"%ref)
                else:
                    print(" %s"%ref)
        print("\n")

    def update(self):
        self.window.blit(self.surface, (self.pos[0], self.pos[1]))
    def updateDFS(self):
        if not self.ADFS:
            self.update()
            return
        dfx, dfy = self.prog.DF
        buff = Font(self.font, round(self.size*dfx))  # needs work, scales to only x.
        self.window.blit(buff.render(self.text, False, self.color), (round(self.pos[0]*dfx), round(self.pos[1]*dfy)))



    class Fonts(object):
        __fonts__ = ("Comic Sans MS", "Arial", "System", "Baskerville Old Face",
                     "Agency FB", "Algerian", "Bauhaus 93", "Bell MT", "Bernard MT",
                     "Blackadder ITC", "Bradley Hand ITC", "Calibri", "Brush Script",
                     "Jokerman", "Lucida Console", "Maiandra GD", "Stencil", "Lucida Sans Typewriter")
        __symbol__ = ("Opus Function Symbols Std", "Marlett", "Helsinki Special Std", "MS Outlook")

        COMIC_SANS      = __fonts__[0]
        ARIAL           = __fonts__[1]
        SYSTEM          = __fonts__[2]
        OLD_TYPE        = __fonts__[3]
        AGENCY          = __fonts__[4]
        ALGERIAN        = __fonts__[5]
        BAUHAUS         = __fonts__[6]
        BELL            = __fonts__[7]
        BERNARD         = __fonts__[8]
        BLACKADDER      = __fonts__[9]
        BRADLEY         = __fonts__[10]
        CALIBRI         = __fonts__[11]
        BRUSH_SCRIPT    = __fonts__[12]
        JOKERMAN        = __fonts__[13]
        CONSOLE         = __fonts__[14]
        MAIANDRA        = __fonts__[15]
        STENCIL         = __fonts__[16]
        SANS_TYPEWRITER = __fonts__[17]

        sOPUS_FUNCTION_SYMBOLS = __symbol__[0]
        sMARLETT               = __symbol__[1]
        sHELSINKI              = __symbol__[2]
        sOUTLOOK               = __symbol__[3]

        def listnames():
            print("List of raw font names from DGraphics.Text.Fonts.__fonts__:")
            for font in Text.Fonts.__fonts__:
                print(" %s"%font)
            print("\nList of raw symbols font names from DGraphics.Text.Fonts.__symbol__:")
            for font in Text.Fonts.__symbol__:
                print(" %s"%font)
            print("\n")


    





# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  ----------------------------- sprite ----------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

class Sprite:
    window = None
    prog = None
    vis = True
    id = b'0x0000'
    animation = None
    gliding = False
    image = None
    removed = False


    def __init__(self, window, program, id=id, visable=True):
        """
        Accessibility: private
        Discription: constructor for Sprite.
        E.g. -
        Overridable: false
        Errors: -
        """

        self.window = window
        self.prog = program
        
        if id == Sprite.id:
            self.id = str(hex(next(ids)))
            uids.append(self.id)
        else:
            self.id = checkID(id, uids)
                    
        self.vis = visable
        self.image = Image()
        self.start()



    def action(self):
        pass

    def start(self):
        pass

    def update(self):
        self.action()
    def updateDFS(self):
        self.action()

    def setID(self, id):
        uids.remove(self.id)
        self.id = checkID(id, uids)
        uids.append(id)

    def getID(self):
        return self.id

    def type(self):
        return self.__class__

    def show(self):
        self.vis = True
    def hide(self):
        self.vis = False
    def visable(self):
        return self.vis

    def getProgram(self):
        return self.prog

    def remove(self):
        self.removed = True
        self.prog.remove(self)

    def setImage(self, image):
        self.image = image
        return self

    def getImage(self):
        return self.image

    def getAnimation(self):
        return self.animation
    def setAnimation(self, anim):
        anim.join([self])
    def removeAnimation(self):
        try:
            self.animation.resign([self])
        except AttributeError:
            pass

    def isGliding(self):
        return self.gliding

    def localised(self):
        """
        Accessibility: private
        Discription: dummy function used for try, except gates in extentions.AdaptedControlls.
        E.g. Program.localised()
        Overridable: false
        Errors: None
        """

        pass











class Sprite2D(Sprite):
    x = 0
    y = 0
    glider = None
    image = None
    ADFS = True


    def __init__(self, window, program, x=0, y=0, id=id, visable=True):
        """
        Accessibility: private
        Discription: constructor for Sprite2D.
        E.g. -
        Overridable: false
        Errors: -
        """

        self.x = x
        self.y = y
        glider = {"inc": (0, 0), "ticks": 0, "et": 0}
        super().__init__(window, program, id, visable)



    def updateDFS(self):
        if not self.ADFS:
            self.update()
            return
        dfsx, dfsy = self.prog.DF
        i = self.image
        sx, sy = i.size
        if self.vis:
            self.window.blit(i.scale(round(sx*dfsx), round(sy*dfsy)).image, (self.x*dfsx, self.y*dfsy))
            i.size = (sx, sy)
        self.action()




    def allowDisplayFrequencyScalling(self):
        self.ADFS = True
    def blockDisplayFrequencyScalling(self):
        self.ADFS = False


    def move(self, x, y):
        self.x += x*TIME.dt
        self.y += y*TIME.dt


    def forward(self, steps):
        self.move(round(sin(radians(self.image.rotation)), 4)*steps, round(cos(radians(self.image.rotation+180)), 4)*steps)

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getXY(self):
        return self.x, self.y
    def getIntXY(self):
        return round(self.x), round(self.y)

    def goto(self, x, y):
        self.x, self.y = x, y

    def rotate(self, deg):
        if self.animation:
            self.animation.rotateAll(deg)
            return;
        self.image.rotateImage(deg)

    def getRotation(self):
        return self.image.rotation

    def setDirection(self, deg):
        if self.animation:
            self.animation.setRotationAll(deg)
            return;
        self.image.setRotation(deg)

    def scale(self, x, y):
        if self.animation:
            self.animation.scaleAll(x, y)
            return;
        self.image.scale(x, y)

    def getSize(self):
        return self.image.getSize()

    def isTouching(self, sprite):
        w, h = self.getSize()
        w2, h2 = sprite.getSize()
        return (self.x < sprite.x + w2 and
                sprite.x < self.x + w and
                self.y < sprite.y + h2 and
                sprite.y < self.y + h)

    def isTouchingType(self, Type):
        for sprite in self.prog.sprites:
            if isinstance(sprite, Type) and \
                self.isTouching(sprite) and sprite != self:
                return sprite
        return False

    def touchingEdge(self):
        """
        Info: for display frequency scalling enabled programs use Sprite2D.touchingEdgeDFS instead.

        """
        ww, wh, w, h = (self.prog.resolution[0], self.prog.resolution[1], self.getSize()[0], self.getSize()[1])
        return (self.x <= 0 or
                self.x+w >= ww or
                self.y <= 0 or
                self.y+h >= wh
                )
    def touchingEdgeDFS(self):
        ww, wh, w, h = (self.prog.display_frequency[0], self.prog.display_frequency[1], self.getSize()[0], self.getSize()[1])
        return (self.x <= 0 or
                self.x+w >= ww or
                self.y <= 0 or
                self.y+h >= wh
                )


    def getNormalVec(self):
        ww, wh = self.prog.display_frequency
        w, h = self.image.getSize()
        x, y = self.x, self.y
        if (y <= 0 or y+h >= wh) and (x <= 0 or x+w >= ww):
            return cVec
        elif x <= 0 or x+w >= ww:
            return hVec
        elif y <= 0 or y+h >= wh:
            return vVec
        else:
            return False
 

    def randomDirection(self):
        self.rotate(random.randint(0, 360))

    def ifOnEdgeBounce(self):
        if self.prog.DFS:
            if self.touchingEdgeDFS():
                vec = self.getNormalVec()
                angle = vec(self.getRotation())
                self.setDirection(angle)
                resx, resy = self.prog.display_frequency
                x, y, dfx, dfy = self.x, self.y, self.prog.DF[0], self.prog.DF[1]
                sizex, sizey = self.image.getSize()

                if vec == hVec:
                    self.setX(1 if x <= resx/2 else resx-sizex-1)
                elif vec == vVec:
                    self.setY(1 if y <= resy/2 else resy-sizey-1)
                elif vec == cVec:
                    self.setY(1 if y <= resy/2 else resy-sizey-1)
                    self.setX(1 if x <= resx/2 else resx-sizex-1)
        else:
            if self.touchingEdge():
                vec = self.getNormalVec()
                angle = vec(self.getRotation())
                self.setDirection(angle)
                resx, resy = self.prog.resolution
                x, y = self.x, self.y
                sizex, sizey = self.image.getSize()

                if vec == hVec:
                    self.setX(1 if x <= resx/2 else resx-sizex-1)
                elif vec == vVec:
                    self.setY(1 if y <= resy/2 else resy-sizey-1)
                elif vec == cVec:
                    self.setY(1 if y <= resy/2 else resy-sizey-1)
                    self.setX(1 if x <= resx/2 else resx-sizex-1)



    def pointTo(self, x, y):
        if self.y < y:
            self.setDirection(degrees(atan((x - self.x)/(self.y - y))) - 180)
        else:
            self.setDirection(degrees(atan((x - self.x)/(self.y - y))))
    def pointToSprite(self, sprite):
        self.pointTo(sprite.x, sprite.y)

    def distanceTo(self, x, y):
        return sqrt((x - self.x)**2 + (self.y - y)**2)
    def distanceToSprite(self, sprite):
        return self.distanceTo(sprite.x, sprite.y)

    def randomScreenPos(self):
        x, y = self.image.getSize()
        wx, wy = self.prog.resolution
        self.goto(Program.random(0, wx - x), Program.random(0, wy - y))


    def clone(self, x="def", y="def", rot="def"):
        if rot == "def": rot = self.getRotation()
        
        self.prog.addSprite(self.__class__, x=self.x if x == "def" else x, y=self.y if y == "def" else y).setDirection(rot).setImage(self.image.copy())






Surface = pygame.Surface
Rect = pygame.Rect
SRCALPHA = pygame.SRCALPHA
Ellipse = pygame.draw.ellipse

class Sprite3D(Sprite):

    x = 0
    y = 0
    z = 0
    depth = 0
    images = None
    image = None
    shadow = None
    surface = None
    rotationX, rotationY, rotationZ = (0, 0, 0)
    glider = {"inc": (0, 0, 0), "ticks": 0, "et": 0}
                               

    def __init__(self, window, program, x=0, y=0, z=0, id=id, visable=True, images="*", shadow=True, depth=6):
        """
        Accessibility: private
        Discription: constructor for Sprite2D.
        E.g. -
        Overridable: false
        Errors: -
        """

        self.images = Images(("image", Image())) if images == "*" else images
        image = self.images.getByIndex(0)
        self.x = x
        self.y = y
        self.z = z
        self.depth = depth
        super().__init__(window, program, id, visable)
        self.getcollision = self.prog.collisionHandler.get
        self.shadow = {"img": Rect(self.x,
                                        -(sin(self.prog.camera.angle())*self.z + cos(self.prog.camera.angle())*self.y) + self.prog.camera.y,
                                        self.image.getSize()[0], self.image.getSize()[1]),
                       "show": shadow, "vis": 100}


    def updateDFS(self):
        self.update_glider()
        cam = self.prog.camera

        dfsx, dfsy = self.prog.DF

        if self.shadow["show"] and self.vis and self.y >= 0:
            w, h = self.image.getSize()
            surface = Surface((w, h), SRCALPHA)

            self.shadow["img"] = Rect(0, 0, w*dfsx, h*dfsy)
            Ellipse(surface, (0, 0, 0, self.shadow["vis"]), self.shadow["img"])
            self.window.blit(surface, ((self.x - cam.x)*dfsx,
                                       ((cam.sincam*self.z + cam.coscam*h) + cam.y)*dfsy))

        if self.vis:
            i = self.image
            sx, sy = i.size
            self.window.blit(i.scale(round(sx*dfsx), round(sy*dfsy)).image,
                             ((self.x - cam.x)*dfsx, ((cam.sincam*self.z - cam.coscam*self.y) + cam.y)*dfsy))

            i.size = (sx, sy)
        self.action()



    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def setZ(self, z):
        self.z = z
    def setXYZ(self, x, y, z):
        self.x, self.y, self.z = (x, y, z)
        
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getZ(self):
        return self.z
    def getXYZ(self):
        return self.x, self.y, self.z

    def translate(self, x, y, z):
        dt = TIME.dt
        self.x += x*dt
        self.y += y*dt
        self.z += z*dt
    def _translate(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

    def forward(self, x, y, z):
        """
        Depricated!
        """
        sinx, cosx, siny, cosy, sinz, cosz = (sin(radians(self.rotationX)), cos(radians(self.rotationX)),
                                              sin(radians(self.rotationY)), cos(radians(self.rotationY)),
                                              sin(radians(self.rotationZ)), cos(radians(self.rotationZ)))
        self.translate(
            x*((self.x*cosz - self.y*sinz) + (self.z*siny + self.x*cosy)),
            y*((self.x*sinz + self.y*cosz) + (self.y*cosx - self.z*sinx)),
            z*((self.y*sinx + self.z*cosx) + (self.z*cosy - self.x*siny))
            )

    def setRotationX(self, r):
        self.rotationX = r
    def setRotationY(self, r):
        self.rotationY = r
    def setRotationZ(self, r):
        self.rotationZ = r
    def rotateX(self, r):
        self.rotationX += r
    def rotateY(self, r):
        self.rotationY += r
    def rotateZ(self, r):
        self.rotationZ += r


    def showShadow(self):
        self.shadow["show"] = True
    def hideShadow(self):
        self.shadow["show"] = False
    def setShadowVis(self, vis):
        assert vis > 255 or vis < 0, "arg 1 of DGraphics.Sprite3D.setShadowVis() must be <= 255 and >= 0."
        self.shadow["vis"] = vis
    def getShadowVis(self):
        return self.shadow["vis"]


    def getDepth(self):
        return self.depth
    def setDepth(self, d):
        self.depth = d

    def getImages(self):
        return self.images

    def glide(self, ticks, xyz):
        if self.gliding:
            raise GliderError(GliderError.err)
        self.gliding = True
        self.glider = {"inc": ((xyz[0]-self.x)/ticks, (xyz[1]-self.y)/ticks, (xyz[2]-self.z)/ticks), "ticks": 0, "et": ticks}

    def update_glider(self):
        if self.gliding:
            if self.glider["ticks"] == self.glider["et"]:
                self.gliding = False
                return;
            self.glider["ticks"] += 1
            self._translate(self.glider["inc"][0], self.glider["inc"][1], self.glider["inc"][2])


    def isTouching(self, sprite):
        for sp in self.getcollision(self):
            if sp == sprite:
                return True
        return False
    def returnTouching(self):
        return self.getcollision(self)

    def isTouchingType(self, type_):
        for sp in self.getcollision(self):
            if type(sp) == type_:
                return True
        return False
    def returnTouchingType(self, type_):
        touching = []
        for sp in self.getcollision(self):
            if type(sp) == type_:
                touching.append(sp)
        return touching







# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#  ----------------------------- extentions ------------------------------  #
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

class extentions:

    def prepare(numbers, low, high):
        pivot = numbers[high]
        item = low - 1
        for i in range(low, high):
            if numbers[i] <= pivot:
                item = item + 1
                (numbers[item], numbers[i]) = (numbers[i], numbers[item])
        (numbers[item + 1], numbers[high]) = (numbers[high], numbers[item + 1])
        return item + 1
    def sort(numbers, low=0, high=""):
        if high == "":
            high = len(numbers) - 1
        if low < high:
            pivot = extentions.prepare(numbers, low, high)
            extentions.sort(numbers, low, pivot - 1)
            extentions.sort(numbers, pivot + 1, high)


    def roundBlock(x, block):
        return round(x/block)*block
    
    class TileMap(Program):
        """
        !NOT USABLE!
        """
        
        fps = 36
        def __init__(self):
            self.backgroundcolor = Color(Color.BLACK)



    class CameraSprite2D(Sprite2D):
        def update(self):
            if self.vis:
                self.window.blit(self.image.image, (self.x - self.prog.camera.x, self.y + self.prog.camera.y))
            self.action()


        def updateDFS(self):
            if not self.ADFS:
                self.update()
                return
            i = self.image
            sx, sy = i.size
            dfsx, dfsy = self.prog.DF
            if self.vis:
                self.window.blit(i.scale(round(sx*dfsx), round(sy*dfsy)).image, ((self.x - self.prog.camera.x)*dfsx, (self.y + self.prog.camera.y)*dfsy))
                i.size = (sx, sy)
            self.action()

        def ifOnEdgeBounce(self):
            raise RuntimeError("DGraphics.extentions.CameraSprite2D.ifOnEdgeBounce is not callable.")


    class CameraProgram(Program):
        camera = Camera()

        def setCamX(self, x):
            self.camera.x = x
        def setCamY(self, y):
            self.camera.y = y
        def getCamX(self):
            return self.camera.x
        def getCamY(self):
            return self.camera.y
        def moveCam(self, x, y):
            self.camera.x += x*TIME.dt
            self.camera.y += y*TIME.dt

        def addSprite(self, sprite, x=0, y=0, id=b'0x0000', visable=True):
            """
            Accessibility: public
            Discription: adds a CameraSprite2D to the program and returns it.
            E.g. self.addSprite(mySprite, x=300, visable=False)
            Overridable: false
            Errors: None
            """

            if not (issubclass(sprite, extentions.CameraSprite2D) or issubclass(sprite, Sprite2D)):
                raise SpriteError(SpriteError.err3)
            self.sprites.append(sprite(self.window, self, x, y, id, visable))
            return self.getLastSprite()



    class Collision2D:
        def CollisionX(sprite1, sprite2):
            return (sprite1.x < sprite2.x + sprite2.image.size[0] and
                    sprite2.x < sprite1.x + sprite1.image.size[0])
        def CollisionY(sprite1, sprite2):
            return (sprite1.y < sprite2.y + sprite2.image.size[1] and
                    sprite2.y < sprite1.y + sprite1.image.size[1])
        def CollisionXY(sprite1, sprite2):
            return extentions.Collision2D.CollisionX(sprite1, sprite2) and \
                   extentions.Collision2D.CollisionY(sprite1, sprite2)

        def OnlyCollisionX(sprite1, sprite2):
            return extentions.Collision2D.CollisionX(sprite1, sprite2) and \
                   not extentions.Collision2D.CollisionY(sprite1, sprite2)
        def OnlyCollisionY(sprite1, sprite2):
            return extentions.Collision2D.CollisionY(sprite1, sprite2) and \
                   not extentions.Collision2D.CollisionX(sprite1, sprite2)


    class Collision3D(Collision2D):
        def CollisionZ(sprite1, sprite2):
            return (sprite1.z < sprite2.z + sprite2.depth and
                    sprite2.z < sprite1.z + sprite1.depth)
        def CollisionYZ(sprite1, sprite2):
            return extentions.Collision2D.CollisionY(sprite1, sprite2) and \
                   extentions.Collision3D.CollisionZ(sprite1, sprite2)
        def CollisionXZ(sprite1, sprite2):
            return extentions.Collision2D.CollisionX(sprite1, sprite2) and \
                   extentions.Collision3D.CollisionZ(sprite1, sprite2)
        def CollisionXYZ(sprite1, sprite2):
            return extentions.Collision2D.CollisionX(sprite1, sprite2) and \
                   extentions.Collision2D.CollisionY(sprite1, sprite2) and \
                   extentions.Collision3D.CollisionZ(sprite1, sprite2)



    class GliderSprite3D(Sprite3D):
        def glideX(self, ticks, x):
            if self.gliding:
                raise GliderError(GliderError.err)
            self.gliding = True
            self.glider = {"inc": ((x-self.x)/ticks, 0, 0), "ticks": 0, "et": ticks}
        
        def glideY(self, ticks, y):
            if self.gliding:
                raise GliderError(GliderError.err)
            self.gliding = True
            self.glider = {"inc": (0, (y-self.y)/ticks, 0), "ticks": 0, "et": ticks}
            
        def glideZ(self, ticks, z):
            if self.gliding:
                raise GliderError(GliderError.err)
            self.gliding = True
            self.glider = {"inc": (0, 0, (z-self.z)/ticks), "ticks": 0, "et": ticks}




    class ThreadedProgram(Program):
        def __init__(self):
            """
            Accessibility: private
            Discription: constructor for BaseProgram.
            E.g. -
            Overridable: false
            Errors: -
            """

            self.backgroundcolor = Color()
            self.window = pygame.display.set_mode(self.resolution)
            TP2D = ThreadProcess2D()
            TP2D.inst = self
            TP2D.start()
            self.th = TP2D

        def main(self):
            """
            Accessibility: private
            Discription: iterates through self.sprites and calls Sprite.update(). Updates pygame display
            and calles pygame.event.pump(). Fills screen with BaseProgram.backgroundcolor and calls BaseProgram.update().
            E.g. None
            Overridable: false
            Errors: -
            """

            self.update()
            pygame.event.pump()
            if self.th.loaded > 0:
                if self.th.loaded > 9:
                    self.th.loaded = 0
                else:
                    self.th.loaded -= 1
                if self.th.loadedT:
                    pygame.display.update()
                    self.window.fill(self.backgroundcolor.getColorRGB())




    class Controlls:
        keys = (1, 1, 1, 1, 0, 0, 0, 0)
        def wsad(self, sprite):
            dt = TIME.dt
            if BPKD(K_w) and self.keys[0]:
                sprite.y -= self.keys[0]*dt
            if BPKD(K_s) and self.keys[1]:
                sprite.y += self.keys[1]*dt
            if BPKD(K_a) and self.keys[2]:
                sprite.x -= self.keys[2]*dt
            if BPKD(K_d) and self.keys[3]:
                sprite.x += self.keys[3]*dt
                
        def udlr(self, sprite):
            dt = TIME.dt
            if BPKD(K_UP) and self.keys[4]:
                sprite.y -= self.keys[4]*dt
            if BPKD(K_DOWN) and self.keys[5]:
                sprite.y += self.keys[5]*dt
            if BPKD(K_LEFT) and self.keys[6]:
                sprite.x -= self.keys[6]*dt
            if BPKD(K_RIGHT) and self.keys[7]:
                sprite.x += self.keys[7]*dt

        def set(self, w=1, s=1, a=1, d=1, up=0, down=0, left=0, right=0):
            self.keys = (w, s, a, d, up, down, left, right)


    class AdaptedControlls:
        keys = (1, 1, 1, 1, 0, 0, 0, 0)
        def __init__(self, sprite, w=1, s=1, a=1, d=1, up=0, down=0, left=0, right=0):
            self.set(sprite, w, s, a, d, up, down, left, right)

        def wsad(self):
            dt = TIME.dt
            if BPKD(K_w) and self.keys[0]:
                self.sprite.y -= self.keys[0]*dt
            if BPKD(K_s) and self.keys[1]:
                self.sprite.y += self.keys[1]*dt
            if BPKD(K_a) and self.keys[2]:
                self.sprite.x -= self.keys[2]*dt
            if BPKD(K_d) and self.keys[3]:
                self.sprite.x += self.keys[3]*dt
                
        def udlr(self):
            dt = TIME.dt
            if BPKD(K_UP) and self.keys[4]:
                self.sprite.y -= self.keys[4]*dt
            if BPKD(K_DOWN) and self.keys[5]:
                self.sprite.y += self.keys[5]*dt
            if BPKD(K_LEFT) and self.keys[6]:
                self.sprite.x -= self.keys[6]*dt
            if BPKD(K_RIGHT) and self.keys[7]:
                self.sprite.x += self.keys[7]*dt

        def set(self, sprite="set", w=1, s=1, a=1, d=1, up=0, down=0, left=0, right=0):
            if sprite != "set":
                self.sprite = sprite
            self.keys = (w, s, a, d, up, down, left, right)







    class MapOS:

        class File:
            text = None
            readable = False
            def __init__(self, file_name, mode="r", cache=False):
                self.file = open(file_name, mode)
                self.file_name = file_name
                self.mode = mode
                if cache:
                    self.text = self.file.read()
                    self.readable = True

            def change_mode(self, mode):
                if not self.mode == mode:
                    self.mode = mode
                    self.file = open(self.file_name, mode)
                    self.text = None
                    self.readable = None

            def read(self):
                return self.text if self.readable else "not readable"

            def cache(self):
                self.text = self.file.read()
                self.readable = True

            def write(self, data):
                self.file.write(data)

            def create(file_name):
                open(file_name, "x")


        class DataFile(File):
            def __init__(self, file_name, mode="r", cache=False):
                self.data = []
                self.scaned = []
                self.decripted = False
                super().__init__(file_name, mode, cache)

            def getAttribute(self, attr, split=False):
                if self.mode != "r":
                    self.change_mode("r")
                if not self.readable:
                    self.cache()
                if not self.decripted:
                    self.decript()
                for datum in self.data:
                    try:
                        if datum[0] == attr:
                            if not split:
                                return datum[1]
                            else:
                                return datum[1].split(split)
                    except IndexError: pass
                return None
            def fastAttr(self, attr):
                for datum in self.data:
                    try:
                        if datum[0] == attr:
                            return datum[1]
                    except IndexError: pass
                return None

            def decript(self):
                self.data = self.text.split("\n")
                self.decripted = True
                for index in range(len(self.data)):
                    if not "###" in self.data[index]:
                        if self.data[index].find("=")+1:
                            self.data[index] = self.data[index].split("=")
                    else:
                        self.data[index] = ''



        def getObject(datafile, id):
            return eval(datafile.getAttribute(id))

        class Map:
            map = None
            scaned = None
            Default = Sprite
            sizex, sizey = (0, 0)
            def load(self, name, objectdatafile):
                self.map = open("worlds\\%s.map"%name, "r").read()
                self.odf = objectsdatafile
            def setDefault(sprite):
                Map.Default = sprite
            def scan(self):
                self.scaned = []
                py = 0
                odf = self.odf
                for y in self.map.split("\n"):
                    bufferx = []
                    px = 0
                    py += self.sizey
                    for x in y:
                        px += self.sizex
                        if x == " ": continue
                        try:
                            bufferx.append((getObject(odf, x), px, py))
                        except Exception:
                            bufferx.append((Default, px, py))
                    self.scaned.append(bufferx)
            def get(self):
                return self.scaned
            def setSize(self, x, y):
                self.sizex, self.sizey = (x, y)
            def apply(self, program):
                AS = program.addSprite
                GLS = program.getLastSprite
                for y in self.get():
                    for x in y:
                        AS(x[0], x[1], x[2])
                        GLS().scale(self.sizex, self.sizey)






    class ProgramServer(Program):
        def build(self):
            pass


        def update(self):
            pass




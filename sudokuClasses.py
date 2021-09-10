import pygame

pygame.init()
baseFont = pygame.font.Font(None, 48)
pygame.key.set_repeat(500, 100)
colourActive = (255, 0, 0)

class Button:
    # constructor
    def __init__(self, name, fontName, fontSize, colour, posX, posY, buttonWidth, buttonHeight):
        self.name = name
        self.colour = colour
        self.rectangle = pygame.Rect(posX, posY, buttonWidth, buttonHeight)
        self.fontName = fontName
        self.fontSize = fontSize


    def getName(self):
        return self.name

    def drawButton(self, screen):
        self.textSurface = pygame.font.Font(self.fontName, self.fontSize).render(self.name, True, (0, 0, 0))
        pygame.draw.rect(screen, pygame.Color(self.colour), self.rectangle)
        screen.blit(self.textSurface, ((self.rectangle.x), (self.rectangle.y)))

class Textbox:
    def __init__(self, text, fontName, fontSize, colour, posX, posY, boxWidth, boxHeight):
        self.text = text
        self.fontName = fontName
        self.fontSize = fontSize
        self.rectangle = pygame.Rect(posX, posY, boxWidth, boxHeight)
        self.colour = colour
        self.timer = -3000

    def setTimer(self, newValue):
        self.timer = newValue

    def getTimer(self):
        return self.timer

    def setText(self, newText):
        self.text = newText

    def draw(self, screen):
        self.textSurface = pygame.font.Font(self.fontName, self.fontSize).render(self.text, True, (255,0,0))
        pygame.draw.rect(screen, pygame.Color(self.colour), self.rectangle)
        screen.blit(self.textSurface, ((self.rectangle.x), (self.rectangle.y)))

# dropdown box class
class Dropdown:
    pass

# sudoku single box class
class MiniBox:

    #constructor
    def __init__(self, value, posX, posY):
        self.value = value
        self.rectangle = pygame.Rect(posX,posY,50,50)
        self.textSurface = baseFont.render(str(self.value), True, (0, 0, 0))
        self.active = False
        self.colour = "black"
        if self.value == 0:
            self.possibleValues = [x for x in range(1, 10)]
        else:
            self.possibleValues = [self.value]


    def setValue(self, newValue):
        self.value = newValue

    def getValue(self):
        return self.value

    def deleteValue(self):
        self.value = 0

    def getBoxPos(self):
        return (self.rectangle.x, self.rectangle.y)

    def getPossibleValues(self):
        return self.possibleValues

    def removePossibleValue(self, x):
        self.possibleValues.remove(x)

    # methods/functions
    def drawBox(self, screen):
        if self.value == 0:
            self.textSurface = baseFont.render("", True, (0, 0, 0))
        else:
            self.textSurface = baseFont.render(str(self.value), True, (0, 0, 0))
        pygame.draw.rect(screen, pygame.Color(self.colour), self.rectangle, 2)
        screen.blit(self.textSurface, ((self.rectangle.x+15), (self.rectangle.y+15)))

    def getActiveState(self):
        return self.active

    def makeActive(self):
        self.active = True

    def makeInactive(self):
        self.active = False


class Sudoku:
    def __init__(self):
        # offset from pos 0,0
        self.offset = 100
        # minibox array
        self.boxArray = [MiniBox(0, ((x % 9)*50)+self.offset, ((x // 9)*50)+self.offset ) for x in range(81)]
        # make array of big rectangles big rectangles to show big boxes
        self.bigRects = [pygame.Rect( ((x % 3)*150)+self.offset, ((x // 3)*150)+self.offset, 150, 150) for x in range(9)]

    # creates a copy of the sudoku
    def copy(self):
        copy = Sudoku()
        for box in self.getBoxArray():
            i = self.getBoxArray().index(box)
            copy.getBoxArray()[i].setValue(box.getValue())
        return copy


    # goes through boxes top to bottom and left to right and returns to the first box with value = 0
    def findNextEmpty(self):
        for box in self.boxArray:
            if box.getValue() == 0:
                return box
        return False

    def isValidNumber(self, box):
        # if value is 0 return True
        if box.getValue() == 0:
            return True
        boxIndex = self.getBoxArray().index(box)
        # check row
        startNum = (boxIndex // 9)*9
        for i in range( startNum, startNum+9 ):
            if ( box.getValue() == self.getBoxArray()[i].getValue() ) and ( not ( box is self.getBoxArray()[i] ) ):
                return False
        # check column
        startNum = boxIndex % 9
        for i in range(startNum, 81, 9):
            if ( box.getValue() == self.getBoxArray()[i].getValue() ) and ( not ( box is self.getBoxArray()[i] ) ):
                return False
        # check box
        colNum = ( ( boxIndex % 9 ) // 3 ) * 3
        rowNum = (boxIndex // 27) * 27
        boxIndices = []
        for i in range(3):
            for j in range(3):
                boxIndices.append( (rowNum+(i*9))+colNum+j )
        for i in boxIndices:
            if ( (self.getBoxArray()[i].getValue() == box.getValue()) and (not(self.getBoxArray()[i] is box)) ):
                return False
        return True

    # solves the sudoku
    def visualSolve(self, screen, cancelButton, copy):
        # hande events during solving
        for event in pygame.event.get():
            # make program quitable during solve
            if event.type == pygame.QUIT:
                exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if cancelButton.rectangle.collidepoint(event.pos):
            #         self = copy
            #         break

        # deselect any active box
        for box in self.getBoxArray():
            box.makeInactive()

        # finds next empty box
        box = self.findNextEmpty()
        # if no next empty box, sudoku is solved
        if box == False:
            return True
        # try all values from 1 to 9
        for i in range(1, 10):
            box.setValue(i)
            screen.fill((255,255,255))
            self.drawSudoku(screen)
            cancelButton.drawButton(screen)
            pygame.display.flip()
            if self.isValidNumber(box) == True:
                if self.visualSolve(screen, cancelButton, copy) == True:
                    return True
        box.deleteValue()
        return False

    def getBoxArray(self):
        return self.boxArray

    def setBoxValue(self, box, newValue, textBox):
        # set new value
        box.setValue(newValue)
        # if new number is not valid, set back to old value
        if self.isValidNumber(box) == False:
            box.deleteValue()
            textBox.setText("This value is not valid!")
            textBox.setTimer(pygame.time.get_ticks())
        else:
            textBox.setText("")

    # generate a random sudoku
    def genRandom(self):
        return

    def drawSudoku(self, screen):
        # draw big rectangles
        for bigRect in self.bigRects:
            pygame.draw.rect(screen, pygame.Color("black"), bigRect, 4)
        # draw each box
        for box in self.boxArray:
            box.drawBox(screen)
            # if a box is active, draw a red box around it
            if box.getActiveState() == True:
                boxPos = box.getBoxPos()
                pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(boxPos[0], boxPos[1], 50, 50), 2)

    # rules based solver: this will convert empty squares into a 9-long list of bools that represent whether it is logically possible
    # for a squre to contain the number that is the index of the bool

    # scanning

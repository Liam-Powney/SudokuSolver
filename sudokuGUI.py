import pygame
from sudokuClasses import *

# initialise pygame
pygame.init()
pygame.display.set_caption("xXx_SudokUwU_Solver_xXx")
screen = pygame.display.set_mode((650, 650))
baseFont = pygame.font.Font(None, 48)

# import pygame locals for easier access to key co-ordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_BACKSPACE,
    KEYDOWN,
    K_KP1,
    K_KP2,
    K_KP3,
    K_KP4,
    K_KP5,
    K_KP6,
    K_KP7,
    K_KP8,
    K_KP9,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    QUIT,
)

# make a sudoku
testSudoku = Sudoku()
# make buttons
buttonArray = []
buttonArray.append(Button("Solve Me!", None, 48, "blue", 250, 610, 155, 30))
buttonArray.append(Button("Generate Random!", None, 48, "green", 175, 565, 304, 30))
buttonArray.append(Button("Clear", None, 28, "red", 50, 50, 52, 18))
# text output area
textOut = Textbox("", None, 25, "white", 228, 75, 200, 20)

# game loop
running = True
while running:

    # controls timed text output
    if pygame.time.get_ticks() - textOut.getTimer() > 3000:
        textOut.setText("")

    # look at every event in the queue
    for event in pygame.event.get():
        # were any keys pressed?
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            # if a box is active and it's value is 0, make the new value an input value
            for box in testSudoku.getBoxArray():
                if box.getActiveState() == True:
                    ci = testSudoku.getBoxArray().index(box)
                    # if a box is active and backspace is pressed
                    if event.key == K_BACKSPACE:
                        box.deleteValue()
                    # using keypad to move active box controls
                    elif event.key == K_UP:
                        box.makeInactive()
                        if ( ci - 9 < 0):
                            ni = 80 - ci
                            testSudoku.getBoxArray()[ni].makeActive()
                            break
                        else:
                            ni = ci - 9
                            testSudoku.getBoxArray()[ni].makeActive()
                            break
                    elif event.key == K_DOWN:
                        box.makeInactive()
                        ci = testSudoku.getBoxArray().index(box)
                        if ( ci + 9 > 80 ):
                            ni = ( ci + 9 ) % 81
                            testSudoku.getBoxArray()[ni].makeActive()
                            break
                        else:
                            ni = ( ci + 9 )
                            testSudoku.getBoxArray()[ni].makeActive()
                            break
                    elif event.key == K_LEFT:
                        box.makeInactive()
                        if ( ci % 9 ) == 0:
                            ni = ci + 8
                            testSudoku.getBoxArray()[ni].makeActive()
                            break
                        else:
                           ni = ci - 1
                           testSudoku.getBoxArray()[ni].makeActive()
                           break
                    elif event.key == K_RIGHT:
                        box.makeInactive()
                        if ( ci % 9 ) == 8:
                            ni = ci - 8
                            testSudoku.getBoxArray()[ni].makeActive()
                            break
                        else:
                           ni = ci + 1
                           testSudoku.getBoxArray()[ni].makeActive()
                           break
                    # if box is active and it's value is 0
                    if box.getValue() == 0:
                        # if input number is pressed, try and change the value of the box to the input number
                        if ( event.key == K_KP1 ) or ( event.key == K_1 ) :
                            testSudoku.setBoxValue(box, 1, textOut)
                        elif ( event.key == K_KP2 ) or ( event.key == K_2 ):
                            testSudoku.setBoxValue(box, 2, textOut)
                        elif ( event.key == K_KP3 ) or ( event.key == K_3 ):
                            testSudoku.setBoxValue(box, 3, textOut)
                        elif ( event.key == K_KP4 ) or ( event.key == K_4 ):
                            testSudoku.setBoxValue(box, 4, textOut)
                        elif ( event.key == K_KP5 ) or ( event.key == K_5 ):
                            testSudoku.setBoxValue(box, 5, textOut)
                        elif ( event.key == K_KP6 ) or ( event.key == K_6 ):
                            testSudoku.setBoxValue(box, 6, textOut)
                        elif ( event.key == K_KP7 ) or ( event.key == K_7 ):
                            testSudoku.setBoxValue(box, 7, textOut)
                        elif ( event.key == K_KP8 ) or ( event.key == K_8 ):
                            testSudoku.setBoxValue(box, 8, textOut)
                        elif ( event.key == K_KP9 ) or ( event.key == K_9 ):
                            testSudoku.setBoxValue(box, 9, textOut)
                        else:
                            pass

        # if mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if mouse clicked on a box, make box active/inactive
            for box in testSudoku.getBoxArray():
                if box.rectangle.collidepoint(event.pos):
                    if box.getActiveState() == False:
                        for i in testSudoku.getBoxArray():
                            i.makeInactive()
                        box.makeActive()
                    elif box.getActiveState() == True:
                        box.makeInactive()
            # if clicked on the solve button
            for button in buttonArray:
                if ( button.getName() == "Solve Me!" ) and ( button.rectangle.collidepoint(event.pos) == True):
                    testSudoku.visualSolve(screen)
                    break
                elif ( button.getName() == "Generate Random!" )  and ( button.rectangle.collidepoint(event.pos) == True ):
                    print("This will eventually generate a random solveable sudoku lol")
                    break
                elif ( button.getName() == "Clear")  and ( button.rectangle.collidepoint(event.pos) == True ):
                    for box in testSudoku.getBoxArray():
                        box.deleteValue()
                    break



        # user clicks the window close button
        if event.type == QUIT:
            running = False

    # DRAWING SECTION OF LOOP

    # make screen white
    screen.fill((255,255,255))
    # draw sudoku
    testSudoku.drawSudoku(screen)
    # draw buttons
    for button in buttonArray:
        button.drawButton(screen)
    textOut.draw(screen)
    # draw call for pygame
    pygame.display.flip()
    #print(pygame.time.get_ticks())

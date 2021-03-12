#==============================
# Team: Kevin Sangurima, Phillip Nam, Ryan Clark
# CSC345: Computer Graphics
#   Spring 2021
# Description:
#   The goal of the assignment is to create
#   a 3D wireframe scene using Python and OpenGL.
#   The scene being created is also animated and interactive.
#
# DISCLAIMER: Due to Mac screen resolution, in line 83, winWidth and winHeight are multiplied by 2.
# For non-Mac systems, get rid of the multiplier.
#==============================

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

# These parameters define the camera's lens shape
CAM_NEAR = 0.01
CAM_FAR = 1000.0
CAM_ANGLE = 60.0

# These parameters define simple animation properties
MIN_STEP = 0.1
DEFAULT_STEP = 2.0 # How much the camera rotation increments by
ANGLE_STEP = DEFAULT_STEP
FPS = 60.0
DELAY = int(1000.0 / FPS + 0.5)

# Global Variables
winWidth = 1000
winHeight = 1000
name = b'Shapes...'
step = MIN_STEP
animate = False
angleMovement = 0 # Controls the initial angle the scene is viewed from (0)
perspectiveMode = True

# Global Variables for the car
carPosition = 0 # Car's initial x value
carDx = 0.06 # How much the car moves by
carDxMin = -7 # Car minimum bound (backwards)
carDxMax = 13 # Car maximum bound (forwards)
wheelAngle = 0 # Wheel initial angle
wheelAngleD = -2.6 # How much the wheels rotate by

def main():
    # Create the initial window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(100,100)
    glutCreateWindow(name)

    init()

    # Setup the callback returns for display and keyboard events
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(specialKeys)
    glutTimerFunc(0, timer, DELAY)

    # Enters the main loop.   
    # Displays the window and starts listening for events.
    glutMainLoop()
    return

# Shape Initialization
def init():
    global cone, tube, block
    cone = gluNewQuadric() # Cone shape
    gluQuadricDrawStyle(cone, GLU_LINE)
    tube = gluNewQuadric() # Car wheel shape, exhaust pipe, headlights
    gluQuadricDrawStyle(tube, GLU_LINE)
    block = gluNewQuadric() # Car body shape
    gluQuadricDrawStyle(block, GLU_LINE)


# Callback function used to display the scene
# Currently it just draws a simple polyline (LINE_STRIP)
def display():
    # Set the viewport to the full screen
    glViewport(0, 0, 2*winWidth, 2*winHeight) # FOR MAC: Multiplied window width & height by 2 for window to display correctly

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    if perspectiveMode:
        # Set view to Perspective Proj. (angle, aspect ratio, near/far planes)
        gluPerspective(CAM_ANGLE, winWidth/winHeight, CAM_NEAR, CAM_FAR)
    else:
        glOrtho(-winWidth/40, winWidth/40, -winHeight/40, winHeight/40, -100, 100)
    
    # Clear the Screen
    glClearColor(1.0, 1.0, 1.0, 0.0) # Clears the screen with white
    glClear(GL_COLOR_BUFFER_BIT)

    # And draw the "Scene"
    glColor3f(1.0, 1.0, 1.0)
    drawScene()

    # And show the scene
    glFlush() # Sends instructions to GPU to render the scene
    glutSwapBuffers()  # Used for double buffering

# Timer: Used to animate the scene when activated:
def timer(alarm):
    glutTimerFunc(0, timer, DELAY)   # Start alarm clock again
    if animate:
        # Advance to the next frame
        advance()
        glutPostRedisplay()

# Advance the scene one frame
# This method is responsible for the car's animation:
#   Car movement going forward and backward)
#   Wheel rotation going CW and CCW
def advance():
    global carPosition, carDx, carDxMin, carDxMax, wheelAngle, wheelAngleD
    carPosition += carDx
    wheelAngle += wheelAngleD
    # When the car goes forward...
    if carPosition >= carDxMax:
        carPosition = carDxMax
        carDx = -carDx # Car will move in the opposite direction when it reaches the max bound
        wheelAngleD = -wheelAngleD # Wheel will rotate in opposite direction
    # When the car goes backward...
    elif carPosition <= carDxMin:
        carPosition = carDxMin
        carDx = -carDx # Car will move in the opposite direction when it reaches the min bound
        wheelAngleD = -wheelAngleD # Wheel will rotate in opposite direction

def specialKeys(key, x, y):
    global ANGLE_STEP, angleMovement
    # Left arrow key rotates the scene CW about the y-axis
    if key == GLUT_KEY_LEFT:
        angleMovement += ANGLE_STEP
        glutPostRedisplay()
    # Right arrow key rotates the scene CCW about the y-axis
    elif key == GLUT_KEY_RIGHT:
        angleMovement -= ANGLE_STEP
        glutPostRedisplay()

# Callback function used to handle any key events
# Currently, it just responds to the ESC key (which quits)
# key: ASCII value of the key that was pressed
# x,y: Location of the mouse (in the window) at time of key press)
def keyboard(key, x, y):
    global angleMovement
    # Pressing escape key closes the program
    if ord(key) == 27: # ASCII code 27 = ESC-key
        glutLeaveMainLoop()
    elif ord(key) == ord('p'):
        global perspectiveMode
        print("DEBUG: Toggling perspective mode")
        perspectiveMode = not perspectiveMode
        glutPostRedisplay()
    # Pressing spacebar animates the scene
    elif ord(key) == ord(' '):
        global animate
        animate = not animate # 'not animate' means 'True'

def drawScene():
    """
    * drawScene:
    *    Draws a simple scene with a few shapes
    """
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslate(0, -7, -30)   # Move world coordinate system so it is in view
    glRotated(angleMovement, 0, 1, 0)  # Spin around y-axis
    glColor3f(0, 0, 0) # Controls wireframe color. (1,1,1) = WHITE. (0,0,0) = BLACK
    draw()

# Draw the entire scene: 2 Cones & 1 Car (Body + Wheels)
def draw():
    glPushMatrix()
    # Drawing Cones
    glTranslated(0, 0, 5) # Moving the cone farther away (-z direction) -25
    glScaled(0.45, 0.45, 0.45) # Scale the cone down
    glRotated(-90, 1, 0, 0) # Drawing the cone pointing upward
    gluCylinder(cone, 3, 0.5, 20, 10, 11) # 1st Cone
    glTranslated(0, 30, 0) # Move 2nd cone farther away from 1st cone
    gluCylinder(cone, 3, 0.5, 20, 10, 11) # 2nd Cone
    glPopMatrix()

    # Drawing Car Body (Bottom)
    glPushMatrix()
    glTranslated(carPosition + -3, 0, -5)
    glScaled(4, 0.5, 1) # Stretch body
    glRotated(-45, 0, 0, 1) # Drawing body parallel to x-axis
    gluCylinder(block, 2, 2, 7, 4, 1) # Body (Bottom)
    glPopMatrix()

    # Drawing Car MEGA Exhaust Pipe (Back Center)
    glPushMatrix()
    glTranslated(carPosition + -8.65, 0.05, -1.4)
    glScaled(1, 0.3, 0.5)
    glRotated(-90, 0, 1, 0) # Rotate exhaust pipe to face in x-axis
    gluCylinder(tube, 2, 2, 3, 50, 1) # Long exhaust pipe
    glPopMatrix()

    # Drawing Car Headlights (Front Left)
    glPushMatrix()
    glTranslated(carPosition + 2.9, 0.05, -3.5)
    glScaled(0.15, 0.3, 0.3) # Making the headlight flatter and smaller
    glRotated(-90, 0, 1, 0) # Rotate headlight so it faces in the x-axis
    gluCylinder(tube, 2, 2, 1, 50, 1) # Headlight
    glPopMatrix()

    # Drawing Car Headlights (Front Right)
    glPushMatrix()
    glTranslated(carPosition + 2.9, 0.05, 0.5)
    glScaled(0.15, 0.3, 0.3) # Making the headlight flatter and smaller
    glRotated(-90, 0, 1, 0) # Rotate headlight so it faces in the x-axis
    gluCylinder(tube, 2, 2, 1, 50, 1) # Headlight
    glPopMatrix()

    # Drawing Car Body (Top)
    glPushMatrix()
    glTranslated(carPosition + 0, 1.45, -5)
    glScaled(0.8, 0.5, 1)
    glRotated(-45, 0, 0, 1) # Drawing body parallel to x-axis
    gluCylinder(block, 2, 2, 7, 4, 1) # Body (Top)
    glPopMatrix()

    # Drawing Car Wheel (Front Right)
    glPushMatrix()
    glTranslated(carPosition + 1, 0, 2)
    glScaled(1, 1, 0.8)
    glRotated(wheelAngle, 0, 0, 1)
    gluCylinder(tube, 1, 1, 1, 10, 5) # Wheel
    glPopMatrix()

    # Drawing Car Wheel (Front Left)
    glPushMatrix()
    glTranslated(carPosition + 1, 0, -5.8)
    glScaled(1, 1, 0.8)
    glRotated(wheelAngle, 0, 0, 1)
    gluCylinder(tube, 1, 1, 1, 10, 5) # Wheel
    glPopMatrix()

    # Drawing Car Wheel (Back Right)
    glPushMatrix()
    glTranslated(carPosition + -7, 0, 2)
    glScaled(1, 1, 0.8)
    glRotated(wheelAngle, 0, 0, 1)
    gluCylinder(tube, 1, 1, 1, 10, 5) # Wheel
    glPopMatrix()

    # Drawing Car Wheel (Back Left)
    glPushMatrix()
    glTranslated(carPosition + -7, 0, -5.8)
    glScaled(1, 1, 0.8)
    glRotated(wheelAngle, 0, 0, 1)
    gluCylinder(tube, 1, 1, 1, 10, 5) # Wheel
    glPopMatrix()


#===============================
# SHAPE NOTES:
#
#   gluCylinder(quadric, base r, top r, height (along z), slices (around), stacks (towards height))
#
#   Cone: Slices = 10, Stacks = 11
#   Block:
#   Wheels: Slices = 10 , Stacks = 5
#===============================

if __name__ == '__main__': main()
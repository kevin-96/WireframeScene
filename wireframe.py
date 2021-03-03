#==============================
# TEAM MEMBERS NAMES GO HERE
# CSC345: Computer Graphics
#   Spring 2021
# Description:
#   The goal of the assignment is to create
#   a 3D wireframe scene using Python and OpenGL.
#   The scene being created is also animated and interactive.
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
DEFAULT_STEP = 0.5 # Controls the rotation speed
ANGLE_STEP = DEFAULT_STEP
FPS = 60.0
DELAY = int(1000.0 / FPS + 0.5)

# Global Variables
winWidth = 1000
winHeight = 1000
name = b'Shapes...'
step = MIN_STEP
animate = False
angleMovement = 0
perspectiveMode = True

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
    global cone, wheel, block
    cone = gluNewQuadric() # Cone shape
    gluQuadricDrawStyle(cone, GLU_LINE)
    wheel = gluNewQuadric() # Car wheel shape
    gluQuadricDrawStyle(wheel, GLU_LINE)
    block = gluNewQuadric() # Car body shape
    gluQuadricDrawStyle(block, GLU_LINE)


# Callback function used to display the scene
# Currently it just draws a simple polyline (LINE_STRIP)
def display():
    # Set the viewport to the full screen
    glViewport(0, 0, winWidth, winHeight)

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
    glFlush()
    glutSwapBuffers()  # needed for double buffering!

# Timer: Used to animate the scene when activated:
def timer(alarm):
    glutTimerFunc(0, timer, DELAY)   # Start alarm clock agani
    if animate:
        # Advance to the next frame
        advance()
        glutPostRedisplay()

#===============================
# SHAPE NOTES
#   Cone: Slices = 10, Stacks = 11
#   Block:
#   Wheel:
#===============================
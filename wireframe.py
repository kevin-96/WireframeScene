#==============================
# Team: Kevin Sangurima, Phillip Nam, Ryan Clark
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
DEFAULT_STEP = 1.5 # Controls the rotation speed (when animated)
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
    glViewport(0, 0, 2*winWidth, 2*winHeight) # For Mac: Multiply window width & height by 2 in order for window to display correctly

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
def advance():
    global angleMovement
    angleMovement += ANGLE_STEP
    if angleMovement >= 360:
        angleMovement -= 360 # So doesn't get too large
    elif angleMovement < 0:
        angleMovement += 360

# Allows the use of arrow keys to control the camera angle
def specialKeys(key, x, y):
	global ANGLE_STEP
	if key == GLUT_KEY_LEFT:
		ANGLE_STEP += DEFAULT_STEP
	elif key == GLUT_KEY_RIGHT:
		ANGLE_STEP -= DEFAULT_STEP

# Callback function used to handle any key events
# Currently, it just responds to the ESC key (which quits)
# key: ASCII value of the key that was pressed
# x,y: Location of the mouse (in the window) at time of key press)
def keyboard(key, x, y):
    if ord(key) == 27:  # ASCII code 27 = ESC-key
        glutLeaveMainLoop()
    elif ord(key) == ord('p'):
        global perspectiveMode
        print("DEBUG: Toggling perspective mode")
        perspectiveMode = not perspectiveMode
        glutPostRedisplay()
    elif ord(key) == ord(' '): # Pressing spacebar animates the scene
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

# Draw the entire scene: 2 Cones & 1 Car
def draw():
    glPushMatrix()
    # Cones
    glTranslated(0, 0, 5) # Moving the cone farther away (-z direction) -25
    glScaled(0.45, 0.45, 0.45) # Scale the cone down
    glRotated(-90, 1, 0, 0) # Drawing the cone pointing upward
    gluCylinder(cone, 3, 0.5, 20, 10, 11) # 1st Cone
    glTranslated(0, 30, 0) # Move 2nd cone farther away from 1st cone
    gluCylinder(cone, 3, 0.5, 20, 10, 11) # 2nd Cone
    glPopMatrix()

#===============================
# gluCylinder(quadric, base r, top r, height (along z), slices (around), stacks (towards height))
#
# SHAPE NOTES
#   Cone: Slices = 10, Stacks = 11
#   Block:
#   Wheels:
#===============================

if __name__ == '__main__': main()
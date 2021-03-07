#==============================
# Christian Duncan
# CSC345: Computer Graphics
#   Spring 2021
# Description:
#   Demonstrates use of gluCylinder and gluSphere to draw
#   3-d objects.
#
# THIS FILE IS FOR REFERENCE ONLY!!!
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
DEFAULT_STEP = 0.2 # Controls the rotation speed
ANGLE_STEP = DEFAULT_STEP
FPS = 60.0
DELAY = int(1000.0 / FPS + 0.5)

# Global (Module) Variables (ARGH!)
winWidth = 1000
winHeight = 1000
name = b'Shapes...'
step = MIN_STEP
animate = False
angleMovement = 0
perspectiveMode = True
fire = False
bulletDistance = 0
BULLET_SPEED = 0.5

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

# Any initialization material to do...
def init():
    global tube, ball
    tube = gluNewQuadric()
    gluQuadricDrawStyle(tube, GLU_LINE)
    ball = gluNewQuadric()
    gluQuadricDrawStyle(ball, GLU_LINE)


# Callback function used to display the scene
# Currently it just draws a simple polyline (LINE_STRIP)
def display():
    # Set the viewport to the full screen
    glViewport(0, 0, 2*winWidth, 2*winHeight) # For Mac: Multiply window width & height by 2

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

# Advance the scene one frame
def advance():
    global angleMovement, bulletDistance, fire
    angleMovement += ANGLE_STEP
    if angleMovement >= 360:
        angleMovement -= 360 # So doesn't get too large
    elif angleMovement < 0:
        angleMovement += 360    
    if fire:
    	bulletDistance += BULLET_SPEED
    	if bulletDistance > CAM_FAR:
    		bulletDistance = 0
    		fire = False
		
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
    elif ord(key) == ord(' '):
        global animate
        animate = not animate
    elif key == b'f':
    	global fire
    	fire = True

def drawScene():
    """
    * drawScene:
    *    Draws a simple scene with a few shapes
    """
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslate(0, -3, -20)   # Move world coordinate system so it is in view
    glRotated(angleMovement, 0, 1, 0)  # Spin around y-axis
    glColor3f(0, 0, 0) # Controls wireframe color. (1,1,1) = WHITE. (0,0,0) = BLACK
    draw() 

# Draw the entire scene - house + coordinate frame    
def draw():
    glPushMatrix()
    gluCylinder(tube, 3, 3, 10, 40, 5)  # quadric, base r, top r, height (along z), slices (around), stacks (towards height)
    gluCylinder(tube, 3, 1, 10, 10, 5)
    glPushMatrix()
    glTranslated(0, 0, bulletDistance)
    glScaled(1, 1, 2)
    gluSphere(ball, 0.9, 10, 10)
    glPopMatrix()
    glPopMatrix()
    
if __name__ == '__main__': main()

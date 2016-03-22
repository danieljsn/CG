#!/bin/python

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Reta:
	def __init__(self,x1,y1,x2,y2):
		self.x1=x1
		self.y1=y1
		self.x2=x2
		self.y2=y2

retas=[]
movendo = False
posSaved = {}

def entre(a,b,c):
	if (a < c):
		if (a <= b <= c):
			return True
	else:
		if (c <= b <= a):
			return True
	return False

def calculateIntersection():
	global retas
	det = ((retas[0].x1 - retas[0].x2)*(retas[1].y1 - retas[1].y2) - (retas[0].y1 - retas[0].y2)*(retas[1].x1 - retas[1].x2))
	if det == 0:
		return -1,-1
	else:
		x = ((retas[0].x1*retas[0].y2 - retas[0].y1*retas[0].x2)*(retas[1].x1 - retas[1].x2) - (retas[0].x1 - retas[0].x2)*(retas[1].x1*retas[1].y2 - retas[1].y1*retas[1].x2))/det
		y = ((retas[0].x1*retas[0].y2 - retas[0].y1*retas[0].x2)*(retas[1].y1 - retas[1].y2) - (retas[0].y1 - retas[0].y2)*(retas[1].x1*retas[1].y2 - retas[1].y1*retas[1].x2))/det

		if (entre(retas[0].x1,x,retas[0].x2) and entre(retas[0].y1,y,retas[0].y2)):
			if (entre(retas[1].x1,x,retas[1].x2) and entre(retas[1].y1,y,retas[1].y2)):
				return x,y
			else:
				return -1,-1
		else:
			return -1,-1

def initFun():
	glClearColor(1.0,1.0,1.0,0.0)
	glColor3f(0.0,0.0, 0.0)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(0.0,640.0,0.0,480.0)
    

def displayFun():
	global retas
	glClear(GL_COLOR_BUFFER_BIT)
	glLineWidth(3.0)
	glBegin(GL_LINES)
	glColor3f(0,0,0)
	for r in retas:
		glVertex2i(r.x1,r.y1)
		glVertex2i(r.x2,r.y2)
	glEnd()
	glPointSize(6.0)
	glBegin(GL_POINTS)
	glColor3f(0,0,0)
	for r in retas:
		glVertex2i(r.x1,r.y1)
		glVertex2i(r.x2,r.y2)
	glColor3f(255,0,0)
	x,y = calculateIntersection()
	if (x != -1 and y != -1):
		glVertex2f(x,y)
	glEnd()
	glFlush()

def mouseFun(button,state,x,y):
	global retas
	global movendo
	global posSaved
	#print("mouse at x = " + str(x) + " y = " + str(y))
	if button==GLUT_LEFT_BUTTON and state == GLUT_DOWN:
		for r in retas:
			if ((x-3 <= r.x1 <= x+3) and ((480-y-3) <= r.y1 <= (480-y+3))):
				posSaved = {retas.index(r):1}
				#print(posSaved)
				movendo = True
			elif ((x-3 <= r.x2 <= x+3) and ((480-y-3) <= r.y2 <= (480-y+3))):
				posSaved = {retas.index(r):2}
				#print(posSaved)
				movendo = True
	if button==GLUT_LEFT_BUTTON and state == GLUT_UP:
		if (movendo == True):
			if (posSaved.values()[0] == 1):
				#print("movendo reta 1 para x = " + str(x) + " y = " + str(y))
				retas[posSaved.keys()[0]].x1 = x
				retas[posSaved.keys()[0]].y1 = 480 - y
				movendo = False
			elif (posSaved.values()[0] == 2):
				#print("movendo reta 2 para x = " + str(x) + " y = " + str(y))
				retas[posSaved.keys()[0]].x2 = x
				retas[posSaved.keys()[0]].y2 = 480 - y
				movendo = False
	glutPostRedisplay()

def mouseMovement(x,y):
	global movendo
	if (movendo == True):
		if (posSaved.values()[0] == 1):
			#print("movendo reta 1 para x = " + str(x) + " y = " + str(y))
			retas[posSaved.keys()[0]].x1 = x
			retas[posSaved.keys()[0]].y1 = 480 - y
		elif (posSaved.values()[0] == 2):
			#print("movendo reta 2 para x = " + str(x) + " y = " + str(y))
			retas[posSaved.keys()[0]].x2 = x
			retas[posSaved.keys()[0]].y2 = 480 - y

	glutPostRedisplay()

def resize(w,h):
	glutReshapeWindow(640,480)

if __name__ == '__main__':
	r=Reta(310,310,400,400)
	retas.append(r)
	r=Reta(350,310,350,450)
	retas.append(r)

	glutInit()
	glutInitWindowSize(640,480)
	glutCreateWindow("Polyline")
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutDisplayFunc(displayFun)
	glutMouseFunc(mouseFun)
	glutMotionFunc(mouseMovement)
	glutReshapeFunc(resize)
	initFun()
	glutMainLoop()

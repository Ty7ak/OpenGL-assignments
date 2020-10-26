from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import numpy
import random

WELCOMING_MESSAGE = "Maciej Tylak 248884 - Zadanie 2 \n"
CONTROLS = "Sterowanie: \n" \
           "p - punkty \n" \
           "l - linie \n" \
           "t - trójkąty \n" \
           "1 - obrót wokół osi y \n" \
           "2 - obrót wokół osi x \n"
print(WELCOMING_MESSAGE)

#  Zapytanie użytkownika o liczbę podziałów
n = int(input("Podaj liczbę podziałów: "))
print(CONTROLS)

#  Globale zmienne
colors = numpy.zeros((n + 1, n + 1), dtype=object)
spin_axis = 0
model = 1
theta = [0.0, 0.0, 0.0]


#  Funkcja rysująca układ współrzędnych
def axes():
    xmin = (-5.0, 0.0, 0.0)
    xmax = (5.0, 0.0, 0.0)

    ymin = (0.0, -5.0, 0.0)
    ymax = (0.0, 5.0, 0.0)

    zmin = (0.0, 0.0, -5.0)
    zmax = (0.0, 0.0, 5.0)

    glColor3f(1.0, 0.0, 0.0)  # czerwony
    glBegin(GL_LINES)
    glVertex3fv(xmin)
    glVertex3fv(xmax)
    glEnd()

    glColor3f(0.0, 1.0, 0.0)  # zielony
    glBegin(GL_LINES)
    glVertex3fv(ymin)
    glVertex3fv(ymax)
    glEnd()

    glColor3f(0.0, 0.0, 1.0)  # niebieski
    glBegin(GL_LINES)
    glVertex3fv(zmin)
    glVertex3fv(zmax)
    glEnd()


def egg():
    # coordinates_matrx - macierz zawierająca współrzędne punktów 3D
    coordinates_matrix = numpy.zeros((n+1, n+1), dtype=object)
    for i in range(0, n+1):
        for j in range(0, n+1):
            u = i/n
            v = j/n

            x_coords = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u)*(math.cos(math.pi*v))
            y_coords = 160*(u**4) - 320*(u**3) + 160*(u**2)
            z_coords = (-90*(u**5) + 225*(u**4) - 270*(u**3) + 180*(u**2) - 45*u)*(math.sin(math.pi*v))

            coordinates_matrix[i][j] = (x_coords, y_coords - 4, z_coords)  # y - 4 w celach prezentacji na osi

    #  rysowanie punktów
    if model == 1:
        for i in range(0, n):
            for j in range(0, n):
                glColor3f(1, 1, 0)  # żółty
                #  rysowanie punktów z macierzy coordinates_matrix
                glBegin(GL_POINTS)
                glVertex3fv(coordinates_matrix[i][j])
                glEnd()

    #  rysowanie linii
    if model == 2:
        for i in range(1, n+1):
            for j in range(1, n+1):
                glColor3f(0, 1, 0)  # zielony
                #  rysowanie linii poziomych
                glBegin(GL_LINES)
                glVertex3fv(coordinates_matrix[i][j-1])
                glVertex3fv(coordinates_matrix[i][j])
                #  rysowanie linii pionowych
                glVertex3fv(coordinates_matrix[i][j])
                glVertex3fv(coordinates_matrix[i-1][j])
                #  rysowanie linii ukośnych
                glVertex3fv(coordinates_matrix[i][j])
                glVertex3fv(coordinates_matrix[i-1][j-1])
                glEnd()

    #  rysowanie trójkątów
    #  (po podzieleniu płaszczyzny na mniejsze kwadraty, każdy mniejszy
    #  kwadrat można podzielić na dwa trójkąty - dolny i górny)
    #  kolory wybierane są z macierzy colors (losowane w main())
    if model == 3:
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                glBegin(GL_TRIANGLES)
                # rysownaie trójkątów dolnych
                glColor3fv(colors[i-1][j-1])
                glVertex3fv(coordinates_matrix[i-1][j-1])
                glColor3fv(colors[i][j-1])
                glVertex3fv(coordinates_matrix[i][j-1])
                glColor3fv(colors[i][j])
                glVertex3fv(coordinates_matrix[i][j])
                # rysowanie trójkątów górnych
                glColor3fv(colors[i-1][j-1])
                glVertex3fv(coordinates_matrix[i-1][j-1])
                glColor3fv(colors[i-1][j])
                glVertex3fv(coordinates_matrix[i-1][j])
                glColor3fv(colors[i][j])
                glVertex3fv(coordinates_matrix[i][j])

                glEnd()


#  funkcja odpowiadająca za ustawienie kątu obrotu jajka
def spin_egg():
    global theta
    if theta[0] > 360.0:
        theta[0] -= 360.0
    if theta[1] > 360.0:
        theta[1] -= 360.0

    # 0 - domyślnie (wokół y), 1 - wokół y, 2 - wokół x
    if spin_axis == 0:
        theta[0] -= 0.0
        theta[1] -= 1
    if spin_axis == 1:
        theta[0] -= 0.0
        theta[1] -= 1
    if spin_axis == 2:
        theta[0] -= 1
        theta[1] -= 0.0

    glutPostRedisplay()


#  funkcja odpowiadająca za zczytywanie znaków z klawiatury użytkownika
def keys(key, x, y):
    # model 1 - punkty (domyślnie), 2 - linie, 3 - trójkąty
    global model
    if key == bytes(b'p'):
        model = 1
    if key == bytes(b'l'):
        model = 2
    if key == bytes(b't'):
        model = 3

    # spin_axis 1 - wokół osi y (domyślnie), 2 - wokół osi y
    global spin_axis
    if key == bytes(b'1'):
        spin_axis = 1
    if key == bytes(b'2'):
        spin_axis = 2

    render_scene()


# Funkcja renderująca scenę
def render_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    axes()
    glRotatef(theta[0], 1.0, 0.0, 0.0)
    glRotatef(theta[1], 0.0, 1.0, 0.0)
    glRotatef(theta[2], 0.0, 0.0, 1.0)
    egg()
    glFlush()
    glutSwapBuffers()


# Funkcja skalująca obiekt do rozmiaru okna
def change_size(horizontal, vertical):
    if vertical == 0:
        vertical = 1

    glViewport(0, 0, horizontal, vertical)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = horizontal / vertical

    if horizontal <= vertical:
        glOrtho(-7.5, 7.5, -7.5/aspect_ratio, 7.5/aspect_ratio, 10.0, -10.0)
    else:
        glOrtho(-7.5*aspect_ratio, 7.5*aspect_ratio, -7.5, 7.5, 10.0, -10.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    #  wypełnienie macierzy colors losowymi wartosciami RGB
    #
    for i in range(0, n + 1):
        for j in range(0, n + 1):
            colors[i][j] = (random.random(), random.random(), random.random())
    glutInit()
    glutIdleFunc(spin_egg)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(600, 600)
    glutCreateWindow("Zadanie 2. - Jajo")
    glutDisplayFunc(render_scene)
    glutReshapeFunc(change_size)
    glutKeyboardFunc(keys)
    glEnable(GL_DEPTH_TEST)
    glutMainLoop()


if __name__ == '__main__':
    main()

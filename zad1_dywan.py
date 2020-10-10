from OpenGL.GL import *
from OpenGL.GLUT import *
import random

WELCOMING_MESSAGE = "Maciej Tylak 248884 - Zadanie 1 \n"

# Zwiększa maksymalny losowy offset kwadratów (0 - brak offsetu)
# !Zaleca się zmniejszyć dla dywanów o poziomie > 4!
DEFORMATION_INTENSITY = 10

print(WELCOMING_MESSAGE)
carpet_layers = int(input("Choose the number of layers: "))


# Funkcja rysująca dywan Sierpinskiego
def draw_sierpinski(length, x, y, layers):
    # length - długość boku kwadratu
    # x, y - współrzędne wiezrchołków kwadratu
    # layers - ilość poziomów dywanu

    # Zagnieżdżone funkcje dzielą kwadrat na 9^N mniejszych
    # kwadratów i określają ich współrzędne, pomijając środkowy

    if layers > 0:
        length = length / 3

        draw_sierpinski(length, x, y, layers - 1)
        draw_sierpinski(length, x - length, y, layers - 1)
        draw_sierpinski(length, x - 2 * length, y, layers - 1)

        draw_sierpinski(length, x, y - length, layers - 1)
        draw_sierpinski(length, x - 2 * length, y - length, layers - 1)

        draw_sierpinski(length, x, y - 2 * length, layers - 1)
        draw_sierpinski(length, x - length, y - 2 * length, layers - 1)
        draw_sierpinski(length, x - 2 * length, y - 2 * length, layers - 1)

    # Po podzieleniu, pojedynczny kwadrat jest rysowany i kolorowany, a następnie
    # wywoływana jest kolejna zagnieżdżona funkcja draw_sierpinski

    else:

        # Zmienna deformation skaluje DEFORMATION_INTENSITY
        deformation = random.randint(-DEFORMATION_INTENSITY, DEFORMATION_INTENSITY) / length

        glBegin(GL_POLYGON)

        # Kolory wierzchołków są losowe, a do ich położenia dodawany jest offset
        glColor3f(random.random(), random.random(), random.random())
        glVertex2f(x + deformation, y + deformation)

        glColor3f(random.random(), random.random(), random.random())
        glVertex2f(x + deformation, y - length + deformation)

        glColor3f(random.random(), random.random(), random.random())
        glVertex2f(x - length + deformation, y - length + deformation)

        glColor3f(random.random(), random.random(), random.random())
        glVertex2f(x - length + deformation, y + deformation)

        glEnd()


# Funkcja renderująca scenę
def render_scene():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_sierpinski(360, 180, 180, carpet_layers)
    glFlush()


# Funkcja skalująca obiekt do rozmiaru okna
def change_size(horizontal, vertical):
    if vertical == 0:
        vertical = 1

    glViewport(0, 0, horizontal, vertical)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = horizontal / vertical

    if horizontal <= vertical:
        glOrtho(-200.0, 200.0, -200.0 / aspect_ratio, 200.0 / aspect_ratio, 1.0, -1.0)
    else:
        glOrtho(-200.0 * aspect_ratio, 200.0 * aspect_ratio, -200.0, 200.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(600, 600)
    glutCreateWindow("Zadanie 1. Sierpinski carpet")
    glutDisplayFunc(render_scene)
    glutReshapeFunc(change_size)
    glClearColor(0.25, 0.25, 0.25, 1.0)
    glutMainLoop()


if __name__ == '__main__':
    main()

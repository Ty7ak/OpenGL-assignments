from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import numpy

WELCOMING_MESSAGE = "Maciej Tylak 248884 - Zadanie 4 \n"
CONTROLS = "Sterowanie: \n" \
           "1 - obrot wokół osi y \n" \
           "2 - obrot wokół osi x \n" \
           "q - swiatło 1 (punktowe, nad jajkiem) \n" \
           "w - swiatło 2 (kierunkowe, wokół jajka)"
print(WELCOMING_MESSAGE)

#  Zapytanie uzytkownika o liczbe podziałow
n = int(input("Podaj liczbę podziałów: "))
print(CONTROLS)

#  GLOBALNE ZMIENNE
egg_color = [1.0, 1.0, 1.0]
spin_axis = 0
model = 1
theta = [0.0, 0.0, 0.0]

#  Swiatlo
light_radius = 10
light_pos = [0.0, 0.0, -5.0, 1.0]
light_theta = 0.0
light_phi = 0.0


def egg():
    # coordinates_matrx - macierz zawierajaca wspołrzedne punktow 3D
    coordinates_matrix = numpy.zeros((n + 1, n + 1), dtype=object)
    for i in range(0, n + 1):
        for j in range(0, n + 1):
            u = i / n
            v = j / n

            x_coords = (-90 * (u ** 5) + 225 * (u ** 4) - 270 * (u ** 3) + 180 * (u ** 2) - 45 * u) * (
                math.cos(math.pi * v))
            y_coords = 160 * (u ** 4) - 320 * (u ** 3) + 160 * (u ** 2)
            z_coords = (-90 * (u ** 5) + 225 * (u ** 4) - 270 * (u ** 3) + 180 * (u ** 2) - 45 * u) * (
                math.sin(math.pi * v))

            coordinates_matrix[i][j] = (x_coords, y_coords - 4, z_coords)  # y - 4 w celach prezentacji

    #  Rysowanie trojkatow + wektorow normalnych
    vector_n = [0.0, 0.0, 0.0]
    vector_normalized = numpy.zeros((n + 1, n + 1), dtype=object)
    if model == 1:
        for i in range(0, n + 1):
            for j in range(0, n + 1):
                u = i / n
                v = j / n

                x_u = (-450 * (u ** 4) + 900 * (u ** 3) - 810 * (u ** 2) + 360 * u - 45) \
                    * math.cos(math.pi * v)

                x_v = math.pi * (90 * (u ** 5) - 225 * (u ** 4) + 270 * (u ** 3) - 180 * (u ** 2) + 45 * u) \
                    * math.sin(math.pi * v)

                y_u = 640 * (u ** 3) - 960 * (u ** 2) + 320 * u

                y_v = 0

                z_u = (-450 * (u ** 4) + 900 * (u ** 3) - 810 * (u ** 2) + 360 * u - 45) \
                    * math.sin(math.pi * v)

                z_v = - math.pi * (90 * (u ** 5) - 225 * (u ** 4) + 270 * (u ** 3) - 180 * (u ** 2) + 45 * u) \
                    * math.cos(math.pi * v)

                vector_n[0] = y_u * z_v - z_u * y_v
                vector_n[1] = z_u * x_v - x_u * z_v
                vector_n[2] = x_u * y_v - y_u * x_v

                vector_length = math.sqrt(vector_n[0] ** 2 + vector_n[1] ** 2 + vector_n[2] ** 2)

                # Normalizacja wektora vector_n
                if i == 0 or i == n:
                    vector_normalized[i][j] = (0, -1, 0)

                elif i < n / 2:
                    vector_normalized[i][j] = (
                        vector_n[0] / vector_length,
                        vector_n[1] / vector_length,
                        vector_n[2] / vector_length)

                elif i > n / 2:
                    vector_normalized[i][j] = (
                        -1 * vector_n[0] / vector_length,
                        -1 * vector_n[1] / vector_length,
                        -1 * vector_n[2] / vector_length)

                else:
                    vector_normalized[i][j] = (0, 1, 0)

        for i in range(0, n + 1):
            for j in range(0, n + 1):
                glBegin(GL_TRIANGLES)
                # rysownaie trojkatow dolnych
                glColor3fv(egg_color)
                glNormal3fv(vector_normalized[i - 1][j - 1])
                glVertex3fv(coordinates_matrix[i - 1][j - 1])

                glNormal3fv(vector_normalized[i][j - 1])
                glVertex3fv(coordinates_matrix[i][j - 1])

                glNormal3fv(vector_normalized[i][j])
                glVertex3fv(coordinates_matrix[i][j])

                # rysowanie trojkatow gornych
                glColor3fv(egg_color)
                glNormal3fv(vector_normalized[i - 1][j - 1])
                glVertex3fv(coordinates_matrix[i - 1][j - 1])

                glNormal3fv(vector_normalized[i - 1][j])
                glVertex3fv(coordinates_matrix[i - 1][j])

                glNormal3fv(vector_normalized[i][j])
                glVertex3fv(coordinates_matrix[i][j])

                glEnd()


#  Funkcja odpowiadajaca za ustawienie katu obrotu jajka
def spin_egg():
    global theta
    if theta[0] > 360.0:
        theta[0] -= 360.0
    if theta[1] > 360.0:
        theta[1] -= 360.0

    # 0 - domyslnie (wokoł y), 1 - wokol y, 2 - wokoł x
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


#  Funkcja odpowiadajaca za zczytywanie znakow z klawiatury uzytkownika
def keys(key, x, y):
    # spin_axis 1 - wokoł osi y (domyslnie), 2 - wokoł osi y
    global spin_axis
    if key == bytes(b'1'):
        spin_axis = 1
    if key == bytes(b'2'):
        spin_axis = 2

    # q - swiatlo punktowe LIGHT0, w - swiatlo kierunkowe LIGHT1
    if key == bytes(b'q'):
        glEnable(GL_LIGHTING)
        glDisable(GL_LIGHT1)
        glEnable(GL_LIGHT0)
    if key == bytes(b'w'):
        glEnable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

    render_scene()


#  Funkcja obsługująca ruch światła
def light_rotation(rotation_speed):
    global light_theta

    light_position = [0, 0, 0, 0]
    light_position[0] = light_radius * math.cos(light_theta) * math.cos(light_phi)
    light_position[1] = light_radius * math.sin(light_phi)
    light_position[2] = light_radius * math.sin(light_theta) * math.cos(light_phi)

    light_theta += rotation_speed
    return light_position


#  Funkcja renderujaca scenę
def render_scene():
    global light_theta
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    light_position = light_rotation(0.1)

    glLightfv(GL_LIGHT1, GL_POSITION, light_position)

    glRotatef(theta[0], 1.0, 0.0, 0.0)
    glRotatef(theta[1], 0.0, 1.0, 0.0)
    glRotatef(theta[2], 0.0, 0.0, 1.0)

    egg()
    glFlush()
    glutSwapBuffers()


def my_init():
    glClearColor(0.0, 0.0, 0.0, 1.0)

    mat_ambient = [1.0, 1.0, 1.0, 1.0]
    mat_diffuse = [1.0, 1.0, 1.0, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = 20.0

    light0_position = [0.0, 10.0, 0.0, 1.0]
    light0_ambient = [0.1, 0.1, 0.1, 1.0]
    light0_diffuse = [1.0, 1.0, 1.0, 1.0]
    light0_specular = [1.0, 1.0, 1.0, 1.0]

    light1_position = [0.0, 0.0, 10.0, 1.0]
    light1_ambient = [0.1, 0.1, 0.1, 1.0]
    light1_diffuse = [1.0, 1.0, 1.0, 1.0]
    light1_specular = [1.0, 1.0, 1.0, 1.0]

    att_constant = 1.0
    att_linear = 0.05
    att_quadratic = 0.001

    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light0_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light0_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light0_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light0_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)


# Funkcja skalujaca obiekt do rozmiaru okna
def change_size(horizontal, vertical):
    if vertical == 0:
        vertical = 1

    glViewport(0, 0, horizontal, vertical)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = horizontal / vertical

    if horizontal <= vertical:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 10.0, -10.0)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 10.0, -10.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit()
    glutIdleFunc(spin_egg)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(600, 600)
    glutCreateWindow("Zadanie 4. - Swiatlo")
    glutDisplayFunc(render_scene)
    glutReshapeFunc(change_size)
    glutKeyboardFunc(keys)
    my_init()
    glutMainLoop()


if __name__ == '__main__':
    main()

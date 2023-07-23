import math
import numpy as np
import matplotlib.pyplot as plt
from environment import Env

def sinal(sinal):
    if sinal >= 0:
        return 1
    else:
        return -1
def fix_angle(ang):
    # Normaliza o ângulo para o intervalo [-2pi, 2pi]
    return (ang + math.pi) % (2 * math.pi) - math.pi
    #return (ang) % (2*math.pi)

def rotate(ang_rot):
    rotacao_finalizada = False
    if ang_rot == 0.0:
        linear = 0.0
        angular = 0.1
        rotacao_finalizada = True
    elif ang_rot > 0.0:
        linear = 0.0
        angular = 0.1
    elif ang_rot < 0.0:
        linear = 0.0
        angular = -0.1
    return linear, angular, rotacao_finalizada

def direcao(os_lados):
    if os_lados:
        return 1
    else:
        return -1

def euler_vector_angle(x1, y1, x2, y2):
    """
    Recebe a dois pontos (x1,y1),(x2,y2)
    Retorna a distancia de euler, angulo, e catetos x e y
    """
    # Cálculo do vetor
    vector_x = x2 - x1
    vector_y = y2 - y1
    
    # Cálculo da distância de Euler
    distance = math.sqrt(pow(vector_x,2)-pow(vector_y,2))
    
    # Cálculo do ângulo
    angle = math.degrees(math.atan2(vector_y, vector_x))
    
    # Cálculo do X equivalente
    x_equivalent = distance * math.cos(math.radians(angle))
    
    # Cálculo do Y equivalente
    y_equivalent = distance * math.sin(math.radians(angle))

    return distance,angle, x_equivalent, y_equivalent

def manhattan_vector_angle(x1, y1, x2, y2):
    """
    Recebe:
      a dois pontos: (x1,y1),(x2,y2)
    Retorna:
      a distancia de manhatam, angulo, e catetos x e y
    """
    # Cálculo do vetor
    vector_x = x2 - x1
    vector_y = y2 - y1
    
    # Cálculo da distância de Manhattan
    distance = abs(vector_x) + abs(vector_y)
    
    # Cálculo do ângulo
    angle = math.degrees(math.atan2(vector_y, vector_x))
    
    # Cálculo do X equivalente
    x_equivalent = distance * math.cos(math.radians(angle))
    
    # Cálculo do Y equivalente
    y_equivalent = distance * math.sin(math.radians(angle))

    return distance, angle, x_equivalent, y_equivalent



    
""" # Exemplo de uso da função
x1, y1 = 40, 2
x2, y2 = 20, 4
angle, x_equivalent, y_equivalent = manhattan_vector_angle(x1, y1, x2, y2)
# Exemplo de uso da função
x1, y1 = 40, 2
x2, y2 = 20, 4
angle, x_equivalent, y_equivalent = manhattan_vector_angle(x1, y1, x2, y2)
print(angle, x_equivalent, y_equivalent)
angle, x_equivalent, y_equivalent = euler_vector_angle(x1, y1, x2, y2)
print(angle, x_equivalent, y_equivalent)

print("Vetor: ({}, {})".format(x2 - x1, y2 - y1))
print("Distância de Manhattan: {}".format(abs(x2 - x1) + abs(y2 - y1)))
print("Distância de euler: {}".format(math.sqrt(pow(x2 - x1,2) + pow(y2 - y1,2))))
print("Ângulo: {} graus".format(angle))
print("X equivalente: {}".format(x_equivalent))
print("Y equivalente: {}".format(y_equivalent))
# Plotagem das retas
plt.plot([x1, x2], [y1, y2], 'ro-', label='Reta de Parâmetro')
plt.plot([x1, x1 + x_equivalent], [y1, y1 + y_equivalent], 'bo-', label='Reta Obtida')
# Plotagem dos catetos
plt.plot([0, x_equivalent], [0, 0], 'ro-', label='Deslocamento em X')
plt.plot([0, 0], [0, y_equivalent], 'bo-', label='Deslocamento em Y')

plt.xlabel('Deslocamento Absoluto em X')
plt.ylabel('Deslocamento Absoluto em Y')
plt.title('Deslocamento em X e Y usando Distância de Manhattan')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show() """


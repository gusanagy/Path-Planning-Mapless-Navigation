#! /usr/bin/env python3
import rospy 
from geometry_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *
from random import uniform
import math
from gazebo_msgs.msg import *
import numpy as np
import csv
import rospkg
import matplotlib.pyplot as plt
from matplotlib import cm
import time
from environment import Env
from utils_nav import *


if __name__ == "__main__":
    rospy.init_node("path_controller_node", anonymous=False)
    
    env = Env()
    state_scan = env.reset()
    action = np.zeros(2)

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)    
    r = rospy.Rate(5) # 10hz
    velocity = Twist()

    #Angulo do veiculo
    ang_env = env.ang
    #Actual goal
    f_goal = Point()
    f_goal.x = env.goal_x
    f_goal.y = env.goal_y
    #Variáveis auxiliares
    state = 0
    var = 0
    sign = 0
    rotacao_finalizada = False
    #Constantes
    trinta = (3*math.pi)/18
    while not rospy.is_shutdown():

        # Variaveis Disponíveis 
        sign = (env.heading+1)/((abs(env.heading)+1))
        nada_na_frente = min(state_scan[0:45]) > 0.3 and min(state_scan[270+45:]) > 0.3
        Tem_na_frente = min(state_scan[0:35]) < 0.25 or min(state_scan[270+45+10:]) < 0.25
        #maximo_frente = min(state_scan[0:45]) == min(state_scan[270+45:])
        #max_direita = max(state_scan[90-20:90+20]) == 0.25
        #max_esquerda = max(state_scan[270-20:270+20]) == 0.25
        #esquerda = min(state_scan[270-20:270+20])<0.25
        #direita = min(state_scan[90-20:90+20])<0.25
        #os_lados = esquerda < direita # se for verdadeiro direita, se for falso esquerda
        ang_rot = abs(round(var,2)) - abs(round(env.ang,2))
        
        #variaveis plotadas
        print(f""" 
        Lidar:
            frente sem obj:     {nada_na_frente} 
            frente com obj:     {Tem_na_frente}
            menor valor em 360: {min(state_scan)} 
            Se e menor que 0.25:{min(state_scan) > 0.25}      
        Posicao: 
            x pos : {env.position.x:.3f}, y pos : {env.position.y:.3f}
            goal x: {f_goal.x:.3f}      , goal y: {f_goal.y:.3f}
            Veiculo angulo: {env.ang}
            Goal angulo:    {env.goal_ang}
            dif ang:        {env.heading}
            add valor:      {trinta*sinal(sign)}
        Acao
            Ação: Linear:   {action[0]} Angular: {action[1]}
        Angulos
            var: {math.degrees(var)}  
            var soma:{math.degrees(fix_angle(env.ang + (trinta*sinal(sign))))}
        State: {state}
        """)

        # State Machine for navigation
        #ESTADO: Segue o alvo enquanto não há objetos na frente do robô
        if state == 0:

            if Tem_na_frente:
                action[0] = 0.0
                action[1] = 0.0
                              
                var = fix_angle(env.ang + (2*trinta*sinal(sign)))# inicializa a somatoria de angulos 
                state = 1
            else:
                    action[0] = 0.1
                    action[1] = 0.2 * env.heading #* direcao(os_lados)

        if state == 1: 
            #ESTADO: Alinhamento, alinha o robo com o angulo estabelecido, caso nao haja obstaculos na rotacao muda seu estado
            print(f"env : {round(env.ang,2)} var : {round(var,2)} difereca: {abs(round(var,2)) - abs(round(env.ang,2)) }")            
            action[0],action[1],rotacao_finalizada = rotate(ang_rot=ang_rot)

            if  nada_na_frente :
                action[0] = 0.0
                action[1] = 0.0
                state = 3
            else:
                var += trinta*sinal(sign)# adiciona mais trinta graus a rotacao do robo caso ainda haja obstaculos a frente apos a rotacao inicial
                state = 1
                
        if state == 3:
            #Estado: Avanca seguindo o obstaculo ou fugindo do obstaculo
            if min(state_scan) > 0.25 and not Tem_na_frente:#caso nao esteja proximo a nenhum objeto retorna ao estado de seguir o goal
                print(f"verdade: {min(state_scan) >= 0.25}")
                action[0] = 0.0
                action[1] = 0.0
                state = 0 
            elif Tem_na_frente:#Caso exista um objeto a frente volta ao estado de rotacionar
                action[0] = 0.0
                action[1] = 0.0
                state = 0
            else:#Avancando para se afastar do objeto
                action[0] = 0.1
                action[1] = 0.0
        env.getOdometry 
        state_scan = env.step(action)
                
        r.sleep()

# Alternativa separando os estados de alinhamento e avancar 
""" 
         if state == 1: 
            #Estado de alinhamento
            print(f"env : {round(env.ang,2)} var : {round(var,2)} difereca: {abs(round(var,2)) - abs(round(env.ang,2)) }")            
            action[0],action[1],rotacao_finalizada = rotate(ang_rot=ang_rot)
            if rotacao_finalizada:
                state = 2

        if state == 2: 
            if  nada_na_frente :
                action[0] = 0.0
                action[1] = 0.0
                state = 3
                
            else:
                var += trinta*sinal(sign)
                #var = fix_angle(var)
                state = 1 """


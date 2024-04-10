#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import pygame
from pygame.locals import *

def control_robot():
    rospy.init_node('keyboard_control_node', anonymous=True)
    pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # Frecuencia de publicación de comandos

    # Inicializar pygame
    pygame.init()
    screen = pygame.display.set_mode((400, 300))

    # Velocidades lineal y angular iniciales
    linear_speed = 0.0
    angular_speed = 0.0

    while not rospy.is_shutdown():
        # Manejo de eventos de teclado
        for event in pygame.event.get():
            if event.type == QUIT:
                rospy.signal_shutdown('Shutting down')
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    linear_speed = 0.5  # Velocidad lineal hacia adelante
                elif event.key == K_DOWN:
                    linear_speed = -0.5  # Velocidad lineal hacia atrás
                elif event.key == K_LEFT:
                    angular_speed = 0.5  # Velocidad angular izquierda
                elif event.key == K_RIGHT:
                    angular_speed = -0.5  # Velocidad angular derecha
            elif event.type == KEYUP:
                if event.key in [K_UP, K_DOWN]:
                    linear_speed = 0.0  # Detener la velocidad lineal
                elif event.key in [K_LEFT, K_RIGHT]:
                    angular_speed = 0.0  # Detener la velocidad angular

        # Crear y publicar el mensaje Twist
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.x = linear_speed
        cmd_vel_msg.angular.z = angular_speed
        pub_cmd_vel.publish(cmd_vel_msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        control_robot()
    except rospy.ROSInterruptException:
        pass

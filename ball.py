from random import random
from random import randint
import pygame
import math
from vector import Vector
from constants import WIDTH, HEIGHT


class Ball:
    def __init__(self,position,radius,color):
        self.color = color
        self.position = position
        self.radius = radius
        self.velocity = Vector(random() * 2 * math.pi, random() * 4) 
        self.scream1 = pygame.mixer.Sound("alana-aaa.mp3")
    #draws a circle within the confinements of the screen. attrs: color, coordinates, and a radius
    def draw(self,screen):
        pygame.draw.circle(screen, self.color, self.position.get_coords(), self.radius)

    #updates the position based on the old position + velocity
    def update(self):
        #self.gravity()
        self.position += self.velocity
        self.bounce_off_wall()

    #
    def bounce_off_wall(self):
        x,y = self.position.get_coords()
        if x + self.radius >= WIDTH or x- self.radius <= 0:
            self.velocity = self.velocity.reflect_over_y()
        if y + self.radius >= HEIGHT or y - self.radius <=0:
            self.velocity = self.velocity.reflect_over_x()
        #Stop the balls from going out of bounds
        #Using the Vector Class which is based on a direction and a magnitude  
        if x + self.radius >= WIDTH:
            self.position = Vector.build_from_xy(WIDTH  - self.radius, y)
        if x - self.radius <= 0:
            self.position = Vector.build_from_xy(self.radius, y)
        if y + self.radius >= HEIGHT:
            self.position = Vector.build_from_xy(x, HEIGHT - self.radius)
        if y - self.radius <= 0:
            self.position = Vector.build_from_xy(x, self.radius)



    #adds gravity to the velocity
    def gravity(self):
        #gravity is a vector. it points down
        gravity = Vector(math.pi/2,1)
        self.velocity += gravity

    def distance_check(self,other):
        delta_vector = other.position - self.position
        return delta_vector.get_magnitude()
    
    #Creates gravity to attract the balls to each other
    def ball_attraction(self,other):
        delta_vector = other.position - self.position
        delta_vector.magnitude = 1
        self.velocity += delta_vector.scale(0.1)
    
    #Checks if the distance between the two balls is equal to their combined radiuses to determine collision
    def collision_check(self,other):
        return self.distance_check(other) <= self.radius + other.radius
    def angle_check(self,other):
        delta_vector = other.position - self.position
        return delta_vector.get_direction()
    def angle_of_velocity(self):
        return self.velocity.get_direction()
    def bounce_off(bawl,other_bawl):
        normal_angle = bawl.angle_check(other_bawl) + math.pi/2
        angle_of_velocity = bawl.angle_of_velocity()
        angle_of_incidence = angle_of_velocity - normal_angle
        new_velocity_angle = normal_angle - angle_of_incidence 
        new_velocity = Vector(new_velocity_angle,bawl.velocity.get_magnitude())
        bawl.velocity = new_velocity
        overlap = bawl.distance_check(other_bawl) - (bawl.radius + other_bawl.radius)
        if overlap < 0:
            normal = other_bawl.position - bawl.position
            normal.magnitude = 1
            
            push_distance = overlap * 0.5
            bawl.position += normal.scale(push_distance)
    def split(self):
        new_ball = Ball(self.position + self.radius/2, self.radius/2, self.color)
        new_ball2 = Ball(self.position - self.radius/2, self.radius/2, self.color)
        new_ball2.velocity = new_ball.velocity.scale(-1)
        return new_ball, new_ball2
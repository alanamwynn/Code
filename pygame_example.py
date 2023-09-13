import pygame
from pygame.time import Clock
import math
from random import randint,random
from ball import Ball
from vector import Vector
import os
from constants import WIDTH, HEIGHT, GRAVITY_STRENGTH, MIN_BALL_RADIUS, MIN_SPLIT_SPEED

def hex_to_rgb(hex_string):
    first = hex_string[:2]
    second = hex_string[2:4]
    third = hex_string[4:6]
    # print(first,second,third)
    return int(first,16),int(second,16),int(third,16)

def angle_to_coord(angle, distance):
    rads = math.radians(angle)
    return distance * math.cos(rads), distance * math.sin(rads)

#Alias for angle to coord;dif concept, same math
def make_vector(angle, distance):
    return distance * math.cos(angle), distance * math.sin(angle)

# Makes a random color using fixed rgb values if provided, otherwise random
def random_color(red=None, green=None, blue=None):
    if red is None:
        red = randint(0, 255)
    if green is None:
        green = randint(0, 255)
    if blue is None:
        blue = randint(0, 255)
    return (red, green, blue)


# Initialize Pygame
pygame.init()
clock = Clock()

# Create a window of 800x600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.set_num_channels(100)
x = int("F", 16)
circle_size = 2*math.pi

# Window title
pygame.display.set_caption("Mistress Ada's Perfect Circle")


max_radius = 100
bawls = []

#Create a number of balls within the specified range and apply random attrs using randint
for ball in range(6):
   x = randint(max_radius,WIDTH - max_radius)
   y = randint(max_radius,HEIGHT - max_radius)
   position = Vector.build_from_xy(x, y)
   bawls.append(Ball(position, randint(0,max_radius), (randint(0,255), randint(0,255), randint(0,255))))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Clear the screen with grey
    screen.fill((125, 125, 125))

    balls_to_add = []
    balls_to_remove = []
    #Iterate over the list of balls
    for bawl_i in range(len(bawls)):
        bawl = bawls[bawl_i]
        #Update covers the core physics of the balls
        bawl.update()
        bawl.draw(screen)
        #Iterate over the list of balls again
        for other_bawl_i in range(bawl_i + 1, len(bawls)):
            other_bawl = bawls[other_bawl_i]
            if bawl not in balls_to_remove and other_bawl not in balls_to_remove:
            #Method that causes balls to gravitate towards each other
                bawl.ball_attraction(other_bawl)
                other_bawl.ball_attraction(bawl)

            #the child balls manitain the same color as the parent ball initially/rest of sim/end color randomization post collision?

                #if the balls collide, they change colors, yell, and bounce
                if bawl.collision_check(other_bawl):

                    bawl.scream()
                    other_bawl.scream()
                    bawl.bounce_off(other_bawl)  
                    other_bawl.bounce_off(bawl)
                    #If two balls collide, they each get split into 2 smaller balls if they are big enough
                    #The original balls are queued for removal and the new balls are queued for addition
                    if bawl.velocity.magnitude > MIN_SPLIT_SPEED or other_bawl.velocity.magnitude > MIN_SPLIT_SPEED:
                        if bawl.radius > MIN_BALL_RADIUS * 2:
                            if other_bawl.velocity.magnitude > bawl.velocity.magnitude:
                                new_ball, new_ball2 = bawl.split()
                                balls_to_add.append(new_ball)
                                balls_to_add.append(new_ball2)
                                balls_to_remove.append(bawl)
                        if other_bawl.radius > MIN_BALL_RADIUS *2:
                            if bawl.velocity.magnitude > other_bawl.velocity.magnitude:
                                new_ball, new_ball2 = other_bawl.split()
                                balls_to_add.append(new_ball)
                                balls_to_add.append(new_ball2)
                                balls_to_remove.append(other_bawl)
                    else:   
                    #if the original 2 balls are small enough, they will combine into a bigger ball
                        if bawl.ball_mass() > other_bawl.ball_mass():
                            bawl.radius += other_bawl.radius
                            balls_to_remove.append(other_bawl)
                        if other_bawl.ball_mass() > bawl.ball_mass():
                            other_bawl.radius += bawl.radius
                            balls_to_remove.append(bawl)
                        
                #make attraction proportional to the size of the ball

    # #After the while loop, new balls that are a result of collision are added to the list of balls to add
    # #their original balls are added to balls to remove
    for ball in balls_to_add:
        bawls.append(ball)
        ball.color = random_color()
    for ball in balls_to_remove:
        if ball in bawls:
            bawls.remove(ball)
    print(len(bawls))
    
                
                
                
    # Update the screen
    pygame.display.update()
    clock.tick(30)

# Quit Pygame
pygame.quit()


#More Ideas for this Pygame:

    # bouncing off eachother that mimics irl physics
    # repulsion
    # spring-like (Parabolic force curve)
    # sudden elimination or combination by contact (agario)

#more dunder methods to add/compare balls


# orange_ball = Ball(400, 300, 50, hex_to_rgb("FF4500"))
# blue_ball = Ball(orange_ball.x, orange_ball.y, 25,hex_to_rgb("0000CD"))

#12 new balls drawn every frame at random locations, colors, and sizes
#Do I need a new variable to generate new balls as it iterates over random.randint? Can I use randint to generate variables with a couple of ints at
#the end of each new ball?

    # def bawl_consumption(self):
    #     for bawl in bawls:
    #         if self.radius


#----------------------------Square Class------------------------------


# Import math library for square root function

# class Shape:
#     def area(self):
#         return 0
# #Square Class
# class Square(Shape):
#     #Defines what the side length of the square is based on input provided 
#     def __init__(self,side_length):
#         self.side_length = side_length
    
# #Overwrites initial area method to calculate area based on given argument to Square()
# #perimeter = side length * 4
#     def area(self):
#         return self.side_length * self.side_length


#     def is_perfect_square(self):
#         y = int(math.sqrt(self.area()))
#         return y*y == self.area()

    # self.v_new = self.velocity_x + gravity
        # damping_factor = 0.8
        # if self.velocity_y_new >= height:
        #     self.v_new = -self.velocity_x * damping_factor
        
        #Do I need to reference bawl check here?
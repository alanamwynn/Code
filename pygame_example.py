import pygame
from pygame.time import Clock
import math
from random import randint,random

from vector import Vector

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

# Initialize Pygame
pygame.init()
clock = Clock()

# Create a window of 800x600
height = 600
width = 800
screen = pygame.display.set_mode((width, height))
x = int("F", 16)
circle_size = 2*math.pi

# Window title
pygame.display.set_caption("Mistress Ada's Perfect Circle")


#make a ball Class constructor, attrs
class Ball:
    def __init__(self,position,radius,color):
        self.color = color
        self.position = position
        self.radius = radius
        self.velocity = Vector(random() * circle_size, random() * 4) 
        self.scream1 = pygame.mixer.Sound("alana-aaa.mp3")
    #draws a circle within the confinements of the screen. attrs: color, coordinates, and a radius
    def draw(self):
        pygame.draw.circle(screen, self.color, self.position.get_coords(), self.radius)

    #updates the position based on the old position + velocity
    def update(self):
        self.gravity()
        self.position += self.velocity
        self.bounce_off_wall()

    def bounce_off_wall(self):
        x,y = self.position.get_coords()
        if x + self.radius >= width or x- self.radius <= 0:
            self.velocity = self.velocity.reflect_over_y()
        if y + self.radius >= height or y - self.radius <=0:
            self.velocity = self.velocity.reflect_over_x()

    def gravity(self):
        #gravity is a vector. it points down
        gravity = Vector(math.pi/2,1)
        self.velocity += gravity

    def distance_check(self,other):
        delta_vector = other.position - self.position
        return delta_vector.get_magnitude()
    
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


max_radius = 100
bawls = []

#Create a number of balls within the specified range and apply random attrs using randint
for ball in range(6):
   x = randint(max_radius,width - max_radius)
   y = randint(max_radius,width - max_radius)
   position = Vector.build_from_xy(x, y)
   bawls.append(Ball(position, randint(0,max_radius), (randint(0,255), randint(0,255), randint(0,255))))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Clear the screen with grey
    screen.fill((125, 125, 125))

    #Does this update the ball's position?
    for bawl_i in range(len(bawls)):
        bawl = bawls[bawl_i]
        bawl.update()
        bawl.draw()
        #can I use angle_check below instead?
        for other_bawl_i in range(bawl_i + 1, len(bawls)):
            other_bawl = bawls[other_bawl_i]

            #if the balls collide, they change colors, yell, and bounce
            if bawl.collision_check(other_bawl):
                bawl.color = (randint(0,255), randint(0,255), randint(0,255))
                other_bawl.color = (randint(0,255), randint(0,255), randint(0,255))
                bawl.scream1.play()
                other_bawl.scream1.play()
                bawl.bounce_off(other_bawl)
                other_bawl.bounce_off(bawl)

                overlap = bawl.distance_check(other_bawl) - (bawl.radius + other_bawl.radius)
                if overlap < 0:
                    normal = other_bawl.position - bawl.position
                    normal.magnitude = 1
                    
                    push_distance = overlap * 0.5
                    bawl.position += normal.scale(push_distance)
                    other_bawl.position -= normal.scale(push_distance)

                
                
    # Update the screen
    pygame.display.update()
    clock.tick(30)

# Quit Pygame
pygame.quit()


#More Ideas for this Pygame:

    # bouncing off eachother that mimics irl physics
    # gravity attracting to each other
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
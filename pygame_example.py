import pygame
from pygame.time import Clock
import math
from random import randint

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

# Window title
pygame.display.set_caption("Mistress Ada's Perfect Circle")
#write a funct that takes a 6 chara string as hex code and returns a tuple of the rgb
#can ask how to convert hexadecimal to rgb in py. don't ask CHATGPT to write this function
# Loop until the user closes the window


#make a ball Class constructor, attrs
class Ball:
    def __init__(self,x,y,radius,color):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity_x = randint(-5,5)
        self.velocity_y = randint(-5,5)
    #draws a circle within the confinements of the screen. attrs: color, coordinates, and a radius
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        #update x,y based on velocity
        #make the edge (not the center) of the balls hit the edge of the screen
    #updates the position based on the old position + velocity
    def update(self):
        self.gravity()
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y
        self.bawl_velocity_set()
    #Changes and sets the velocity times equals -1 to convert it to a negative number. Neg in Pygame goes up, not down.
    #when the sum of x and the radius are greater than/equal to the width or when the subtraction
    #of x from the radius is less than or equal to 0
    def bawl_velocity_set(self):
        if self.x + self.radius >= width or self.x - self.radius <= 0:
            self.velocity_x *= -1
            self.x += self.velocity_x
        if self.y + self.radius >= height or self.y - self.radius <=0:
            self.velocity_y *= -1
            self.y += self.velocity_y
#mess with the gravity method. see how it changes the behavior. switch back to next project afterwards
#Modifies gravity based on the velocity of y
    def gravity(self):
        gravity = 1
        self.velocity_y += gravity

        #Make distance method to use with collision check
    #Calculating the magnitude(distance) by squaring the result of the subtracted x vectors and adding the 
    #squared result of the subtracted y vectors, squared by .5
    def distance_check(self,other):
        delta_vector_x = other.x - self.x
        delta_vector_y = other.y - self.y
        distance = (delta_vector_x)**2 + (delta_vector_y)**2
        distance = distance**0.5
        return distance
    #Checks if the distance between the two balls is equal to their combined radiuses to determine collision
    def collision_check(self,other):
        if self.distance_check(other) <= self.radius + other.radius:
            return True
        else:
            return False
    #determines the angle of the balls based on the subtraction of both the position vectors, plugged into atan2
    def angle_check(self,other):
        delta_vector_x = other.x - self.x
        delta_vector_y = other.y - self.y
        angle = math.atan2(delta_vector_y, delta_vector_x)
        return angle
    def angle_of_velocity(self):
        return math.atan2(self.velocity_y, self.velocity_x)
    

max_radius = 100
bawls = []

#Create a number of balls within the specified range and apply random attrs using randint
for ball in range(2):
   bawls.append(Ball(randint(max_radius,width - max_radius), randint(max_radius,height - max_radius), randint(0,max_radius), (randint(0,255), randint(0,255), randint(0,255))))

    #randint might be helpful for generating random attr
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Clear the screen with grey
    screen.fill((125, 125, 125))

    #Does this update the ball's position?
    for bawl in bawls:
        bawl.update()
        bawl.draw()
        #can I use angle_check below instead?
        for other_bawl in bawls:
            if bawl.x == other_bawl.x and bawl.y == other_bawl.y:
                continue
            
            # bawls_in_sim = []
            # collision_update_needed = []
            #Detect collisions and mark balls for update
            # for i,bawls in enumerate(bawls_in_sim):
            #     for other_bawl in bawls_in_sim[i+1:]:
            #         if bawl.collision_check(other_bawl):
            #             collision_update_needed.append(bawl,other_bawl)
            # for bawl,other_bawl in collision_update_needed:
            #     bawl.bawl_velocity_set(other_bawl)
            # collision_update_needed.clear()

            #if the balls collide, change the color of both bawls. 
            if bawl.collision_check(other_bawl):
                bawl.color = (randint(0,255), randint(0,255), randint(0,255))
                #
                angle = bawl.angle_check(other_bawl)
                # angle_of_reflection = angle + math.pi/2 
                angle_of_velocity = bawl.angle_of_velocity()
                angle_of_incidence = angle_of_velocity - angle
                new_velocity_angle = angle - angle_of_incidence 
                new_velocity = make_vector(new_velocity_angle, math.sqrt((bawl.velocity_x ** 2) + (bawl.velocity_y ** 2)))
                bawl.velocity_x, bawl.velocity_y = new_velocity
                overlap = bawl.distance_check(other_bawl) - (bawl.radius + other_bawl.radius)
                if overlap < 0:
                    # Calculate the normal vector components
                    normal_x = bawl.x - other_bawl.x
                    normal_y = bawl.y - other_bawl.y
                    
                    # Normalize the normal vector
                    normal_length = math.sqrt(normal_x**2 + normal_y**2)
                    normal_x /= normal_length
                    normal_y /= normal_length
                    
                    # Push the balls apart by half the overlap distance along the normal vector
                    push_distance = overlap
                    bawl.x -= normal_x * push_distance
                    bawl.y -= normal_y * push_distance
                    other_bawl.x += normal_x * push_distance
                    other_bawl.y += normal_y * push_distance

                
                
                
                

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
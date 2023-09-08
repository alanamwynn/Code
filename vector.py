import math

class Vector:
    def __init__(self,direction,magnitude):
        self.direction = direction
        self.magnitude = magnitude
        #define vector x (ball.x - other_ball.x) and vector_y here?
        #how can I make this method work using x & y?
        #connect vectors to x & y coordinates?
    def get_direction(self):
        return self.direction
    def get_magnitude(self):
        return self.magnitude
    def get_coords(self):
        #scale cosin and sin based on mag
        x = math.cos(self.direction) * self.magnitude
        y = math.sin(self.direction) * self.magnitude
        return (x,y)
    #scale: mag*= k, add: C=A(x + other x) + B (y + other y), rotate: direction += rotation
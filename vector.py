import math

class Vector:
    @staticmethod
    def build_from_xy(x, y):
        vec = Vector(0, 0)
        vec.direction = math.atan2(y, x)
        vec.magnitude = math.sqrt(x ** 2 + y ** 2)
        return vec

    def __init__(self,direction,magnitude):
        self.direction = direction
        self.magnitude = magnitude
    def get_direction(self):
        return self.direction
    def get_magnitude(self):
        return self.magnitude
    def get_coords(self):
        #scale cosin and sin based on mag
        x = math.cos(self.direction) * self.magnitude
        y = math.sin(self.direction) * self.magnitude
        return (x,y)
    #Creates a New Vector
    def __add__(self,other):
        self_x, self_y = self.get_coords()
        if type(other) == Vector: # adding a vector
            other_x, other_y = other.get_coords()
            new_y = self_y + other_y
            new_x = self_x + other_x
        else: # adding a scalar
            new_y = self.y + other
            new_x = self.x + other
        return Vector.build_from_xy(new_x, new_y)
    def __sub__(self, other):
        return self + (other.scale(-1))
    # Scalar below    
    def scale(self,other):
        return Vector(self.direction,self.magnitude * other)
    def rotate(self,other):
        return Vector(self.direction + other,self.magnitude)
    #Reflection Methods - to rotate over x use 2pi - theta. to rotate over y use pi - theta.
    def reflect_over_x(self):
        return Vector(math.pi*2 - self.direction,self.magnitude)
    def reflect_over_y(self):
        return Vector(math.pi - self.direction,self.magnitude)
    #scale: mag*= k, add: C=A(x + other x) + B (y + other y), rotate: direction += rotation
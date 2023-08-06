import math
import random
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
          
    def square(self):
        return self.x * self.x + self.y * self.y
    
    def length(self):
        return math.sqrt(self.square())
    
    def clone(self):
        return Vector(self.x, self.y)
    
    def negative(self):
        self.x = - self.x
        self.y = - self.y
    
    def normalize(self):
        length = self.length()
        if(length > 0):
            self.x = self.x/length
            self.y = self.y/length
        return self.length
 
    def addition(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)
    
    def increment(self, vector):
        self.x = self.x + vector.x
        self.y = self.y + vector.y
        
    def subtract(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y)
    
    def decrement(self, vector):
        self.x = self.x - vector.x
        self.y = self.y - vector.y
    
    def multiply(self, k):
        return Vector(k * self.x, k * self.y)
    
    def scale(self, k):
        self.x = self.x * k
        self.y = self.y * k
        
    def scalerProduct(self, vector):
        return self.x * vector.x + self.y * vector.y

    def addMultbyScaler(self, vector, k):
	    return Vector(self.x + k*vector.x, self.y + k*vector.y)

    def distance(self, vector1, vector2):
        return (vector1.subtract(vector2)).length()

    def angleRad(self, vector1, vector2):
        return math.acos(vector1.dotProduct(vector2) / (vector1.length() * vector2.length()))

def Random(min, max):
    return math.floor(random.random()*(max - min + 1)) + min

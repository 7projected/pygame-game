import math

# mag = sqrt(x^2 + y^2)
def magnitude(vec):
    return math.sqrt((vec[0] * vec[0]) + (vec[1] * vec[1]))

# norm = (x/mag, y/mag)
def normalize(vec):
    mag = magnitude(vec)
    if mag == 0:
        return vec
    return [vec[0] / mag, vec[1] / mag]

def clamp(input, min, max):
    if input > max:
        return max
    
    if input < min:
        return min
    
    return input

import math

M_PI = math.pi

def computeDistanceOnCircle(alpha, beta):
    
    return min((beta - alpha) % (2 * M_PI), (alpha - beta) % (2 * M_PI))

def computeDistanceOnTorus(alpha1, alpha2, beta1, beta2):

    return math.sqrt(computeDistanceOnCircle(alpha1, alpha2) ** 2 \
                     + computeDistanceOnCircle(beta1, beta2) ** 2)

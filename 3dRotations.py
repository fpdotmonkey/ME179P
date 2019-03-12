#
# 3dRotations.py
#
# Fletcher Porter
#

import math

import numpy as np


def skewMatrix(vector):
    """
Computes the skew matrix of vector as defined by (7.2) in Bullo and Smith.  
vector must be a 3x1 matrix to work with this function.

This function works by iterating through the upper triangle of the matrix.  It 
takes advantage of the fact that in the case of 3x3 matrices, the sum of row 
and column indicies is unique, and so they are iterated through and the 
corresponding element of the matrix is found and given its value of vector, 
multiplied by a constant."""
    # @TODO: make this work for nx1 vector
    try:
        assert len(vector) == 3, "I haven't figured out yet how to make this general for vectors of length != 3.  Forgive me."
    except TypeError:
        print("skewMatrix: vector must be iterable")

    length = len(vector)
    numberOfRows = int(1/2 + (8 * length + 1) ** .5 / 2)
    column = numberOfRows - 1
    skewMatrix = np.zeros((numberOfRows, numberOfRows))
    for i in reversed(range(1, 2 * numberOfRows - 2)):
        row = i - column
        skewMatrix[row, column] = \
            (-1) ** (i) * vector[int(-(i - 1) * (length - 1) \
                                     / (2 * length - 4) + length - 1)]

        if (row == 0):
            column = column - 1

    skewMatrix = skewMatrix - skewMatrix.transpose()
        
    return skewMatrix

def inverseSkewMatrix(skewMatrix):
    """
This computes the inverse skew matrix of skewMatrix following the definition in 
(7.2) in Bullo and Smith.  skewMatrix must be a 3x3 matrix.  Other matrix sizes 
presently don't work."""
    # @TODO: make this work for nxn matrices
    
    numberOfRows = len(skewMatrix)
    length = int((numberOfRows ** 2 - numberOfRows) / 2)
    column = numberOfRows - 1
    axis = np.zeros((length, 1))
    for i in reversed(range(1, 2 * numberOfRows - 2)):
        row = i - column
        axis[int(-(i - 1) * (length - 1) / (2 * length - 4) + length - 1)] = \
            (-1) ** i * skewMatrix[row, column]

        if (row == 0):
            column = column - 1

    return axis


def computeRMfromAA(angle, axis):
    """Simply follow Rodrigues's formula as shown in Theorem 7.10 in Bullo
and Smith, and that gets the correct result"""
    rotationMatrix = np.identity(3) \
                     + math.sin(angle) * skewMatrix(axis) \
                     + (1 - math.cos(angle)) * skewMatrix(axis) \
                     @ skewMatrix(axis)
    
    return rotationMatrix


def computeAAfromRM(rotationMatrix):
    """
Computes the axis and angle of rotation from a rotation matrix using the 
inverse Rodrigues formula, as given in Theorem 7.12 in Bullo and Smith.  It 
checks through the cases of the rotation matrix having trace of -1, (-1, 3), 
and 3, with the procedure of calculations given in the theorem.  In the case 
of trace = 3, the rotation is arbitrarily set to (1, 0, 0), in the case of 
trace == -1, the positive axis is selected, and the case where the trace falls 
outside of the tested range, the zero vector is returned."""
    trace = rotationMatrix.trace()

    if (trace == -1.0):
        angle = math.pi
        axis = (0.5 * (rotationMatrix \
                       + np.identity(3)).diagonal().reshape(3, 1)) ** 0.5

    elif (trace < 3):
        angle = math.acos((trace - 1) / 2)
        axis = inverseSkewMatrix(rotationMatrix - rotationMatrix.transpose()) \
               / (2 * math.sin(angle))

    elif (trace == 3.0):
        # Choose Arbitrary axis and angle of 0 since rotation matrix is identity
        angle = 0
        axis = np.array([[1,0,0]]).transpose()
        
    else:
        angle = 0
        axis = np.array([[0,0,0]])
        print("computeAAfromRN: rotationMatrix must be a special orthoganal matrix")
        
        
    return (angle, axis)


if "__main__" == __name__:
    # Should return the skew diagonal matrix as described in (7.2) of Bullo and Smith
    print(skewMatrix([1,2,3]))

    # Should return a vector that is the inverse of a skew diagonal matrix as defined by (7.2) in Bullo and Smith
    print(inverseSkewMatrix(np.array([[0, -3, 2], [3, 0, -1], [-2, 1, 0]])))

    # Should be the same result as Example 7.11 in Bullo and Smith
    print(computeRMfromAA(2 * math.pi / 3, 1/3 ** .5 * np.ones((3, 1))))
    # Should be the identity Matrix
    print(computeRMfromAA(0, np.array([[1], [0], [0]])))
    # Should be the identity Matrix
    print(computeRMfromAA(2 * math.pi, np.array([[0], [1], [0]])))

    # Tests -1 < trace < 3, should recreate the result of Example 7.13 in Bullo and Smith
    print(computeAAfromRM(np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])))
    # Tests trace == -1, should be a pi rotation about an axis that is 45deg on the yz plane
    print(computeAAfromRM(np.array([[-1, 0, 0], [0, 0, 1], [0, 1, 0]])))
    # Tests trace == 3, should be an angle of zero with arbitrary axis
    print(computeAAfromRM(np.identity(3)))

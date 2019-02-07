#
# grid.py
#
# Fletcher Porter 2019
#

import math
import random
from itertools import count, islice

from matplotlib import pyplot

def computeGridSukharev(numberOfSamples):
    """
Calculates the points of a uniform center grid with numberOfSamples samples.  Raises an AssertionError if numberOfSamples is not a perfect square."""
    samplesOnASide = int(numberOfSamples ** 0.5)
    
    assert samplesOnASide ** 2 == numberOfSamples, "computeGridSukharev: numberOfSamples must be a perfect square"

    return [ [(0.5 + i) / samplesOnASide, (0.5 + j) / samplesOnASide] \
             for i in range(numberOfSamples) \
             for j in range(numberOfSamples) ]


def computeGridRandom(numberOfSamples):
    """
Simply computes a list of pairs of random numbers with length numberOfSamples.  Raises an AssertionError if numberOfSamples is negative or not an integer."""

    assert numberOfSamples > -1 and numberOfSamples == int(numberOfSamples), "computeGridRandom: numberOfSamples must be a non-negative integer"
    
    return [ [random.random(), random.random()] \
             for _ in range(numberOfSamples) ]


def isPrime(n):
    """
Checks for pimality by counting from 1 to n**0.5 and checking each number
if it is a divisor of n.  Doesn't raise an OverflowError for n > 2**31 - 1
(maximum of a C long) thanks to itertools count and islice."""

    if (n != int(n)):
        return false
    
    return n > 1 and all(n % i for i in islice(count(2), int(n ** 0.5 - 1)))


def haltonSequence(index, base):
    """
Computes the indexth number in the halton sequence with base base."""
    # TODO: make this a generator
    assert index > -1, "haltonSequence: index must be a non-negative."
    assert isPrime(base), "haltonSequence: base must be prime"
    
    f = 1
    haltonNumber = 0
    temp = index

    while (temp > 0):
        f = f / base
        haltonNumber = haltonNumber + f * (temp % base)
        temp = int(temp / base)

    return haltonNumber
    
    
def computeGridHalton(numberOfSamples, baseX, baseY):
    """
Creates a list of pairs of halton numbers of bases baseX and baseY of length numberOfSamples."""
    return [ [haltonSequence(i, baseX), haltonSequence(i, baseY)] \
                   for i in range(numberOfSamples) ]
    


if "__main__" == __name__:
    numberOfSamples = 100
    
    sukharev = computeGridSukharev(numberOfSamples)
    sukharevX = [ x for [x, y] in sukharev ]
    sukharevY = [ y for [x, y] in sukharev ]

    pyplot.scatter(sukharevX, sukharevY)
    pyplot.xlim([0, 1])
    pyplot.ylim([0, 1])
    pyplot.show()

    
    random = computeGridRandom(numberOfSamples)
    randomX = [ x for [x, y] in random ]
    randomY = [ y for [x, y] in random ]

    pyplot.scatter(randomX, randomY)
    pyplot.xlim([0, 1])
    pyplot.ylim([0, 1])
    pyplot.show()

    
    halton = computeGridHalton(numberOfSamples, 2, 3)
    haltonX = [ x for [x, y] in halton ]
    haltonY = [ y for [x, y] in halton ]

    pyplot.scatter(haltonX, haltonY)
    pyplot.xlim([0, 1])
    pyplot.ylim([0, 1])
    pyplot.show()

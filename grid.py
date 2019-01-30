#
# grid.py
#
# Fletcher Porter 2019
#

import math

def computeGridSukharev(numberOfSamples):
    samplesOnASide = math.floor(math.sqrt(numberOfSamples))
    
    assert samplesOnASide ** 2 == numberOfSamples, "computeGridSukharev: numberOfSamples must be a perfect square"


    for i in range(samplesOnASide):
        for j in range(samplesOnASide):
            

    return True



if "__main__" == __name__:
    print(computeGridSukharev(16))

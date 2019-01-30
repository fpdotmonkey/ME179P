#
# breadthFirstSearch.py
#
# Fletcher Porter 2019
#

import math

def computeBFSTree(adjacencyTable, startNode):
    assert startNode < len(adjacencyTable), "computeBFSTree: startNode must be the index of a node in adjacencyTable"
    
    parents = [ None for _ in range(len(adjacencyTable)) ]
    parents[startNode] = -1  # -1 here will be used to indicate lack of parent

    parentsInOrder = [ startNode ]
    parentIndex = 0
    
    while None in parents:
        try:
            for i in adjacencyTable[parentsInOrder[parentIndex]]:
                if parents[i] is None:
                    parents[i] = parentsInOrder[parentIndex]
                    
                if i not in parentsInOrder:
                    parentsInOrder.append(i)
                        
            parentIndex = parentIndex + 1

        except IndexError:
            print("computeBFSTree: adjacencyTable represents a disconnected graph!  A complete tree could not be made.")
            return []

    return parents


def computeBFSPath(adjacencyTable, startNode, goalNode):
    assert len(adjacencyTable) > 0, "computeBFSPath: adjacencyTable must be a list of lists representing a connected graph."
    assert startNode < len(adjacencyTable), "computeBFSPath: startNode must be the index of a node in adjacencyTable"
    assert goalNode < len(adjacencyTable), "computeBFSPath: endNode must be the index of a node in adjacencyTable"

    parents = computeBFSTree(adjacencyTable, startNode);
    if len(parents) == 0:
        print("computeBFSPath: A tree could not be generated.")
        return []

    path = [ goalNode ]  # this will be reversed at the end

    while path[-1] != startNode:
        path.append(parents[path[-1]])

        if (path[-1] == -1):
            path.pop()
            break
                    

    path.reverse()
    
    return path


if "__main__" == __name__:
    
    print("A simple triangle graph")
    triangle = [ [1, 2], [0, 2], [0, 1] ]  # Complete graph of degree 3
    print(triangle)
    print("Tree:")
    print(computeBFSTree(triangle, 0))
    print("Path:")
    print(computeBFSPath(triangle, 0, 2))
    

    print("\nThe graph given in Figure 2.14 of the text")
    figure214 = [ [1], [0, 2, 3], [1, 4], [1], [2] ]  # Figure 2.14 in the text
    print(figure214)
    print("Tree:")
    print(computeBFSTree(figure214, 4))
    print("Path:")
    print(computeBFSPath(figure214, 4, 0))


    print("\nThe graph given in the problem")
    givenGraph = [ [1, 9],
                   [0, 2, 10],
                   [1, 3],
                   [2, 4],
                   [3, 5, 11],
                   [4, 6, 12],
                   [5, 7, 13],
                   [6, 8],
                   [7, 14],
                   [0, 10, 15],
                   [1, 9, 16],
                   [4, 12],
                   [5, 11, 13],
                   [6, 12, 17],
                   [8, 18],
                   [9, 16, 19],
                   [10, 15, 20],
                   [13, 21],
                   [14, 22],
                   [15, 20, 23],
                   [16, 19, 24],
                   [17, 29],
                   [18, 31],
                   [19, 24],
                   [20, 23, 25],
                   [24, 26],
                   [25, 27],
                   [26, 28],
                   [27, 29],
                   [21, 28, 30],
                   [29, 31],
                   [22, 30] ]
    print(givenGraph)
    print("Tree:")
    print(computeBFSTree(givenGraph, 0))
    print("Path:")
    print(computeBFSPath(givenGraph, 0, 31))

import polygons

def distance(point1, point2):
    """Returns the euclidian distance between two 2D points"""
    return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5

def unitVector(vector):
    magnitude = (vector[0] ** 2 + vector[1] ** 2) ** 0.5
    return [ vector[0] / magnitude, vector[1] / magnitude ]

def step(initialPosition, stepSize, direction):
    normalizedDirection = unitVector(direction)
    newPosition =  [ stepSize * normalizedDirection[0] + initialPosition[0],
                     stepSize * normalizedDirection[1] + initialPosition[1] ]

    return newPosition

def vectorFrom(point1, toPoint2):
    return [ toPoint2[0] - point1[0],
             toPoint2[1] - point1[1] ]
    

def computeBug1(start, goal, obstaclesList, stepSize):
    currentPosition = start
    path = [ start ]

    goalDirection = vectorFrom(start, goal)

    while (distance(currentPosition, goal) > stepSize):
        closestObstacle = None
        closestObstacleDistance = float("infinity")
        for obstacle in obstaclesList:
            obstacleDistance = polygons.computeDistancePointToPolygon(
                obstacle, currentPosition)
            if (obstacleDistance < closestObstacleDistance):
                closestObstacle = obstacle
                closestObstacleDistance = obstacleDistance

        if (closestObstacleDistance < stepSize):
            # check if it's okay to not follow the obstacle
            newPosition = step(currentPosition, stepSize, goalDirection)
            if (polygons.inPolygon([newPosition], closestObstacle)[-1]):
                # walk around the obstacle
                walkAroundDirection = \
                    polygons.computeTangentVectorToPolygon(closestObstacle,
                                                           currentPosition)
                newPosition = \
                    step(currentPosition,
                         stepSize,
                         walkAroundDirection)
            currentPosition = newPosition
            
        else:
            currentPosition = step(currentPosition, stepSize, goalDirection)

        goalDirection = vectorFrom(currentPosition, goal)
        path.append(currentPosition)

    path.append(goal)
    return path



if "__main__" == __name__:
    # compute bug1 for an empty environment
    print(computeBug1([0, 0], [1, 1], [], 0.1))

    # compute bug1 for an environment with a square in the middle
    print(computeBug1([0, 0], [1, 1], [[[0.25, 0.25], [0.25, 0.75], [0.75, 0.75], [0.75, 0.25]]], 0.1))

    # compute bug1 for the given environment
    start = [0, 0]
    goal = [5, 3]
    obstacles = [ [[1, 2], [1, 0], [3, 0]], \
                  [[2, 3], [4, 1], [5, 2]] ]
    print(computeBug1(start, goal, obstacles, 0.1))

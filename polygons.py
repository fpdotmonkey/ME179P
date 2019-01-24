import matplotlib.path as mplPath

import linesAndSegments


def inPolygon(testPoints, polygon):
    """
matplotlib.path.contains_points() isn't consistent about what it
returns if a testpoint is on a vertex, so I have to make it consistent."""
    try:
        onVertex = [ ]
    
        for point in testPoints:
            onVertex.append(False)
            for vertex in polygon:
                if point == vertex:
                    onVertex[-1] = True
                    break
            
            polygonPath = mplPath.Path(polygon)
            polygonContainsPoints = polygonPath.contains_points(testPoints)
            
            return [ a or b for (a, b) in zip(onVertex, polygonContainsPoints) ]
    except:
        
        return False

def findNearestSegmentToPoint(polygon, point):
    """
Finds the vertex of a polygon that is closest to the point as well as
one of that vertices two neighbors that is closest to the point. 
Returns the indices of these vertices in polygon."""
    vertexWithMinimumDistance = -1
    nearestAdjacentVertex = -1
    distancesToVertices = []
    for vertex in polygon:
        distancesToVertices.append(((point[1] - vertex[1]) ** 2 \
                                    + (point[0] - vertex[0])**2) ** 0.5)
    vertexWithMinimumDistance = \
        distancesToVertices.index(min(distancesToVertices))
    nearestAdjacentVertex = \
        distancesToVertices.index(
            min(
                distancesToVertices[(vertexWithMinimumDistance + 1) % 3], 
                distancesToVertices[vertexWithMinimumDistance - 1]))

    return [ vertexWithMinimumDistance, nearestAdjacentVertex ]


        
def computeDistancePointToPolygon(polygon, point):
    """
Finds the nearest point to the polygon by first finding the nearest line
segment on the polygon to the point and then finding the distance from that
segment to the point."""
    if inPolygon([point], polygon)[-1]:
        # first, check if the point is in the polygon and return 0 if it is
        return 0
    else:
        # otherwise, find the nearest vertex to the point and the nearest
        # neighbor of that vertex to the point, and find the distance from
        # the segment defined by these vertices and the point
        [ vertexWithMinimumDistance, nearestAdjacentVertex] = \
            findNearestSegmentToPoint(polygon, point)
                
        return linesAndSegments.computeDistancePointToSegment(
            point,
            polygon[vertexWithMinimumDistance],
            polygon[nearestAdjacentVertex])

    
def computeTangentVectorToPolygon(polygon, point):
    """
Finds the nearest segment to the polygon and the nearest point on that segment to the point.  Calculates the line that connects the point and the nearest on the segment and uses the slope of that line to draw a vector of length 1 perpendicular in the clockwise direction to that line."""
    if inPolygon([point], polygon)[-1]:
        # The notion of tangency defined in the problem breaks down in
        # the case of points inside the polygon, notably for test points
        # on vertices where tangency is ill-defined, and in robotic
        # application, we'll generally be outside of polygons, so the
        # tangency vector here will be defined to be the zero vector.

        return [ 0, 0 ]
    else:
        nearestSegmentToPoint = findNearestSegmentToPoint(polygon, point)
        nearestPoint = linesAndSegments.findNearestPointOnSegmentToPoint(
            point,
            polygon[nearestSegmentToPoint[0]],
            polygon[nearestSegmentToPoint[1]])
        
        [ a, b, c ] = linesAndSegments.\
                      computeLineThroughTwoPoints(nearestPoint, point)

        scalingFactor = (a ** 2 + b ** 2) ** -0.5
        
        pointForTangentLine = [ point[0] - scalingFactor * a,
                                point[1] - scalingFactor * b ]
        
        return [ pointForTangentLine[0] - point[0],
                 pointForTangentLine[1] - point[1] ]


if "__main__" == __name__:
    testPolygonTriangle = [ [ 0, 0 ], [ 1, 0 ], [ 0, 1 ] ]

    print("computeDistancePointToPolygon()")
    print(computeDistancePointToPolygon(testPolygonTriangle, [0, 0]))
    print(computeDistancePointToPolygon(testPolygonTriangle, [0, 0.5]))
    print(computeDistancePointToPolygon(testPolygonTriangle, [0.1, 0.1]))
    print(computeDistancePointToPolygon(testPolygonTriangle, [0, 1.1]))
    print(computeDistancePointToPolygon(testPolygonTriangle, [1.1, 0]))
    print(computeDistancePointToPolygon(testPolygonTriangle, [-0.1, -0.1]))
    print(computeDistancePointToPolygon(testPolygonTriangle, [0.6, 0.6]))

    print("\ncomputeTangentVectorToPolygon()")
    print(computeTangentVectorToPolygon(testPolygonTriangle, [0, 0]))
    print(computeTangentVectorToPolygon(testPolygonTriangle, [0, 0.5]))
    print(computeTangentVectorToPolygon(testPolygonTriangle, [0.1, 0.1]))
    print(computeTangentVectorToPolygon(testPolygonTriangle, [0, 1.1]))
    print(computeTangentVectorToPolygon(testPolygonTriangle, [1.1, 0]))
    print(computeTangentVectorToPolygon(testPolygonTriangle, [-0.1, -0.1]))
    print(computeTangentVectorToPolygon(testPolygonTriangle, [0.61, 0.6]))

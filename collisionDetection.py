#
# collisionDetection.py
#
# Fletcher Porter
#

def isPoint(possiblePoint):
    """
Returns true if possiblePoint is an iterable thing with length 2 whose elements are all real-valued numbers.  Complex numbers and strings will result in a False result."""
    try:
        if (len(possiblePoint) == 2
            and not isinstance(possiblePoint, str)
            and not any(isinstance(i, complex) for i in possiblePoint)):
            [ float(i) for i in possiblePoint ]

            return True
        else:

            return False
    except (ValueError, TypeError):
        return False

def isSegment(possibleSegment):
    """
Returns true if possible segment is an iterable thing with length 2 whos elements are both points as defined by isPoint()."""
    try:
        if (len(possibleSegment) == 2
            and all(isPoint(point) for point in possibleSegment)):

            return True
        else:
        
            return False
    except (ValueError, TypeError):
        
        return False

def isPolygon(possiblePolygon):
    """
Returns True if possiblePolygon is an iterable thing with length greater than zero whose elements are all points as defined by isPoint()."""
    try:
        if (len(possiblePolygon) > 0
            and all(isPoint(point) for point in possiblePolygon)):

            return True
        else:
        
            return False
    except (ValueError, TypeError):
        
        return False


def isInAABB(point, polygon, smallAmount=1e-5):
    """
Checks if point is inside the smallest axis-aligned bounding box (AABB) that contains polygon.  It has an optional parameter smallAmount which is the size of the small buffer between the bounding box and the polygon which is to avoid any false negatives for collision.

It will raise an AssertionError if point is not a point defined by isPoint() or if polygon is not a polygon as defined by isPolygon()."""
    assert isPoint(point), "isInAABB: point is not a numerical list with two elements"
    assert isPolygon(polygon), "isInAABB: polygon is not a list of points"

    maxX = max(i for [i, j] in polygon) + smallAmount
    minX = min(i for [i, j] in polygon) - smallAmount
    maxY = max(j for [i, j] in polygon) + smallAmount
    minY = min(j for [i, j] in polygon) - smallAmount

    if (point[0] > minX and point[0] < maxX
        and point[1] > minY and point[1] < maxY):

        return True
    else:

        return False

def pointOutsideOf(polygon, smallAmount=0.01):
    """
This returns a point that is gurenteed to be outside of polygon, useful for pretending to cast rays out of polygons.  It has an optional parameter smallAmount which is the size of the distance from the closest point that might be on the polygon.

It will raise an AssertionError if polygon is not a polygon as defined by isPolygon()."""
    assert isPolygon(polygon), "pointOutsideOf: polygon is not a list of points"

    maxX = max(i for [i, j] in polygon) + smallAmount
    maxY = max(j for [i, j] in polygon) + smallAmount

    return [ maxX, maxY ]

def isOdd(n):
    """
Returns True if n is odd, False otherwise."""
    if (n % 2 == 1):
        
        return True
    else:
        
        return False
    
def isPointInPolygon(point, polygon):
    """
Checks if point is inside polygon by first checking if point is inside the smallest axis-aligned bounding box around polygon.  If not, it casts a ray from point and counting how many times it intersects the sides of the polygon.  If odd, point is inside the polygon, otherwise it's not.

Raises an AssertionError is point is not a point as defined by isPoint() or if polygon is not a polygon as defined by isPolygon()."""
    assert isPoint(point), "isPointInPolygon: point is not a numerical list with two elements"
    assert isPolygon(polygon), "isPointInPolygon: polygon is not a list of points"

    # if the point isn't in the AABB, then there's no need to do
    # further calculating
    if (not isInAABB(point, polygon)):
        
        return False

    pointOutsideOfPolygon = pointOutsideOf(polygon)
    segmentIntersections = 0
    for i in range(len(polygon)):
        if (doTwoSegmentsIntersect([ point, pointOutsideOfPolygon ], \
                                  [ polygon[i], polygon[i - 1] ])):
            segmentIntersections = segmentIntersections + 1

    if (isOdd(segmentIntersections)):
        
        return True
    else:

        return False


def doTwoSegmentsIntersect(segment1, segment2):
    """
Returns True if segments1 and segment2 intersect at at least one point.  It does this by computing whether the lines that contain each of segment1 and segment2 intersect using (4.2) in Bullo and Smith.  If they do, they are either co-linear or intersect at a point.  For the point case, it needs to be checked if the point on the line where the intersection occured is also on the segment.  For the co-linear case, an AABB is drawn around segment 2, and if a point on segment1 is in that box, then they must intersect.

Raises an AssertionError if segment1 or segment2 are not segments as defined by isSegment()."""
    assert isSegment(segment1), "doTwoSegmentsIntersect: segment1 is not a list of 2 points"
    assert isSegment(segment2), "doTwoSegmentsIntersect: segment2 is not a list of 2 points"
    
    numerator_a = ((segment2[1][0] - segment2[0][0]) * \
                   (segment1[0][1] - segment2[0][1]) - \
                   (segment2[1][1] - segment2[0][1]) * \
                   (segment1[0][0] - segment2[0][0]))
    numerator_b = ((segment1[1][1] - segment1[0][1]) * \
                   (segment1[0][0] - segment2[0][0]) + \
                   (segment1[1][0] - segment1[0][0]) * \
                   (segment1[0][1] - segment2[0][1]))
                   
    denominator = ((segment2[1][1] - segment2[0][1]) * \
                   (segment1[1][0] - segment1[0][0]) - \
                   (segment2[1][0] - segment2[0][0]) * \
                   (segment1[1][1] - segment1[0][1]))

    if (numerator_a != 0 and denominator == 0):

        return False
    elif (numerator_a == 0 and denominator == 0):
        if (isInAABB(segment1[0], segment2)
            or isInAABB(segment1[1], segment2)):
            
            return True
        else:

            return False

    else:
        s_a = numerator_a / denominator
        s_b = numerator_b / denominator

        if (s_a >= 0 and s_a <= 1
            and s_b >= 0 and s_b <= 1):
            
            return True
        else:

            return False
    
    return True 


def doTwoConvexPolygonsIntersect(polygon1, polygon2):
    """
Checks if two polygons intersects by checking if any of the points in either of the polygons are in the other and if any of the segments that make up the polygons intersect.

Raises an AssertionError if polygon1 or polygon2 are not polygons as defined by isPolygon()."""
    assert isPolygon(polygon1), "doTwoConvexPolygonsIntersect: polygon1 is not a list of points"
    assert isPolygon(polygon2), "doTwoConvexPolygonsIntersect: polygon1 is not a list of points"

    for i in range(len(polygon1)):
        if (isPointInPolygon(polygon1[i], polygon2)):
            
            return True

        for j in range(len(polygon2)):
            if (doTwoSegmentsIntersect([polygon1[i], polygon1[i-1]],
                                       [polygon2[j], polygon2[j-1]])
                or isPointInPolygon(polygon2[j], polygon1)):
                
                return True
    
    return False



if "__main__" == __name__:
    print("\nisPoint()")
    intPoint = [1, 2]
    floatPoint = [1.0, 2.0]
    complexPoint = [1.0j, 2.0]
    stringPoint = "ab"
    numberStringPoint = "13"
    tooLongPoint = [1, 2, 3]
    tooShortPoint = [1]

    print(isPoint(intPoint))  # True
    print(isPoint(floatPoint))  # True
    print(isPoint(complexPoint))  # False
    print(isPoint(stringPoint))  # False
    print(isPoint(numberStringPoint))  # False
    print(isPoint(tooLongPoint))  # False
    print(isPoint(tooShortPoint))  # False


    print("\nisSegment()")
    goodSegment = [ intPoint, floatPoint ]
    longSegment = [ intPoint, intPoint, floatPoint ]
    shortSegment = [ intPoint ]

    print(isSegment(goodSegment))  # True
    print(isSegment(longSegment))  # False
    print(isSegment(shortSegment))  # False
    print(isSegment(intPoint))  # False


    print("\nisPolygon()")
    goodPolygon = [ intPoint for _ in range(10) ]
    nothingPolygon = []

    print(isPolygon(goodPolygon))  # True
    print(isPolygon(nothingPolygon))  # False
    
                    
    print("\nisInAABB()")
    unitSquare = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
    outsideUnitSquare = [-2, 2]
    insideUnitSquare = [0, 0]
    onUnitSquareBoundary = [1, 0]

    print(isInAABB(outsideUnitSquare, unitSquare))  # False
    print(isInAABB(insideUnitSquare, unitSquare))  # True
    print(isInAABB(onUnitSquareBoundary, unitSquare))  # True


    print("\ndoTwoSegmentsIntersect()")
    referenceSegment = [[0, 0], [1, 0]]
    parallelAndDistinct = [[0, 1], [1, 1]]
    parallelAndCoincidentToSegment = [[0.5, 0], [1.5, 0]]
    parallelAndCoincidentToLine = [[3, 0], [4, 0]]
    intersectsOnSegment = [[0.5, -0.5], [0.5, 0.5]]
    intersectsOnLine = [[3, -0.5], [3, 0.5]]

    print(doTwoSegmentsIntersect(referenceSegment,
                                 parallelAndDistinct)) # False
    print(doTwoSegmentsIntersect(referenceSegment,
                                 parallelAndCoincidentToSegment))  # True
    print(doTwoSegmentsIntersect(referenceSegment,
                                 parallelAndCoincidentToLine))  # False
    print(doTwoSegmentsIntersect(referenceSegment,
                                 intersectsOnSegment))  # True
    print(doTwoSegmentsIntersect(referenceSegment,
                                 intersectsOnLine))  # False
  

    print("\nisPointInPolygon()")
    triangle = [[0, 0], [1, 0], [0, 1]]
    insideTriangle = [0.25, 0.25]
    onTriangleBoundary = [0.5, 0.5]
    outsideTriangleAndInsideAABB = [0.75, 0.75]
    outsideTriangleAABB = [3, 3]

    print(isPointInPolygon(insideTriangle, triangle))  # True
    print(isPointInPolygon(onTriangleBoundary, triangle))  # True
    print(isPointInPolygon(outsideTriangleAndInsideAABB, triangle))  # False
    print(isPointInPolygon(outsideTriangleAABB, triangle))  # False


    print("\ndoTwoConvexPolygonsIntersect()")
    doesntIntersectUnitSquare = [[-5, -5], [-4, -5], [-4, -4], [-5, -4]]
    intersectsUnitSquare = [[0, 0], [2, 0], [2, 2], [0, 2]]
    subsetOfUnitSquare = [[0.5, 0.5], [-0.5, 0.5], [-0.5, -0.5], [0.5, -0.5]]
    supersetOfUnitSquare = [[2, 2], [-2, 2], [-2, -2], [2, -2]]
    noVerticesIntersect = [[1.1, 0], [0, 1.1], [-1.1, 0], [0, -1.1]]

    print(doTwoConvexPolygonsIntersect(unitSquare,
                                       doesntIntersectUnitSquare)) # False
    print(doTwoConvexPolygonsIntersect(unitSquare,
                                       intersectsUnitSquare))  # True
    print(doTwoConvexPolygonsIntersect(unitSquare,
                                       subsetOfUnitSquare))  # True
    print(doTwoConvexPolygonsIntersect(unitSquare,
                                       supersetOfUnitSquare))  # True
    print(doTwoConvexPolygonsIntersect(unitSquare,
                                       noVerticesIntersect))  # True

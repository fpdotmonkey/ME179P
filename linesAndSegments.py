import math

def computeLineThroughTwoPoints(p1, p2):
    """
This function returns coefficiant (a, b, c) such that a*x + b*y + c = 0 
gives a line that goes through the 2-tuples p1 and p2.  In the case of
p1 == p2, it will return (0, 0, 0).  If the inputs aren't indexable objects
whose first two entries are numbers, then this function will return NaN.

The method used to find these coefficients was to find the point-slope
form of the line, which is taught in introductory algebra classes.  I then
rearranged the formula so all terms are on one side and so there is no
possibility of 0-division."""
    try:
        a = p2[1] - p1[1]
        b = p1[0] - p2[0]
        c = (p1[1] - p2[1]) * p1[0] + (p2[0] - p1[0]) * p1[1]
        return (a, b, c)
    
    except TypeError:
        return float("nan")

def computeDistancePointToLine(q, p1, p2):
    """
This function calculates the normal distance from the point q to the
line that connects the points p1 and p2.  If the inputs aren't
indexable objects whose first two entries are numbers, then this
function will return NaN.

The method used to find this distance was to construct lines parallel
to p1-p2 through q.  Another line was contructed perpendicular to these
lines through the origin.  The points where this line intersected the other lines were found, and then the distance between these points is the answer."""
    (a, b, c) = computeLineThroughTwoPoints(p1, p2)
    try:
        distance = abs(a * q[0] + b * q[1] + c) / math.sqrt(a ** 2 + b ** 2)
        return distance
    
    except ZeroDivisionError:
        if (p1 == p2):
            return math.sqrt((p1[0] - q[0]) ** 2 + (p1[1] - q[1]) ** 2)
        else:
            return float("nan")
    except TypeError:
        return float("nan")


def computeDistancePointToSegment(q, p1, p2):
    """
This function calculates the minimum distance from a point to a line
segment defined by p1-p2.  If the inputs aren't indexable objects whose
first two entries are numbers, then this function will return NaN.

The method used to calculate this was to parameterize the line segment
so one vertex corresponds to t = 0 and the other to t = 1.  A t in the
interval [0, 1] was found so to minimize the distance between q and the
line segment.  This was done by finding the distance from q to any point
on the segment.  This general distance was differentiated and set to 0
to find the minimum t, t_min.  This was then plugged into the distance
formula to get the minimum distance between q and the segment."""
    try:
        t_min = min(max(((q[0] - p1[0]) * (p2[0] - p1[0]) \
                         + (q[1] - p1[1]) * (p2[1] - p1[1])) \
                        / ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2), \
                        0), \
                    1)
        minimumDistance = math.sqrt((p1[0] - q[0] \
                                     + t_min * (p2[0] - p1[0])) ** 2 \
                                    + (p1[1] - q[1] \
                                       + t_min * (p2[1] - p1[1])) ** 2)
        return minimumDistance
    except ZeroDivisionError:
        return math.sqrt((p1[0] - q[0]) ** 2 + (p1[1] - q[1]) ** 2)
    except TypeError:
        return float("nan")



if '__main__' == __name__:
    # unit testing computeLineThroughTwoPoints()
    assert (computeLineThroughTwoPoints((0, 0), (0, 0)) == (0, 0, 0)), "computeLineThroughTwoPoints() Doesn't handle the degenerate case"
    assert (computeLineThroughTwoPoints((0, 0), (1, 0)) == (0, -1, 0)), "computeLineThroughTwoPoints() can't handle a horizontal line at the origin"
    assert (computeLineThroughTwoPoints((0, 0), (0, 1)) == (1, 0, 0)), "computeLineThroughTwoPoints() can't handle a vertical line at the origin"
    assert (computeLineThroughTwoPoints((0, 0), (1, 1)) == (1, -1, 0)), "computeLineThroughTwoPoints() can't handle a sloped line through the origin"
    assert (computeLineThroughTwoPoints((0, 1), (1, 0)) == (-1, -1, 1)), "computeLineThroughTwoPoints() can't handle a negatively sloped line"
    assert (computeLineThroughTwoPoints((2, 1), (1, 4)) == (3, 1, -7)), "computeLineThroughTwoPoints() can't handle a line that's not definted by points on the axes"
    assert (math.isnan(computeLineThroughTwoPoints((1), "foo"))), "computeLineThroughTwoPoints() doesn't correctly handle too-short tuples"
    
    # unit testing for computeDistancePointToLine()
    assert (computeDistancePointToLine((0, 0), (0, 0), (0, 0)) == 0), "computeDistancePointToLine() can't compute the case where all points are (0, 0)"
    assert (computeDistancePointToLine((0, 0), (0, 0), (1, 0)) == 0), "computeDistancePointToLine() can't compute the case where q is on one of the vetices"
    assert (computeDistancePointToLine((0.5, 0), (0, 0), (1, 0)) == 0), "computeDistancePointToLine() can't compute the case where q is on the line"
    assert (abs(computeDistancePointToLine((0, 0), (0, 1), (1, 0)) - math.sqrt(2)/2)) < 1e-10, "computeDistancePointToLine() can't compute the case where q is off the line"

    # unit testing for computeDistancePointToSegment()
    assert (computeDistancePointToSegment((0, 0), (0, 0), (0, 0)) == 0), "computeDistancePointToSegment() can't compute the case where all points are (0, 0)"
    assert (computeDistancePointToSegment((0, 0), (0, 0), (1, 0)) == 0), "computeDistancePointToSegment() can't compute the case where q is on one of the vetices"
    assert (computeDistancePointToSegment((0.5, 0), (0, 0), (1, 0)) == 0), "computeDistancePointToSegment() can't compute the case where q is on the line"
    assert (abs(computeDistancePointToSegment((0, 0), (0, 1), (1, 0)) - math.sqrt(2)/2)) < 1e-20, "computeDistancePointToSegment() can't compute the case where q is off the line"

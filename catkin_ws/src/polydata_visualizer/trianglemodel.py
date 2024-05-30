#!/usr/bin/env python3

import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from ros_igtl_bridge.msg import igtlpolydata
import numpy as np

def euclidean_distance(point1, point2):
    return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)

def create_triangle_list_marker(points):
    marker = Marker()
    marker.header.frame_id = "world"
    marker.header.stamp = rospy.Time.now()
    marker.ns = "triangle_list"
    marker.id = 0
    marker.type = Marker.TRIANGLE_LIST
    marker.action = Marker.ADD
    marker.scale.x = 1.0
    marker.scale.y = 1.0
    marker.scale.z = 1.0
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 0.0

    # Convert Point32 list to numpy array for easier distance calculations
    np_points = np.array([[p.x, p.y, p.z] for p in points])
    
    for i, p in enumerate(points):
        # Calculate distances from point p to all other points
        distances = np.linalg.norm(np_points - np_points[i], axis=1)
        # Get the indices of the two closest points
        closest_indices = np.argsort(distances)[1:9]
        
        # Add the triangle formed by p and its two closest points
        marker.points.append(Point(p.x/300+1, p.y/300, p.z/300-0.2))
        marker.points.append(Point(points[closest_indices[0]].x/300+1, points[closest_indices[0]].y/300, points[closest_indices[0]].z/300-0.2))
        marker.points.append(Point(points[closest_indices[1]].x/300+1, points[closest_indices[1]].y/300, points[closest_indices[1]].z/300-0.2))
        marker.points.append(Point(p.x/300+1, p.y/300, p.z/300-0.2))
        marker.points.append(Point(points[closest_indices[2]].x/300+1, points[closest_indices[2]].y/300, points[closest_indices[2]].z/300-0.2))
        marker.points.append(Point(points[closest_indices[3]].x/300+1, points[closest_indices[3]].y/300, points[closest_indices[3]].z/300-0.2))
        marker.points.append(Point(p.x/300+1, p.y/300, p.z/300-0.2))
        marker.points.append(Point(points[closest_indices[4]].x/300+1, points[closest_indices[4]].y/300, points[closest_indices[4]].z/300-0.2))
        marker.points.append(Point(points[closest_indices[5]].x/300+1, points[closest_indices[5]].y/300, points[closest_indices[5]].z/300-0.2))
        marker.points.append(Point(p.x/300+1, p.y/300, p.z/300-0.2))
        marker.points.append(Point(points[closest_indices[6]].x/300+1, points[closest_indices[4]].y/300, points[closest_indices[4]].z/300-0.2))
        marker.points.append(Point(points[closest_indices[7]].x/300+1, points[closest_indices[5]].y/300, points[closest_indices[5]].z/300-0.2))
    print("triangle_list")
    print(marker.points[0])
    print(marker.points[1])
    print(marker.points[2])

    return marker

def polygons_callback(msg):
    print(msg.points[0])
    print(msg.points[1])
    print(msg.points[2])
    points = msg.points
    
    # Create and publish the marker
    marker = create_triangle_list_marker(points)
    marker_pub.publish(marker)

if __name__ == '__main__':
    rospy.init_node('triangle_list_marker_publisher')
    marker_pub = rospy.Publisher('triangle_list_marker', Marker, queue_size=10)

    rospy.Subscriber('/IGTL_POLYDATA_IN', igtlpolydata, polygons_callback)
    rospy.spin()


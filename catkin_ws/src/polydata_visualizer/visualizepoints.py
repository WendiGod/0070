#!/usr/bin/env python3

import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point32
from geometry_msgs.msg import Point
from ros_igtl_bridge.msg import igtlpolydata 

def polygons_callback(msg):
    print(len(msg.polygons))
    print(len(msg.points))
    #print(msg.points[0])
    #print(msg.points[1])
    #print(msg.points[2])
    #print(msg.points[3])
    #print(msg.points[4])
    #print(msg.points[5])
    marker = Marker()
    marker.header.frame_id = "world"
    marker.header.stamp = rospy.Time.now()
    marker.ns = "brain_model"
    marker.id = 0
    marker.type = Marker.POINTS
    marker.action = Marker.ADD
    marker.scale.x = 0.005
    marker.scale.y = 0.005
    marker.scale.z = 0.005
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 0.0

    # Add each point to the marker's points list
    for point in msg.points:
        p = Point(x=point.x/300+1, y=point.y/300, z=point.z/300-0.2)
        marker.points.append(p)
    
    #num_points = len(msg.points)
    #for i in range(num_points-10000):
        # Create a triangle with vertices i, i+1, i+2
        #p1 = msg.points[i]
        #p2 = msg.points[i+1]
        #p3 = msg.points[i+2]
        #marker.points.append(Point(x=p1.x/10, y=p1.y/10, z=p1.z/10))
        #marker.points.append(Point(x=p2.x/10, y=p2.y/10, z=p2.z/10))
        #marker.points.append(Point(x=p3.x/10, y=p3.y/10, z=p3.z/10))

    

    # Publish the marker
    marker_pub.publish(marker)

if __name__ == '__main__':
    rospy.init_node('polygon_visualizer')
    
    rospy.Subscriber('/IGTL_POLYDATA_IN', igtlpolydata, polygons_callback)
    marker_pub = rospy.Publisher('polygon_marker', Marker, queue_size=10)

    rospy.spin()


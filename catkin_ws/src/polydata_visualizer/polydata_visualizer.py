#!/usr/bin/env python3

import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point32
from geometry_msgs.msg import Point
from ros_igtl_bridge.msg import igtlpolydata 

def polygons_callback(msg):
    print(len(msg.polygons))
    print(len(msg.points))
    #set a publisher to publish MARKER with MARKER.POINTS type
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
        p = Point(x=point.x/400+1, y=point.y/400, z=point.z/400)#The brain model is set within the working range of the robotic arm
        marker.points.append(p)
    

    # Publish the marker
    marker_pub.publish(marker)

if __name__ == '__main__':
    rospy.init_node('polygon_visualizer')
    
    rospy.Subscriber('/IGTL_POLYDATA_IN', igtlpolydata, polygons_callback)
    marker_pub = rospy.Publisher('polygon_marker', Marker, queue_size=10)

    rospy.spin()


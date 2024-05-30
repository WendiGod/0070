#!/usr/bin/env python3

import rospy
from moveit_commander import MoveGroupCommander, RobotCommander, PlanningSceneInterface
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler
from visualization_msgs.msg import Marker
from std_msgs.msg import ColorRGBA
from ros_igtl_bridge.msg import igtlpoint
import math


marker_pub = None
Trajectory = []

def calculate_direction_vector(point1, point2):#Computed direction vector
    direction_vector = [
        point2.x - point1.x,
        point2.y - point1.y,
        point2.z - point1.z
    ]
    magnitude = math.sqrt(direction_vector[0]**2 + direction_vector[1]**2 + direction_vector[2]**2)
    direction_vector = [coord / magnitude for coord in direction_vector]
    return direction_vector
    
def calculate_quaternion(direction_vector):
    # the initial orientation is along the x-axis
    roll = 0
    pitch = math.atan2(direction_vector[2], math.sqrt(direction_vector[0]**2 + direction_vector[1]**2))
    yaw = math.atan2(direction_vector[1], direction_vector[0])
    quaternion = quaternion_from_euler(roll, pitch, yaw)
    return quaternion

def move_to_point(x, y, z, Quater):
    
    robot = RobotCommander()
    scene = PlanningSceneInterface()
    group_name = "panda_arm"
    move_group = MoveGroupCommander(group_name)

    # set target position
    
    pose_goal = move_group.get_current_pose(end_effector_link="panda_hand").pose
    pose_goal.position.x = x
    pose_goal.position.y = y
    pose_goal.position.z = z
    pose_goal.orientation.x = Quater[0]
    pose_goal.orientation.y = Quater[1]
    pose_goal.orientation.z = Quater[2]
    pose_goal.orientation.w = Quater[3]

    # plan trajectory
    move_group.set_pose_target(pose_goal, end_effector_link="panda_hand")

    
    plan = move_group.go(wait=True)

    # clear this target
    move_group.stop()
    move_group.clear_pose_targets()

    if plan:
        rospy.loginfo("sucessfully move to (%f, %f, %f)", x, y, z)
    else:
        rospy.logerr("fail to move (%f, %f, %f)", x, y, z)

def Get_Points(msg):
    # get x y z from /IGTL_POINT_IN and Make sure the path is in the robot's work area and match with brain model
    x = -msg.pointdata.x/400+1
    y = -msg.pointdata.y/400
    z = msg.pointdata.z/400

    rospy.loginfo("receive point (%f, %f, %f)", x, y, z)
    Trajectory.append(Point(x,y,z))

    # creat a trajectory
    if len(Trajectory)==2:
       vector = calculate_direction_vector(Trajectory[0],Trajectory[1])
       Quater = calculate_quaternion(vector)
       print(Quater)#show the target quaternion
       move_to_point(Trajectory[0].x,Trajectory[0].y,Trajectory[0].z,Quater)#control robot move to entry point and start the surgery
       move_to_point(Trajectory[1].x,Trajectory[1].y,Trajectory[1].z,Quater)#control robot move to target point and finish the surgery

    # publish the trajectory line with MARKER
    marker = Marker()
    marker.header.frame_id = "world"
    marker.header.stamp = rospy.Time.now()
    marker.ns = "Trajectory"
    marker.id = 0
    marker.type = Marker.LINE_STRIP
    marker.action = Marker.ADD
    marker.scale.x = 0.01
    marker.scale.y = 0.01
    marker.scale.z = 0.01
    marker.color = ColorRGBA(0.0, 1.0, 0.0, 1.0)  # green



    # Publish MARKER
    if len(Trajectory)==2:
       marker.points.append(Trajectory[0])
       marker.points.append(Trajectory[1])
       #print(Trajectory[1])
       marker_pub.publish(marker)

def main():
    global marker_pub
    rospy.init_node('pose_goal', anonymous=True)

    marker_pub = rospy.Publisher('Trajectory', Marker, queue_size=10)

    rospy.Subscriber('/IGTL_POINT_IN', igtlpoint, Get_Points)

    rospy.spin()

if __name__ == '__main__':
    main()


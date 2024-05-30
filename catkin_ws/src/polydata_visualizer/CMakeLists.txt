cmake_minimum_required(VERSION 2.8.3)
project(polydata_visualizer)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  visualization_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS
  scripts/polydata_visualizer.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


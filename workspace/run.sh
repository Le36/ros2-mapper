#!/bin/bash
trap "exit" INT TERM ERR
trap "kill 0" EXIT

source install/setup.bash

if [[ -z $IP && -z $BOT ]]; then
  # Gazebo
  ros2 launch launch/test_world_2.launch.py use_sim_time:=True >/dev/null 2>&1 &
  ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True >/dev/null 2>&1 &
  sleep 0.5
  ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True >/dev/null 2>&1 &
  ros2 launch launch/gazebo_launch.py use_sim_time:=True >/dev/null 2>&1 &
  ros2 run io_node control use_sim_time:=True
elif [ -z "$BOT" ]; then
  # Remote -> Raspi
  ssh ubuntu@"$IP" 'cd ~/ros2-mapper/workspace && BOT=1 ./run.sh'
  exit 0
else
  # Raspi
  . ~/ros2_ws/install/local_setup.bash
  ros2 launch turtlebot3_bringup robot.launch.py >/dev/null 2>&1 &
  sleep 20
  ros2 launch turtlebot3_navigation2 navigation2.launch.py >/dev/null 2>&1 &
  ros2 launch slam_toolbox online_async_launch.py >/dev/null 2>&1 &
  ros2 launch explore_lite explore.launch.py >/dev/null 2>&1 &
  ros2 launch launch/launch.py &
fi

wait

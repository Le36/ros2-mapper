# Diary, Juho

## Sprint 0 (16.05 - 23.05)
### Monday 16.05
I use Arch Linux (btw) on my laptop so I started trying to install gazebo on it. There is a [gazebo package](https://aur.archlinux.org/packages/gazebo) in the Arch User Repository but installing it wasn't easy. I had to install some of the dependencies separately because their PKGBUILDs had errors and one of them even had a compile error, which I fixed by editing the file just before it was compiled. (Not the correct way to fix things, but it worked)  
After I installed Gazebo, I started trying to install ROS 2. The Galactic version of ROS 2 is also a [package](https://aur.archlinux.org/packages/ros2-galactic) in the Arch User Repository, but it had too many errors and I gave up trying to install it.

### Tuesday 17.05
I tried to install ROS 2 Foxy by compiling from source using [this guide](https://wiki.archlinux.org/title/ROS#Building_from_source), but that also had compile errors. I don't remember If I managed to compile it, but there were many problems and ROS 2 doesn't officially support Arch.  
I found a [good tutorial](https://ubuntu.com/blog/simulate-the-turtlebot3) for installing ROS 2 and gazebo on Ubuntu and tried it out on a Ubuntu virtual machine. The tutorial only had a couple of errors, but fixing them was easy. Now I had Gazebo and ROS 2 running on a Ubuntu virtual machine.

### Wednesday 18.05
I don't want to develop code and run the simulation on a virtual machine so I decided to install Ubuntu on my laptop beside Arch. After installing and configuring Ubuntu to my liking, I installed gazebo and ROS 2 following the tutorial and it worked out nicely.

### Thursday 19.05
I started reading the `Beginner: CLI Tools` part of the [ROS 2 tutorial](https://docs.ros.org/en/foxy/Tutorials.html) to get an understanding of how it works. I learned what types of nodes are possible and how they can communicate, but I'm pretty sure I won't remember the commands because I just copy-pasted them to my console. I liked the visualizations that the tutorials had, and they helped me to understand the subject at hand. I also wondered why `ros2 run turtlesim turtle_teleop_key` uses so much CPU.  
I also had a problem with the `rqt*` programs where the icons were not displayed. This is probably because I'm using [i3 window manager](https://i3wm.org/) instead of Gnome. My `rqt_graph` also looked different than in the tutorial (the topics didn't have rectangles around them). (Future note: after configuring the settings to be the same as in the tutorial, it looked the same)

### Friday 20.05
I started reading the Python part of the `Beginner: Client Libraries` part of the ROS 2 tutorial. The tutorial always said to `fill in the <description>, <maintainer> and <license> tags`, but this was a tutorial and that was not necessary? The tutorial was also basically just copy-pasting code, so I didn't learn too much. At least I can recheck the tutorial when I need to make some code of my own.
After reading the tutorial, I made some testing code of my own and started thinking about possible architectures for our project. Writing the code was a bit confusing, but copy-pasting code from the tutorials and then editing it worked out nicely.  
But now I am confused about the dependencies because one of my nodes was missing `<exec_depend>rclpy</exec_depend>` from the `package.xml` file, but the project still worked.

### Saturday 21.05
When looking up how to find QR codes from images and get their relative position, I found a [GitHub repository](https://github.com/rudzen/qr_radar2) that contained a ROS ~~2~~ node that automatically found QR codes and told the distance and angle relative to them. (Future note: It was a ROS 1 node, and I'm not sure if we can use it in ROS 2)

### Monday 23.05
I started trying to figure out how I would attach add a camera to the TurtleBot3 in Gazebo but didn't get too far.  
I also tried to figure out how to use Nav2 in the simulation but the [Nav2 tutorial](https://navigation.ros.org/tutorials/docs/navigation2_with_slam.html) didn't work.  

## Sprint 1 (24.05 - 30.05)
### Wednesday 25.06
I started trying to figure out how to get a camera working in the simulation. I found [a Gazebo tutorial](https://classic.gazebosim.org/tutorials?tut=ros_gzplugins#Camera), but it didn't help at all. I also found [turtlebot3-camera](https://github.com/shaigivati/turtlebot3-camera) GitHub repository, but that didn't work either. The turtlebot3-camera repository had launch files, but I was initially a bit confused as to how to use them, but after rechecking the ros2 tutorial I managed to launch it, but it failed because it is for ROS 1 I think. I had no idea how to get the camera working in the simulation or how the model files work, but I had to get the camera working by desperately googling stuff.

### Thursday 26.05
After googling some more, I found [this](https://github.com/ros-simulation/gazebo_ros_pkgs/wiki/ROS-2-Migration:-Camera#gazebo_ros_camera) migration tutorial from ROS 1 to ROS 2, and copy-pasted code from there to `turtlebot3_ws/src/turtlebot3/turtlebot3_simulations/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf` and it worked after recompiling the turtlebot3 models. I had to copy code from the Gazebo tutorial and transform it into sdf format somehow by looking at examples from the same file. Somehow I got it working, but I'm not completely sure how I did it and how it works. I also needed to do some tweaking to get the camera position right, but I wasn't sure how to do it properly so I just changed the values and recompiled until the camera was in the correct position.  
After that, I struggled to visualize the data from the camera. The camera published the image data to a topic, but I wasn't sure how to transform the data into an image without writing a node for it. Luckily I found out that rviz2 can visualize the images easily.  

## Sprint 2
I wanted to create launch scripts to make running stuff easier, but I had some trouble with launching launch files from a launch file. More specifically I wanted to launch, for example, turtlebot3_world.py but to do so I had to find the path to that. I first tried looking at the Ros 2 official launch file [tutorial](https://docs.ros.org/en/foxy/Tutorials/Launch/Creating-Launch-Files.html), but it didn't mention launching other launch files. Then I found [this](https://answers.ros.org/question/306935/ros2-include-a-launch-file-from-a-launch-file/) tutorial, and I started making a launch file following that. I didn't notice the `get_package_share_directory`, so I had to find the launch files manually. Also, I couldn't run `turtlebot3_teleop` and I couldn't source setup.bash files. Using launch files didn't feel like a good solution so I just ended up creating bash scripts for launching stuff.

I then started creating the QR code node, but I didn't remember much from the tutorials. Luckily I could just copy-paste the code there and easily modify it to fit my needs. Creating the node went surprisingly smoothly. I had one problem though, I wasn't sure how to convert `sensor_msgs/image` to OpenCV image, but I quickly found [this](https://answers.ros.org/question/304777/new-in-ros-sensor_msgsimage-in-opencv/) tutorial, which was for ROS 1, but I got it working easily.

Now that the QR code node was ready, I wanted to test it, but to do that I needed to get QR codes into Gazebo. I had some trouble with that because it wasn't trivial, but I found [this](https://answers.gazebosim.org/question/4761/how-to-build-a-world-with-real-image-as-ground-plane/) tutorial and then tweaked it to be a cube instead of a plane, but the QR Code texture didn't work. Then I found [this](https://campus-rover.gitbook.io/lab-notebook/faq/how-to-add-texture-to-sdf) really good tutorial and I got the QR code working by copy-pasting stuff from there. Combining the QR code node with the memory node was really easy and creating a launch script was also easy, because I had done launch scripts before.

I started working on the tests, and I couldn't find anything anywhere about how to do tests, even on the ROS 2 [tutorial page](https://docs.ros.org/en/foxy/Tutorials.html), and I just decided to try to do them myself. I figured that it would be best to just do level 2 tests (black box test each node individually). Initially, the test script first ran the nodes in the background and then ran the tests, but that introduced race conditions and other unreliabilities. First, the test class also inherited the node class, but then I couldn't subscribe to anything because a node needs to spin to subscribe to stuff. Then I had to create a different node and spin it in the background and then make that node call a mock when it received data, and I also had to wait some time to check if it really got any data.

Publishing data in the tests was always easy though. At some point, I just rewrote the tests and moved the test files to each node's own directory, and then spun it when I tested it. After the rewrite, the tests were much more reliable and the CI also was able to run them successfully. When testing I had trouble with publishing to the image topic and I got the error: `TypeError: Your input type is not a numpy array`, but after some debugging, I just had forgotten one `()`. I also got the error: `rclpy.init() has not been called` and something among the lines of `rclpy has been initialized in another context`, but I got that working by shutting down rclpy after each test suite. When creating a script for running the tests I wanted to check if the nodes were running to run the tests only after the nodes were running, and I thought that I could use `ros2 topic list` and `ros2 topic info ...`, but `ros2 topic list` only refreshes its list every 15? seconds or something, and there is no way to refresh the topic list. I also wanted to not show info logging when running the tests, but I had to figure out how to change logging severity. There was a function to change it, but I got an error about `LoggingSeverity`, but I didn't know what were the valid values. After a quick Google search, I found [this](https://docs.ros2.org/foxy/api/rclpy/api/logging.html) tutorial about logging and I got it working. I also got an error that said: `_rclpy.RCLError: Failed to shutdown: context is zero-initialized` when I did this: `if not rclpy.ok: rclpy.init()` in the nodes, when I actually just needed to run `rclpy.init()` which is a bit weird, because I would think that if `rclpy.ok` is true, I wouldn't get any errors when shutting down rclpy.

I wanted to get the CI working, but I wasn't sure how to do that at first. I found [ament_lint](https://github.com/ament/ament_lint) and [setup-ros](https://github.com/ros-tooling/setup-ros), which I then used to get the linting working. Later I removed the ament_lint and just replaced it with my own script for running linting. Getting the build working in the CI was relatively easy, but I had some problems with adding the tests. I had to (re-)install ros-foxy-ros-base (I thought that setup-ros would install it?), and I also forgot to source `/opt/ros/foxy/setup.bash`, but after doing those two things, the tests were ~~working~~. The tests didn't initially work because they were written badly with race conditions and such, but after rewriting the tests they ran fine.

I tried to run the stuff on the physical robot but every time I ran it, I got a random error. I tried multiple things, including running some of the things on the remote PC, but I still got some random errors, even though it should work the same way as in the Gazebo simulation.

### Positives
- After rewriting the tests, I'm happy with how they turned out
    - Initially, I thought that we couldn't test the API of the nodes, but we actually can
    - I also managed to get code coverage working
- Writing the nodes is easy
- Everything is easy to run with just one command

### Negatives
- No tutorials about how to test nodes
- Random errors on the TurtleBot3 even though the code works in Gazebo

## Sprint 3
When trying to run nav2 and slam on the physical robot, I got multiple different errors:
```
[controller_server-1] [INFO] [1654783491.286673323] [local_costmap.local_costmap]: Timed out waiting for transform from base_link to odom to become available, tf error: Invalid frame ID "base_link" passed to canTransform argument source_frame - frame does not exist
```
```
[controller_server-1] terminate called after throwing an instance of 'std::bad_alloc'
[controller_server-1]   what():  std::bad_alloc
```
```
[planner_server-5] [INFO] [1654784138.185491793] [global_costmap.global_costmap]: Timed out waiting for transform from base_link to map to become available, tf error: Invalid frame ID "map" passed to canTransform argument target_frame - frame does not exist
[controller_server-4] [WARN] [1654784138.332260559] [nav2_costmap_2d]: Robot is out of bounds of the costmap!
[controller_server-4] [WARN] [1654784138.332493952] [local_costmap.local_costmap]: Sensor origin: (0.10, -403336888441395376578708244190451660626474919528593484057303141346297197999760575394529983230900174848.00, 0.18), out of map bounds. The costmap can't raytrace for it.
```
```
# Before setting the initial pose
[planner_server-5] [INFO] [1654783732.368384161] [global_costmap.global_costmap]: Timed out waiting for transform from base_link to map to become available, tf error: Lookup would require extrapolation into the past.  Requested time 0.200000 but the earliest data is at time 1654783727.100093, when looking up transform from frame [base_link] to frame [map]

# After setting the initial pose
Warning: TF_OLD_DATA ignoring data from the past for frame odom at time 0.200000 according to authority Authority undetectable
Possible reasons are listed at http://wiki.ros.org/tf/Errors%20explained
         at line 332 in /tmp/binarydeb/ros-foxy-tf2-0.13.13/src/buffer_core.cpp
```

Googling those errors did not really help. Sometimes it gave a lot of errors but still worked and sometimes it didn't work at all. It's really annoying that it works differently on the physical robot than in the simulation. After trying for some time, I just gave up. I and Oskari also tried to fix this together later but didn't manage to fix it and because of this problem, we can't get the program working on the physical robot properly...

Next, I did a lot of math to figure out how I would get the QR code positions from the images.
I needed to calibrate the Raspberry Pi camera and I found [this](https://navigation.ros.org/tutorials/docs/camera_calibration.html) good tutorial from nav2, but of course, it didn't work but I managed to calibrate the camera by making my own script and running it on the TurtleBot3.

Then I tried to combine the QR code position with the current position of the robot but I ran into a problem where Nav2 didn't publish the current location often enough. Later I found out that this is because I was visualizing the QR code positions with matplotlib. Because of that problem, I just decided to fetch the current position with `tf_buffer.lookup_transform`. Before I fixed the slowness, I was confused with `use_sim_time`. I don't know how to enable `use_sim_time` for all of the launch things and I wish I could just run `ros 2 param set use_sim_time true` and everything would use simulation time. Also, the lookup transform takes in `rclpy.time.Time()` which is always zero for some reason and I have to compare the time in the return value to `self.get_clock().now()` and this is pretty confusing.

When googling answers for my problems, I often came across a tutorial for ROS 1. Also the error for TF_OLD_DATA links to a [ROS 1 page](https://wiki.ros.org/tf/Errors%20explained). Also in the [TurtleBot3 tutorial](https://emanual.robotis.com/docs/en/platform/turtlebot3/appendix_raspi_cam/), they say to run `sudo raspi-config` even though their **OWN** TurtleBot3 image doesn't have raspi-config.

At multiple points during this project, I thought that I'd rather do some web development because I could at least get some coding done. At least VSCode supports Ros2 well and handles all of the imports well.


### Positives
- VSCode supports Ros2 well

### Negatives
- Everything is slow and painful to do
- Nav2 and slam_toolbox don't work properly (on the robot)
- Stuff works differently in the simulation than on the physical robot
- Using simulation time is confusing
- ROS 2 doesn't support the fish shell (no source file after colcon build)

## Sprint 4
In the ROS2 documentation [Synchronous vs. asynchronous service clients](https://docs.ros.org/en/foxy/How-To-Guides/Sync-Vs-Async.html#synchronous-calls) the link to 'The Simple Service and Client' tutorial actually links to 'Writing a simple publisher and subscriber'

Using services is harder than I think it should be. Why can't I just call a service like a function and instead have to do some asynchronous magic? Also the tutorials [Writing a simple service and client](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html) and [Synchronous vs. asynchronous service clients](https://docs.ros.org/en/foxy/How-To-Guides/Sync-Vs-Async.html) are bad because they don't cover the case where a node would want to call it's own function to get the response from the service and instead call the service in the main function which is useless. The 'Writing a simple service and client' tutorial also links a [GitHub repository](https://github.com/ros2/examples/tree/foxy/rclpy/services) with client examples, but none of them are useful...

### Positives

### Negatives
- Calling services is unnecessarily complicated
- ROS2 tutorials lack tutorials for what I wanted to do
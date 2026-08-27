# 4.1 Three-Point Calibration at Robot

Calibrate the camera to the robot by creating a base frame on the robot side that overlaps with the camera frame. Create the base frame at the robot via three points directly on the measuring or picking plane and mark it, if needed, so that it is visible in the camera image:

1. Reference point
2. Point in x direction based on the reference point
3. Point in y direction based on the reference point

<figure class="align-left">
  <img src="images/no_server/no_server_robot_base_frame.png" alt="without wenglor robot server, robot base frame" class="uniform-width-200"/>
</figure>

!!! note

    Make sure to use the same origin and the same orientation for the robot frame and the camera frame. `Module Image Coordinate System` defines the coordinate system of the camera (see [4.2 Job in uniVision](4_2_0_job_in_univision.md)).

<figure class="align-left">
  <img src="images/no_server/no_server_frame_overview.png" alt="without wenglor robot server, frame overview" class="uniform-width-400"/>
</figure>
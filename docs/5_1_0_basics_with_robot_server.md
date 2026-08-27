# 5.1 Basics with Robot Server

!!! note

    - In case of printing your calibration plate, make sure to print the PDFs at actual size and on a stiff and flat material.
    - Typically, the reprojection error for the ZVZJ calibration plate is five times smaller compared to the printed version.
    - For direct light applications, non-transparent calibration plates made of carbon fiber are available. For backlight applications, transparent calibration plates made of glass are available.
    - The calibration plate must cover at least half of the image to be detected. Covering as much of the image as possible, ideally the entire plate, gives the most accurate results.

Consider the following points when setting the calibration poses:

- Ensure the calibration plate is in the field of view of the camera when setting the poses.
- Make sure that the difference between one pose and the next one is as big as possible for the most accurate results (motions with non-parallel rotation axes are required, so make sure to vary the pose angles as much as possible). The same pose could be used several times if not consecutive (e.g., pose one and three can be similar). If space is limited in the application, small differences between one pose and the next one are also possible but result in less accurate results.
- The calibration plate should cover as much of the camera image as possible for the most accurate results (see note above for the minimum required coverage).

The calibration process differs depending on whether the camera is mounted on the robot (see [5.1.1 Camera on Robot](5_1_1_camera_on_robot.md)) or not on the robot (see [5.1.2 Camera not on Robot](5_1_2_camera_not_on_robot.md)).

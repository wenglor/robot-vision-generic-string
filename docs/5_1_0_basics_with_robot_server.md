# 5.1 Basics with Robot Server

The wenglor robot server supports communication with specific robot manufacturers. For details, check the dropdown list of robot manufacturers on the device website of the Machine Vision Device and the operating instructions of the device. Using `Generic` in the dropdown allows communication with additional robot manufacturers via the generic string-based robot vision API (see chapter [5.6 Generic Robot Vision API](5_6_0_generic_robot_vision_api.md)).

It is possible to mount the camera either on the robot or separately from it. The camera can also be slightly tilted towards the measuring or picking plane.

<figure class="align-left">
<img src="images/picking_plane.png" alt="picking_plane" class="uniform-width-200"/>
</figure>

It is also possible to mount the camera and robot on a mobile platform (e.g., an Automated Guided Vehicle - AGV) in order to correct the positional deviation of the mobile platform in front of the machine or the shelf.

Calibrate the robot and camera via several calibration poses in which the camera views the calibration plate from different positions and angles (hand-eye calibration). Buy one of the different [ZVZJ](https://www.wenglor.com/en/Accessories/Optics-Filters-Deflectors-and-Focusers/Calibration-Plates/c/cxmCID222488) calibration plates (recommended) or print the corresponding PDF yourself onto flat, stiff material. The calibration is done inside the wenglor robot server, including compensation for lens distortion and the calculations in mm (`Module Image Calibration` is not needed within the uniVision job). Use `Device Robot Vision` within the uniVision job to send results (coordinates of found objects) to the robot server.

<figure class="align-left">
<img src="images/table_and_plate.png" alt="table_and_plate" class="uniform-width-200"/>
</figure>

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

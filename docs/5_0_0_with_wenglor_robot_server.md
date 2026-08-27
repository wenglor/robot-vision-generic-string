# 5. With wenglor Robot Server

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

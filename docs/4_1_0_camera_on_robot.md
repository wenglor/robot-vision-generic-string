# 4.1 Camera on Robot

This chapter describes the calibration and detection process for a camera mounted on the robot (eye-in-hand), including the use case of camera and robot mounted on a mobile platform.

## Calibration use case

If the camera is on the robot, teach a minimum of five calibration poses. For more accurate results, teach further calibration poses (e.g., seven to eleven poses).

The first calibration pose is also the detection pose. Make sure to use a suitable pose where the objects are located safely. Make sure to use big variations between the different poses.


<table>
<tr>
<td>
<figure>
<img src="images/on_robot/camera_on_robot.png" alt="calibration_pose_1_eih" class="uniform-width-200"/>
<figcaption>Calibration pose 1</figcaption>
</figure>
</td>
<td>
<figure>
<img src="images/on_robot/target_view_1.png" alt="target_view_1" class="uniform-width-200"/>
</figure>
</td>
</tr>
</table>

<table>
<tr>
<td>
<figure>
<img src="images/on_robot/calibration_pose_2_eih.png" alt="calibration_pose_2_eih" class="uniform-width-200"/>
<figcaption>Calibration pose 2</figcaption>
</figure>
</td>
<td>
<figure>
<img src="images/on_robot/target_view_2.png" alt="target_view_2" class="uniform-width-200"/>
</figure>
</td>
</tr>
</table>

<table>
<tr>
<td>
<figure>
<img src="images/on_robot/calibration_pose_3_eih.png" alt="calibration_pose_3_eih" class="uniform-width-200"/>
<figcaption>Calibration pose 3</figcaption>
</figure>
</td>
<td>
<figure>
<img src="images/on_robot/target_view_3.png" alt="target_view_3" class="uniform-width-200"/>
</figure>
</td>
</tr>
</table>

<table>
<tr>
<td>
<figure>
<img src="images/on_robot/calibration_pose_4_eih.png" alt="calibration_pose_4_eih" class="uniform-width-200"/>
<figcaption>Calibration pose 4</figcaption>
</figure>
</td>
<td>
<figure>
<img src="images/on_robot/target_view_4.png" alt="target_view_4" class="uniform-width-200"/>
</figure>
</td>
</tr>
</table>

<table>
<tr>
<td>
<figure>
<img src="images/on_robot/calibration_pose_5_eih.png" alt="calibration_pose_5_eih" class="uniform-width-200"/>
<figcaption>Calibration pose 5</figcaption>
</figure>
</td>
<td>
<figure>
<img src="images/on_robot/target_view_5.png" alt="target_view_5" class="uniform-width-200"/>
</figure>
</td>
</tr>
</table>

After calibration, an optional verification step can be performed to check its accuracy. Applying it moves the robot TCP to the bottom left corner of the calibration plate (with an adjustable safety height offset). It is necessary that the calibration plate was not moved between the calibration and the verification step. In case of bad results, check the setup and recalibrate.

!!! note

    - For the verification step, the Z-axis must point to the object plane.
    - The reprojection error shows how good the calibration was. Typical values are 0.1 for ZVZJ calibration plates and 0.5 for printed calibration plates.

<figure class="align-left">
<img src="images/on_robot/validation_eih.png" alt="validation_eih" class="uniform-width-200"/>
</figure>

## Detect use case

After successful calibration, pick your objects. For the detection pose, it is mandatory to use the position of the first calibration pose.

<figure class="align-left">
<img src="images/on_robot/detection_pose_eih.png" alt="detection_pose_eih" class="uniform-width-200"/>
</figure>

With the object position sent by the camera, the robot moves to the object pose.

<figure class="align-left">
<img src="images/on_robot/robot_at_object_eih.png" alt="robot_at_object_eih" class="uniform-width-200"/>
</figure>

## Mobile platform use case

A further use case is to correct positional deviations of mobile platforms in front of a machine or shelf.

<figure class="align-left">
<img src="images/on_robot/mobile_platform_camera_on_robot.png" alt="mobile_platform_camera_on_robot" class="uniform-width-600"/>
</figure>

If using camera and robot on a mobile platform, make sure that the calibration plate is mounted fixed at each machine or shelf as a reference position. Run the normal calibration process once at the beginning with several different poses with big variations (especially differences in the pose angles). Afterwards, in the run use case, when the mobile platform is in front of the machine or shelf, the camera captures only one image of the calibration plate and calculates the positional deviation of the mobile platform towards the target position. Use this info to update the reference frame of the machine or shelf if the handling pose is fixed.

In case of varying handling poses at mobile platforms, it is possible to calibrate the camera-to-target relation and afterwards use the detect command. Run the normal calibration process once at the beginning with several different poses with big variations (especially differences in the pose angles). Afterwards, in the run use case, the camera captures only one image of the calibration plate and then captures another image via the detect command for flexible object picking. Make sure that the position of the mobile platform is unchanged between calibrating the camera to the calibration target and detecting the object, and that the same robot pose is used for calibrating the camera to the target and for detecting the objects.

!!! note

    - It is also possible to mount camera and robot in the machine. Then the calibration plate must be at a fixed reference position on the mobile platforms or on the boxes.
    - For unique identification of the machine, the shelf, or the mobile platform, it is possible to label them, e.g., with codes. The camera can read the code and send it to the robot as additional info. The code result must be linked to the additional value in `Device Robot Vision` in the uniVision job.

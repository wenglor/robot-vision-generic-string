"""Example template for controlling a wenglor vision device from a robot program.

This script demonstrates an example structure for using the vision system API in
a robot program. Several placeholders need to be adapted to robot-specific use
cases.
"""

import socket
import time
import sys

# -------------------- User configuration -------------------

# Define parameters related to vision system and calibration
# These parameters should be customized based on the specific use case

# Define the IP address and port of the vision system
W_VISION_DEVICE_IP: str = "192.168.100.1"
W_VISION_DEVICE_PORT: int = 32006

# Choose between "camera_on_robot" or "camera_not_on_robot"
W_USE_CASE: str = "camera_on_robot"

# Choose between "zvzj001", "zvzj002", "zvzj003", "zvzj004"
# Choose "zvzj001" instead of "zvzj005" and "zvzj002" instead of "zvzj006"
W_CALIBRATION_TARGET: str = "zvzj001"

# All uniVision jobs require the "device robot vision"
W_CALIBRATION_JOB: str = "calibration.u3p"
W_DETECT_OBJECTS_JOB: str = "find_objects.u3p"
W_DETECT_TARGET_JOB: str = "find_target.u3p"

W_USER_COMMAND: str = "single_detection"
#W_USER_COMMAND: str = "multi_detection"
#W_USER_COMMAND: str = "update_reference_frame"

# Safety offset in mm to be applied to the calibration target pose during validation,
# to prevent collisions in case of a bad calibration result.
W_SAFETY_OFFSET_MM: float = 10

# Define calibration poses and the detection pose. Set to zero for "unset" checks.
# If your robot supports arrays, you can also use arrays instead of lists for better readability and performance
W_CALIB_POSE_1: list = [0, 0, 0, 0, 0, 0]
W_CALIB_POSE_2: list = [0, 0, 0, 0, 0, 0]
W_CALIB_POSE_3: list = [0, 0, 0, 0, 0, 0]
W_CALIB_POSE_4: list = [0, 0, 0, 0, 0, 0]
W_CALIB_POSE_5: list = [0, 0, 0, 0, 0, 0]

# Placeholder for your detection pose
w_detection_pose: list = [0, 0, 0, 0, 0, 0]

w_calibration_done: bool = False      # Indicates whether calibration is complete

# --------------------- Mobile platform-specific parameters --------------------------------------

# Set to TRUE if you have taught the poses inside the machine. Otherwise, the program stops after updating the
# reference frame (`w_reference_frame`) so you can approach the machine and teach the poses relative to it.
W_MACHINE_POSES_TAUGHT: bool = False

# This is the reference frame for all fixed poses inside the machine
w_reference_frame: list = [0, 0, 0, 0, 0, 0]  

# This is a dummy pose that represents any pose in the machine relative to `w_reference_frame`
W_POSE_IN_MACHINE: list = [0, 0, 0, 0, 0, 0]  

# --------------------- End of user configuration -------------------------------------------------------------------------

# -------------------- Utilities ----------------------------

# Global socket
vision_socket: socket.socket = None

"""Utility functions for user interaction and robot control."""

def ui_message(text: str):
    """Simulate a message in the user interface."""
    print("[UI]:", text)
    
def exit_program(text: str):
    ui_message("Exiting program: " + text)
    sys.exit()
    
def set_reference_frame(pose: list):
    """Simulate updating the robot reference frame based on the detected target pose."""
    w_reference_frame[:] = pose[:]
    print("Updated reference frame to target pose:", pose)

def user_dialog(message: str):
    """Simulate a user confirmation dialog. True = confirm, False = cancel."""
    print("[Prompt]: Enter '1' to confirm, '2' to cancel:", message)
    user_input = input()
    if user_input == '1':
        return True
    elif user_input == '2':
        return False
    else:
        exit_program("Invalid input. Exiting program.")

def wait_seconds(seconds: float):
    time.sleep(seconds)

def pose_to_robot_convention(pose: list):
    """Convert a pose to the native robot convention."""
    return pose

def pose_to_vision_convention(pose: list):
    """Convert a pose to the vision system's expected format.

    Position in meters and orientation as a Rodrigues vector in radians.
    """
    return pose

def get_tcp_pose():
    """Simulate getting the robot's current TCP pose."""
    # Here we just use a fake pose.
    return [0.1, 0.2, 0.3, 3.14, 1.57, 1.57]

def to_string(pose: list):
    """Convert a pose to a string representation to send to the vision device."""
    # Before converting to a string, ensure the pose follows the expected vision system convention.
    pose = pose_to_vision_convention(pose)
    
    pose_data = ','.join(map(str, pose))
    # Add brackets to match the expected format
    pose_string = "[" + pose_data + "]"
    return pose_string

def str_to_int(response: str):
    try:
        val = int(response.strip())
        return val, True
    except:
        return 0, False

def str_to_float(response: str):
    try:
        val = float(response.strip())
        return val, True
    except:
        return 0.0, False
    
def is_pose_set(pose: list):
    """Check whether a pose is set to non-zero values."""
    return pose != [0, 0, 0, 0, 0, 0]

def are_calibration_poses_set():
    """Check whether all calibration poses are set to non-zero values."""
    global W_CALIB_POSE_1, W_CALIB_POSE_2, W_CALIB_POSE_3, W_CALIB_POSE_4, W_CALIB_POSE_5
    if ( is_pose_set(W_CALIB_POSE_1) and
         is_pose_set(W_CALIB_POSE_2) and
         is_pose_set(W_CALIB_POSE_3) and
         is_pose_set(W_CALIB_POSE_4) and
         is_pose_set(W_CALIB_POSE_5)):
        return True
    return False

def to_pose(response: str):
    """Convert the response string from the vision device to a pose."""
    # Parse (x,y,z,rx,ry,rz).
    pose = response.strip("()").split(",")
    if len(pose) != 6:
        exit_program("Invalid pose format received: " + response)
    
    # Convert string values to float
    pose = [float(x.strip()) for x in pose]
    
    # Convert the pose from the vision convention to the robot convention.
    pose = pose_to_robot_convention(pose)
    return pose

def move_j(pose: list):
    """Simulate moving the robot to a position with joint interpolation."""
    print("MoveJ to:", pose)

def move_l(pose: list):
    """Simulate moving the robot to a position with linear interpolation."""
    print("MoveL to:", pose)

# -------------------- TCP Socket Handling --------------------

def connect_socket():
    global vision_socket
    try:
        vision_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        vision_socket.settimeout(2)
        vision_socket.connect((W_VISION_DEVICE_IP, W_VISION_DEVICE_PORT))
    except Exception as e:
        ui_message("Socket error: " + str(e))
        vision_socket = None

def close_socket():
    global vision_socket
    if vision_socket:
        vision_socket.close()
        vision_socket = None

def recover_connection():
    """Attempt to recover the connection to the vision system."""
    global vision_socket
    if vision_socket:
        ui_message("Connection is already open")
        return True
    for _ in range(3):  # Try three times.
        close_socket()
        wait_seconds(0.5)  # Wait before retrying.
        connect_socket()
        if vision_socket:
            return True
    ui_message("Failed to reconnect to vision device")
    return False

def send_command(command: str):
    global vision_socket
    if not vision_socket:
        connect_socket()
        if not vision_socket:
            return False
    try:
        vision_socket.sendall((command + "\n").encode())
        return True
    except:
        recover_connection()
        if vision_socket:
            try:
                vision_socket.sendall((command + "\n").encode())
                return True
            except:
                return False
        return False

def receive_response():
    global vision_socket
    try:
        data = vision_socket.recv(1024)
        return data.decode().strip(), True
    except:
        recover_connection()
        if vision_socket:
            try:
                data = vision_socket.recv(1024)
                return data.decode().strip(), True
            except:
                return "", False
        return "", False

def send_and_receive(command: str):
    """Send a command to the vision system and receive the response, with error handling."""
    if not send_command(command):
        return ""
    response, receive_ok = receive_response()
    print ("Sent command: ", command, "Received response: ", response)
    if not receive_ok:
        return "", False
    check_reply(response)  # Check for errors in the response.
    return response

# -------------------- Error Handling --------------------

def set_error_code(error_code: int):
    """Set the error message based on the error code received from the vision system."""
    code = abs(error_code)

    if code == 5001:
        cam_error_message = "General Error"
    elif code == 5002:
        cam_error_message = "Badly formatted request"
    elif code == 5003:
        cam_error_message = "No connection to uniVision"
    elif code == 5004:
        cam_error_message = "Unknown uniVision job name"
    elif code == 5005:
        cam_error_message = "Badly configured uniVision job"
    elif code == 5006:
        cam_error_message = "Calibration failed"
    elif code == 5007:
        cam_error_message = "No calibration data"
    elif code == 5008:
        cam_error_message = "No object found"
    elif code == 5009:
        cam_error_message = "Bad or empty device message"
    elif code == 5010:
        cam_error_message = "Index error"
    else:
        cam_error_message = "Unknown error"

    # Exit the program after an error to prevent undefined behavior.
    exit_program("Vision system error: " + cam_error_message)

def check_reply(response: str):
    """Check whether the response from the vision system indicates success or an error."""
    if response == "":
        exit_program("No response from vision device, exiting program.")

    # Check whether the response indicates an error (negative error code).
    if response[0] == '-':
        error_code, parsing_ok = str_to_int(response)
        if parsing_ok:
            set_error_code(error_code)
            # `set_error_code` exits the program, so the return value is not relevant.

# -------------------- Vision Functions --------------------

def load_job(job_name: str):
    """Load a uniVision job on the vision system."""
    send_and_receive("job:change[" + job_name + "];")
    
def get_job():
    """Get the currently loaded uniVision job."""
    return send_and_receive("job:get;")

def update_camera_status():
    """Checks the current status of the vision system and updates calibration state."""
    global w_calibration_done
    response = send_and_receive("state[" + W_USE_CASE + "];")

    if response[0] != '0':
        exit_program(f"Camera error. Please check the robot server state at http://{W_VISION_DEVICE_IP}/#/jobs.")

    if response[1] == '0':
        w_calibration_done = False
    else:
        w_calibration_done = True
        
def clear_calibration_buffer():
    """Clear the calibration buffer in the vision system."""
    send_and_receive("calibration:clear;")

def add_calibration_pose(pose: list):
    """Trigger the vision system and add the provided pose as a calibration pose."""
    tcp_pose = to_string(pose)
    send_and_receive("calibration:add[" + tcp_pose + "];")
    
def calculate_calibration():
    """Trigger calibration calculation based on added poses and captured images."""
    cmd = "calibration:calculate[" + W_USE_CASE + "," + W_CALIBRATION_TARGET + "];"
    response = send_and_receive(cmd)

    reprojection_error, ok = str_to_float(response)
    if not ok:
        exit_program("Failed to parse calibration result")
    return reprojection_error

def calibrate_to_ground():
    """Calibrate the camera-to-ground relation for the `camera_not_on_robot` use case only.

    This also creates a new calibration file if the robot-to-camera relation was
    calibrated previously with the `calibration:calculate` command.
    """
    
    if W_USE_CASE != "camera_not_on_robot":
        ui_message("Calibration to ground skipped, only relevant for 'camera_not_on_robot' use case")
        return
    cmd = "calibration:ground[" + W_CALIBRATION_TARGET + "];"
    send_and_receive(cmd)
    
def calibrate_to_target():
    """Calibrate the camera-to-target relation for the selected use case.

    This does not create a new calibration file. The calibration is stored only
    temporarily in the vision device buffer.
    """
    
    cmd = "calibration:target[" + W_USE_CASE + "," + W_CALIBRATION_TARGET + "];"
    send_and_receive(cmd)
    

def run_calibration():
    """Executes a calibration procedure for the vision system."""
    global w_detection_pose

    if not are_calibration_poses_set():
        exit_program("Calibration poses not set. Please set them before calibration.")

    update_camera_status()

    if w_calibration_done:
        confirmed = user_dialog("Calibration already done. Redo?")
        if not confirmed:
            ui_message("Calibration skipped")
            return

    clear_calibration_buffer()
    load_job(W_CALIBRATION_JOB)

    # Prompt the user based on camera placement.
    if W_USE_CASE == "camera_on_robot":
        prompt = "Place calibration target. Ready?"
    elif W_USE_CASE == "camera_not_on_robot":
        prompt = "Mount calibration target and select tool. Ready?"
    else:
        exit_program("Invalid use case")

    confirmed = user_dialog(prompt)
    if not confirmed:
        ui_message("Calibration aborted")
        return

    # Move through the calibration poses.
    move_j(W_CALIB_POSE_1)
    add_calibration_pose(W_CALIB_POSE_1)

    move_j(W_CALIB_POSE_2)
    add_calibration_pose(W_CALIB_POSE_2)

    move_j(W_CALIB_POSE_3)
    add_calibration_pose(W_CALIB_POSE_3)

    move_j(W_CALIB_POSE_4)
    add_calibration_pose(W_CALIB_POSE_4)

    move_j(W_CALIB_POSE_5)
    add_calibration_pose(W_CALIB_POSE_5)
    
    # You can add more calibration poses if needed, but at least five are recommended for good results.

    # Compute calibration results.
    reprojection_error = calculate_calibration()
    ui_message("Calibration completed with a reprojection error of " + str(reprojection_error))

    # The first calibration pose estimates the camera-to-ground relation,
    # so it has to be set as the detection pose.
    if W_USE_CASE == "camera_on_robot":
        w_detection_pose[:] = W_CALIB_POSE_1[:]
    elif W_USE_CASE == "camera_not_on_robot":
        # For ground calibration, the calibration target is placed on the object plane.
        # Therefore, the robot needs to move to the detection pose so it does not cover it.
        if not is_pose_set(w_detection_pose):
            exit_program("Detection pose not set. Please set it before calibration.")
        # Move to the detection pose so the user can place the calibration target on the object plane.
        move_j(w_detection_pose)
        confirmed = user_dialog("Confirm when the calibration target has been placed on the object plane.")
        if confirmed:
            calibrate_to_ground()
        else:
            exit_program("Calibration to ground aborted")

def validate_calibration(offset_mm: float):
    
    update_camera_status()
    
    if not w_calibration_done:
        ui_message("Calibration is not complete and cannot be validated.")
        return
    
    confirmed = user_dialog("Move to detection pose and confirm to validate calibration?")
    
    if not confirmed:
        ui_message("Calibration validation aborted")
        return

    move_j(w_detection_pose)

    pose_str = to_string(get_tcp_pose())
    cmd = "validate[" + W_USE_CASE + "," + pose_str + "];"
    response = send_and_receive(cmd)

    pose = to_pose(response)
    pose[2] = pose[2] + offset_mm  # Assume Z is at index 2.
    move_l(pose)
    user_dialog("Confirm when calibration result was checked.")
    
def detect_target():
    """Get the calibration target pose from the vision system based on the current TCP pose."""
    pose_str = to_string(get_tcp_pose())
    cmd = "target:pose[" + W_USE_CASE + "," + W_CALIBRATION_TARGET + "," + pose_str + "];"
    response = send_and_receive(cmd)
    return to_pose(response)

def detect_objects():
    pose_str = to_string(get_tcp_pose())
    cmd = "detect[" + W_USE_CASE + "," + pose_str + "];"
    response = send_and_receive(cmd)
    return to_pose(response)

def read_num_objects():
    cmd = "num_objects:get;"
    response = send_and_receive(cmd)
    num_objects, parse_ok = str_to_int(response)
    if not parse_ok or num_objects < 0:
        exit_program("Failed to read number of objects")
    return num_objects

def read_pose_by_index(index: int):
    cmd = "pose:get[" + str(index) + "];"
    response = send_and_receive(cmd)
    pose = to_pose(response)
    return pose

def read_shape_by_index(index: int):
    cmd = "shape:get[" + str(index) + "];"
    response = send_and_receive(cmd)
    shape_id, parse_ok = str_to_int(response)
    if not parse_ok or shape_id < 0:
        exit_program("Failed to read shape id")
    return shape_id

def read_value_by_index(index: int):
    cmd = "value:get[" + str(index) + "];"
    response = send_and_receive(cmd)
    # The response is a raw string. Its format depends on the use case.
    return response

def calibrate_if_needed():
    """Run calibration if no calibration has been done yet."""
    global W_SAFETY_OFFSET_MM
    
    update_camera_status()

    if not w_calibration_done:
        ui_message("No calibration found, starting calibration procedure.")
        run_calibration()
        
        # Update camera status again after calibration.
        update_camera_status()  
        if not w_calibration_done:
            exit_program("Calibration failed. Aborting program.")
        else:
            # Validate using the safety offset defined in the configuration section.
            validate_calibration(W_SAFETY_OFFSET_MM)
            confirmed = user_dialog("Calibration successful, proceed with detection?")
            if not confirmed:
                exit_program("User aborted program.")

def prepare_detection():
    """Prepare the robot for detection by updating camera status and loading the job."""
    calibrate_if_needed()

    load_job(W_DETECT_OBJECTS_JOB)
    move_j(w_detection_pose)

def single_detection():
    
    calibrate_if_needed()
    
    load_job(W_DETECT_OBJECTS_JOB)
    move_j(w_detection_pose)
    

    object_pose = detect_objects()
    # Access index 0 since we only expect one object.
    shape = read_shape_by_index(0)
    
    # Link additional value in the uniVision job before using read_value_by_index.
    #user_value = read_value_by_index(0)
    
    # Add conditional checks for `shape` or `user_value` here.
    
    move_l(object_pose)

    close_socket()

def multiple_detection():
    
    calibrate_if_needed()
    
    load_job(W_DETECT_OBJECTS_JOB)
    move_j(w_detection_pose)

    num_objects = read_num_objects()
    if num_objects <= 0:
        ui_message("No objects found.")
        close_socket()
        return

    for i in range(num_objects):
        pose = read_pose_by_index(i)
        shape = read_shape_by_index(i)
        
        # Link additional value in the uniVision job before using read_value_by_index.
        #user_value = read_value_by_index(0)

        # Add conditional checks for `shape` or `user_value` here.

        move_l(pose)

    close_socket()
    
def update_reference_frame():
    calibrate_if_needed()
    
    load_job(W_DETECT_TARGET_JOB)
    
    # Move to the pose where the vision device can see the calibration target.
    move_j(w_detection_pose)
    
    target_pose = detect_target()
    
    set_reference_frame(target_pose)
    
    if not W_MACHINE_POSES_TAUGHT:
        ui_message("Reference frame updated. Please teach poses now relative to w_reference_frame")
        exit_program("Set W_MACHINE_POSES_TAUGHT to True and restart the program after teaching the poses.")
        
    # The machine reference frame is now updated, and so are the poses inside the machine.

    # Optionally add an intermediate support pose.
    
    # Move to poses in the machine that were taught relative to `w_reference_frame`.
    # `W_POSE_IN_MACHINE` is just a dummy pose.
    move_l(W_POSE_IN_MACHINE)
    
def call_user_command():
    if W_USER_COMMAND == "single_detection":
        single_detection()
    elif W_USER_COMMAND == "multi_detection":
        multiple_detection()
    elif W_USER_COMMAND == "update_reference_frame":
        update_reference_frame()
    else:
        exit_program("Invalid user command, exiting program.")

# -------------------- Main --------------------

def main():
    print("=== EXAMPLE PROGRAM ONLY ===")
    call_user_command()

if __name__ == "__main__":
    main()

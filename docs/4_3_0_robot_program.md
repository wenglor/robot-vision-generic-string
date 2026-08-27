# 4.3 Robot Program

The communication from the robot to the camera via socket messaging is based on the TCP/IP protocol.

Create two socket connections from the robot:

- One socket connection to the LIMA Read Write Limited port for trigger commands (based on request/answer).
- One socket connection to Device TCP in order to get the process data (the camera sends results after each trigger without being requested).

!!! note

    For details, check the network interfaces chapter at the operating instructions of the software [wenglor uniVision 3 (DNNF023)](https://www.wenglor.com/en/Machine-Vision/Machine-Vision-Software/Image-Processing-Software-uniVision-3/wenglor-uniVision-3-Software/p/DNNF023).

The pseudo code on the robot side looks as follows:

- Create the LIMA Read Write Limited socket.
- Connect the LIMA Read Write Limited socket to the IP address (by default `192.168.100.1`) and the port (e.g., `33060` for the first processing instance) of the Machine Vision Device.
- Create the Device TCP socket.
- Connect the Device TCP socket to the IP address (by default `192.168.100.1`) and the Device TCP port (e.g., `34000` for the first processing instance) of the Machine Vision Device.
- Send LIMA trigger command `<T/>` through the LIMA Read Write Limited socket.
- Wait for the response from LIMA through the LIMA Read Write Limited socket.
- Read the result from the Device TCP socket.
- Move the robot to the coordinates provided by the Device TCP socket.

!!! note

    - In case of a camera on the robot, make sure that the robot position when triggering the camera is the same position that was used for calibrating the camera via `Module Image Calibration`.
    - The `<T/>` command on the LIMA Read Write Limited socket triggers the job tree of uniVision. If the job contains `Module Device TCP` and the port set in the robot program matches the port set in uniVision, `Module Device TCP` sends the linked data.
    - For details about Device TCP and LIMA commands, check the operating instructions of the software [wenglor uniVision 3 (DNNF023)](https://www.wenglor.com/en/Machine-Vision/Machine-Vision-Software/Image-Processing-Software-uniVision-3/wenglor-uniVision-3-Software/p/DNNF023).

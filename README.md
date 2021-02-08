# PythonDroneCode
Python code to control the Tello Drone

FaceTracking

Using the haarcascade_frontalface_default.xml machine learning object detection algorithm and the following python modules...

•	OpenCV-Python
•	numpy
•	djitellopy
•	time
•	os
•	platform
•	getpass

We are able to control the Tello Drone to follow the closest face detected.


Setup:

Using Python 3.8.6 and Microsoft Visual Studio Code IDE

1)	Create a new directory
    a.	mkdir FaceTracking
    b.	cd FaceTracking

2)	Create and activate the virtual environment

virtual environment

Note: A best practice among Python developers is to avoid installing packages into a global interpreter environment. You instead use a project-specific virtual environment that contains a copy of a global interpreter. Once you activate that environment, any packages you then install are isolated from other environments. Such isolation reduces many complications that can arise from conflicting package versions. To create a virtual environment and install the required packages, enter the following commands as appropriate for your operating system:

a.	Create and activate the virtual environment

For windows:
py -3 -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\scripts\activate

Note: When you create a new virtual environment, you should be prompted by Visual Studio Code (VS Code) to set it as the default for your workspace folder. If selected, the environment will automatically be activated when you open a new terminal.

The following message should be displayed:

We noticed a new virtual environment has been created. Do you want to select it from the workspace folder?

Click on the “Yes” button.

b.	Install other python modules in the virtual environment
     •	OpenCV-Python - python -m pip install opencv-python
        o	Note: This also installs numpy
     •	djitellopy - python -m pip install djitellopy

3)	Deactivate the virtual environment
    a.	deactivate

4)	Turn on the drone
5)	Select “FaceTracking.py”
6)	Run the code (“F5”)

This code will automatically switch your WiFi to the Tello Drone WiFi name identified in line 10 of the code, the percentage of battery will be displayed, the drone will takeoff and move upward 25 centimeters and look for a human face, once the face is detected the drone will attempt to follow the face, when the user chooses to land the drone, they can land the drone by pressing the letter ‘q’ on the keyboard.

# ESP32-hand-tracker
I made a automatic hand tracker using Python and an esp32 and some servos and a laser
# hardware setup
First of all get two servos and a pan-tilt mechanism
Connect the pan Servo in pin no. 33 and tilt servo in pin no. 21 of the ESP 32
# ESP code
After you have connected the hardware properly upload the `main.ino` file to your ESP 32
# Python code
After you have uploaded the code to your esp32
Install the following python packages
```
pip install opencv cvzone mediapipe numpy serial
```
After installing the packages above run the python file
```
python main.py
```

![github](https://github.com/user-attachments/assets/71e2b10b-e167-4e95-9f7c-d82da1e07c44)

#include <ESP32Servo.h>

Servo left_right;
Servo up_down;

const int panPin = 33; 
const int tiltPin = 21;    

void setup() {
  Serial.begin(115200);    
  left_right.attach(panPin);
  up_down.attach(tiltPin);
  

  left_right.write(90);
  up_down.write(90);

  Serial.println("Servo control ready");
}

void loop() {
  if (Serial.available() > 0) {
    int servoNum = Serial.parseInt();   
    int angle = Serial.parseInt();  

    if (Serial.read() == '\r') {        
      angle = constrain(angle, 0, 180); 

      if (servoNum == 1) {           
        left_right.write(angle);
        Serial.println("Pan angle set to: " + String(angle));
      } 
      else if (servoNum == 2) { 
        up_down.write(angle);
        Serial.println("Tilt angle set to: " + String(angle));
      }
    }
    delay(10); 
  }
}

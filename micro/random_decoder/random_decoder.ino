#include <stdarg.h>


int sensorX = A6;
int sensorY = A7;
float valueX;
float valueY;
char buffer[40];

//setup
void setup() {
  Serial.begin(9600);
}

//loop
void loop() {
  valueX = analogRead(sensorX);
  valueY = analogRead(sensorY);
  sprintf(buffer, "sensorX:%s sensorY:%s !", String(valueX).c_str(), String(valueY).c_str());
  Serial.print(buffer);
  delay(100);
}

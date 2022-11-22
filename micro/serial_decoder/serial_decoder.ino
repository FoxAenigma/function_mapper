#include <stdarg.h>


double valueX;
double valueY;
double DIG = 1000;
char buffer[100];

//setup
void setup() {
  Serial.begin(9600);
}

//loop
void loop() {
  valueX = map(analogRead(A0), 0, 1023, 0, 25000)/DIG;
  valueY = map(analogRead(A1), 0, 1023, -5000, 5000)/DIG;
  sprintf(buffer, "sensorX:%s sensorY:%s !", String(valueX).c_str(), String(valueY).c_str());
  Serial.print(buffer);
  delay(100);
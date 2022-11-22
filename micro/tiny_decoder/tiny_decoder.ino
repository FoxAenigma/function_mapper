#include <stdarg.h>
#define SERIAL_PRINTF_MAX_BUFF 256
const int PINX = A6;
const int PINY = A7;

int valueX;
int valueY;

//header
void serialPrintf(const char *fmt, ...);

//functions
void serialPrintf(const char *fmt, ...) {
  char buff[SERIAL_PRINTF_MAX_BUFF];  
  va_list pargs; 
  va_start(pargs, fmt); 
  vsnprintf(buff, SERIAL_PRINTF_MAX_BUFF, fmt, pargs);
  va_end(pargs);  
  Serial.print(buff);
}

//setup
void setup() {
  Serial.begin(9600);
}

//loop
void loop() {
  valueX = map(analogRead(PINX), 0, 1023, 0, 25)/1000;
  valueY = map(analogRead(PINY), 0, 1023, 0, 5)/1000;
  serialPrintf("sensorX:%d sensorY:%d !", valueX, valueY);
  delay(100);
}

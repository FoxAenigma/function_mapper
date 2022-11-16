#include <stdarg.h>
#define SERIAL_PRINTF_MAX_BUFF 256
int sensorX;
int sensorY;

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
  sensorX = random(10);
  sensorY = random(10);
  serialPrintf("sensorX:%d sensorY:%d !", sensorX, sensorY);
  delay(100);
}

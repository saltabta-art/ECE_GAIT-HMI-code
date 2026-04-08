#include <SoftwareSerial.h>

SoftwareSerial nextion(2,3);   // RX, TX

void setup() {

  nextion.begin(9600);
  delay(1000);

  nextion.print("t_status.txt=\"Status: RUNNING\"");
  nextion.write(0xff);
  nextion.write(0xff);
  nextion.write(0xff);

}

void loop() {

}
#include <SoftwareSerial.h>

SoftwareSerial nextion(2,3); // RX, TX

void setup() {
  Serial.begin(9600);
  nextion.begin(9600);
}

void loop() {
  if (nextion.available()) {
    int data = nextion.read();

    if (data == 49) {
      Serial.println("START");
    }

    else if (data == 48) {
      Serial.println("STOP");
    }

    else if (data == 50) {
      Serial.println("STANDBY");
    }

    else if (data == 51) {
      Serial.println("RESET");
    }
  }
}
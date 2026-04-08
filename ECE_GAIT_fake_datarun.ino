#include <SoftwareSerial.h>

SoftwareSerial nextion(2, 3);   // RX, TX

void sendCommand(String cmd) {
  nextion.print(cmd);
  nextion.write(0xFF);
  nextion.write(0xFF);
  nextion.write(0xFF);
}

float calfValues[]  = {0.42, 0.55, 0.61, 0.48};
float quadValues[]  = {0.31, 0.47, 0.52, 0.40};
float thighValues[] = {0.28, 0.44, 0.50, 0.36};

String activities[] = {
  "Turn Left",
  "Turn Right",
  "Step Up/Down",
  "Straight"
};

const int numSamples = 4;
int indexVal = 0;

bool running = false;
bool standbyMode = false;

unsigned long startTime = 0;
unsigned long lastUpdate = 0;
const unsigned long updateInterval = 2000;   // 2 seconds per sample

void resetDisplay() {
  sendCommand("t_status.txt=\"Status: READY\"");
  sendCommand("t_time.txt=\"Time: 00:00\"");
  sendCommand("t_activity.txt=\"Activity: Ready\"");
  sendCommand("t_calf.txt=\"Calf: 0.00\"");
  sendCommand("t_quad.txt=\"Quad: 0.00\"");
  sendCommand("t_thigh.txt=\"Thigh: 0.00\"");
  sendCommand("j0.val=0");
}

void setup() {
  Serial.begin(9600);
  nextion.begin(9600);
  delay(1000);

  resetDisplay();
}

void loop() {
  // Read button commands from Nextion
  if (nextion.available()) {
    int data = nextion.read();

    if (data == 49) {   // START
      running = true;
      standbyMode = false;
      startTime = millis();
      lastUpdate = 0;
      sendCommand("t_status.txt=\"Status: WALKING\"");
    }
    else if (data == 48) {   // STOP
      running = false;
      standbyMode = false;
      sendCommand("t_status.txt=\"Status: STOPPED\"");
    }
    else if (data == 50) {   // STANDBY
      running = false;
      standbyMode = true;
      sendCommand("t_status.txt=\"Status: STANDBY\"");
    }
    else if (data == 51) {   // RESET
      running = false;
      standbyMode = false;
      indexVal = 0;
      resetDisplay();
    }
  }

  // Update timer while running
  if (running) {
    unsigned long elapsed = millis() - startTime;
    unsigned long totalSeconds = elapsed / 1000;
    int minutes = totalSeconds / 60;
    int seconds = totalSeconds % 60;

    String timeText = "Time: ";
    if (minutes < 10) timeText += "0";
    timeText += String(minutes);
    timeText += ":";
    if (seconds < 10) timeText += "0";
    timeText += String(seconds);

    sendCommand("t_time.txt=\"" + timeText + "\"");
  }

  // Update fake data every 2 seconds
  if (running && millis() - lastUpdate >= updateInterval) {
    lastUpdate = millis();

    sendCommand("t_calf.txt=\"Calf: " + String(calfValues[indexVal], 2) + "\"");
    sendCommand("t_quad.txt=\"Quad: " + String(quadValues[indexVal], 2) + "\"");
    sendCommand("t_thigh.txt=\"Thigh: " + String(thighValues[indexVal], 2) + "\"");
    sendCommand("t_activity.txt=\"Activity: " + activities[indexVal] + "\"");

    int progress = ((indexVal + 1) * 100) / numSamples;
    if (progress > 100) progress = 100;
    sendCommand("j0.val=" + String(progress));

    indexVal++;

    if (indexVal >= numSamples) {
      indexVal = 0;
    }
  }
}
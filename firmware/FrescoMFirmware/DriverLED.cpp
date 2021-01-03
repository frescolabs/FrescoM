#include "DriverLED.h"
#include <Arduino.h>

DriverLED::DriverLED(int controllPin) {
  this->controllPin = controllPin;
  this->set(false);
}

DriverLED::set(bool state) {
  if (state) {
    digitalWrite(this->controllPin, LOW);
  }
  else {
    analogWrite(this->controllPin, 255);
  }
}

#include "MOSFETLED.h"
#include <Arduino.h>

MOSFETLED::MOSFETLED(int controllPin) {
  this->controllPin = controllPin;
}

MOSFETLED::set(bool state) {
  if (state) {
    digitalWrite(this->controllPin, HIGH);
  }
  else {
    digitalWrite(this->controllPin, LOW);
  }
}

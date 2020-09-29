#include "EndStopper.h"

EndStopper::EndStopper(int stopPin) {
  this->stopPin = stopPin;
}

bool EndStopper::getState() {
  return digitalRead(stopPin) == LOW;
}

#include "FrescoMotor.h"
#include <Arduino.h>

#define MICROSECONDS_DELAY_BETWEEN_STEPS 100

FrescoMotor::FrescoMotor(int stepPin, int dirPin) {
  this->stepPin = stepPin;
  this->dirPin = dirPin;
  digitalWrite(dirPin, LOW);
  this->setDirection(true);
} 

void FrescoMotor::step() {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(MICROSECONDS_DELAY_BETWEEN_STEPS);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(MICROSECONDS_DELAY_BETWEEN_STEPS);
}

void FrescoMotor::setDirection(bool direction) {
  this->direction = direction;
  if (this->direction) {
    digitalWrite(dirPin, LOW);
  }
  else {
    digitalWrite(dirPin, HIGH);
  }
}

bool FrescoMotor::getDirection() {
  return direction;
}

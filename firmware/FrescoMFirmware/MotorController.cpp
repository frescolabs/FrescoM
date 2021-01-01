#include "MotorController.h"

#define REBOUND -1000
#define CURRENT_POSITION_KEY 1

MotorController::MotorController(FrescoMotor* motor, 
                                 EndStopper* stopper,
                                 bool goToZeroDirection) {
  this->motor = motor;
  this->stopper = stopper;
  this->axisLength = -1;
  this->currentPosition = -1;
  this->goToZeroDirection = goToZeroDirection;
  
  if (goToZeroDirection) {
    this->rebound = REBOUND;
  }
  else {
    this->rebound = REBOUND * -1;
  }
  
}

void MotorController::goToPosition(long position) {
  if (currentPosition == -1) {
    // Error case, Zero was not defined
  }
  else {
    this->goDelta(position - this->currentPosition);
  }
}

void MotorController::goDelta(long stepsNumber) {
  Serial.print("Go delta in controller \n");
  if (stepsNumber > 0) {
    this->motor->setDirection(true);
  } else {
    this->motor->setDirection(false);
  }
  long stepsCounter = 0;
  while (stepsCounter < abs(stepsNumber)) {
     motor->step();
     stepsCounter++;
     if (stepsNumber > 0) {
       this->currentPosition++;
     }
     else {
       this->currentPosition--;
     }
  }
}

void MotorController::goToZero() {
  this->motor->setDirection(this->goToZeroDirection);
  while (!stopper->getState()) {
    motor->step();
  }
  goDelta(this->rebound);
  this->setCurrentPositionAsGlobalZero();
}

void MotorController::rememberStartPosition() {
  this->motor->setDirection(true);
  long stepsCounter = 0;
  while (!stopper->getState()) {
    motor->step();
    stepsCounter++;
  }
  goDelta(this->rebound);
  axisStart = stepsCounter;
  this->setCurrentPositionAsGlobalZero();
}

void MotorController::rememberEndPosition() {
  this->motor->setDirection(true);
  long stepsCounter = 0;
  while (!stopper->getState()) {
    motor->step();
    stepsCounter++;
  }
  goDelta(this->rebound);
  axisEnd = stepsCounter;
  this->setCurrentPositionAsGlobalZero();
}

long MotorController::getAxisStart() {
  return this->axisStart;
}

long MotorController::getAxisEnd() {
  return this->axisEnd;
}

long MotorController::setCurrentPositionAsGlobalZero() {
  this->currentPosition = 0;
}

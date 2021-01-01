#include "Manifold.h"

Manifold::Manifold(MotorController* zMotorController, 
                   int numberOfPumps,
                   MotorController **pumps) {
  this->zMotorController = zMotorController;
  this->numberOfPumps = numberOfPumps;
  for (int i = 0; i < numberOfPumps; i++) {
    this->pumps[i] = pumps[i];
  }
}

Manifold::deltaPump(int pumpNumber, int delta) {
  Serial.print("Manifold to pump \n");
  pumps[pumpNumber]->goDelta(delta);
}


Manifold::goDeltaZ(int delta) {
  this->zMotorController->goDelta(delta);
}

Manifold::goToZeroVerticalZ() {
  this->zMotorController->goToZero();
}

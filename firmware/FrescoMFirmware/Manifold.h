#ifndef Manifold_h
#define Manifold_h

#include "MotorController.h"
#include "FrescoMotor.h"

#define MAX_NUMBER_OF_PUMPS 10

class Manifold {

  private:
  
    MotorController* zMotorController;
    MotorController* pumps[MAX_NUMBER_OF_PUMPS];
    int numberOfPumps = 0;

  public:

    Manifold(MotorController* zMotorController, 
             int numberOfPumps,
             MotorController **pumps);

    deltaPump(int pumpNumber, int delta);
    goToZeroVerticalZ();
    goDeltaZ(int delta);
    
};

#endif

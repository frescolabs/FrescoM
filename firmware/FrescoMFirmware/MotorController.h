#ifndef MotorController_h
#define MotorController_h

#include "FrescoMotor.h"
#include "EndStopper.h"

class MotorController {
  
  private:

    FrescoMotor* motor;
    EndStopper* stopper;
    long position;
    long axisStart;
    long axisEnd;
    long axisLength;
    long currentPosition;
    bool goToZeroDirection;
    long rebound;
  
  public:
  
    MotorController(FrescoMotor* motor, 
                    EndStopper* stopper,
                    bool goToZeroDirection);
    
    void goToPosition(long position);
    void goDelta(long stepsNumber);
    void goToZero();
    void rememberStartPosition();
    void rememberEndPosition();
    long getAxisStart();
    long getAxisEnd();
    long setCurrentPositionAsGlobalZero();
    
};

#endif

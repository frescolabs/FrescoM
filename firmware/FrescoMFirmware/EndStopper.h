#ifndef Stopper_h
#define Stopper_h

#include <Arduino.h>

// Stopper
class EndStopper {

  private:
  
    byte stopPin;
  
  public:
  
    EndStopper(int stopPin);
    bool getState();

};

#endif

#ifndef FrescoMotor_h
#define FrescoMotor_h



class FrescoMotor {

  private:
  
    int dirPin;
    int stepPin;
    int currentStep;
    long stepsToRun;
    bool direction;

  public:
  
    FrescoMotor(int stepPin, int dirPin);
    void step();
    void setDirection(bool direction);
    bool getDirection();

};

#endif

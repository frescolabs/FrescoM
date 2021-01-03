#ifndef DriverLED_h
#define DriverLED_h


class DriverLED {

  private:
  
    int controllPin;

  public:

    DriverLED(int controllPin);
    set(bool state);
    
};


#endif

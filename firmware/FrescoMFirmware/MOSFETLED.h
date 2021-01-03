#ifndef MOSFETLED_h
#define MOSFETLED_h

class MOSFETLED {

  private:
  
    int controllPin;

  public:

    MOSFETLED(int controllPin);
    set(bool state);
    
};

#endif

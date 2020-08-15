
//Direction pin to beremoved when new pcb arrives
#define X_DIR     5 
#define Y_DIR     6
#define Z_DIR     7

//Step pin
#define X_STP     2
#define Y_STP     3 
#define Z_STP     4 

#define EN 13

//CNC1 
#define XS1 5
#define YS1 6
#define ZS1 7
#define XD1 8
#define YD1 9
#define ZD1 10
#define AS1 11
#define AD1 12

///////////////////////// CNC 2  
#define XS2 27
#define YS2 29
#define ZS2 31
#define AS2 23
#define XD2 33
#define YD2 35
#define ZD2 37 
#define AD2 25

/////////////////////// CNC3
#define XS3 43
#define YS3 45
#define ZS3 47
#define AS3 37
#define XD3 49
#define YD3 51
#define ZD3 53
#define AD3 41

////////////////////// Send stops
#define ES1 22//  return this back fr the new pcb
#define ES2 24// return this back fr the new pcb
#define ES3 26
#define ES4 28
#define ES5 30
#define ES6 32
#define ES7 34
#define ES8 36
#define ES9 38
#define ES10 40
#define ES11 42
#define ES12 44

//////////////////////////
#define NUM_MOTORS 3
#define STEPS_AFTER_ZERO 500 // needs to be calculated
#define MOTOR_DELAY 100
#define FULL_X_LENGTH 33373
#define FULL_X_LENGTHMM 167
#define FULL_Y_LENGTH 20146


#define WELLA0X 8644 // 9144-STEPS_AFTER-ZERO = 9134-500 
#define WELLA0Y 3136 // 3636-STEPS_AFTER-ZERO = 3183-500

#define LASTWELLX 28584//29084-500
#define LASTWELLY 15682//16182-500 
#define INTER_WELL_DISTANCE 1812//  ((LASTWELLX-WELL0X)/11 + same for Y) /2  

/*
 *  Commands:
 *  
 *  Z -> Go to Zero
 *  VerticalZ -> Go to Zero for Z
 *  N -> Vertiacl Z go down by 1 step
 *  M -> Move XY Delta
 *  P X=100 Y=1000 Z=100 -> Set Position
 *  D X=0 Y=0 Z=10 -> Move to Delta
 *  TL -> Remember top left
 *  BR -> Remember bottom right
 *  
 */

enum CommandType {
  GoToZero,
  GoToZeroVerticalZ,
  GoDownBy1StepVerticalZ,
  MoveDeltaXY,
  SetPosition,
  MoveDelta,
  SetTopLeft,
  SetBottomRight,
  Unknown
};

struct Command {
  
  CommandType type;
  String command;
  
};

// Stopper
class EndStopper {

  private:
  
    byte stopPin;
  
  public:
  
    EndStopper(int stopPin) {
      this->stopPin = stopPin;
    }
  
    bool getState() {
      return digitalRead(stopPin) == LOW;
    }

};

class FrescoMotor {

  private:
  
    int dirPin;
    int stepPin;
    int currentStep;
    long stepsToRun;
    bool direction;

  public:
  
    FrescoMotor(int stepPin, int dirPin) {
      this->stepPin = stepPin;
      this->dirPin = dirPin;
      digitalWrite(dirPin, LOW);
      this->direction = true;
    } 

    void step() {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(100);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(100);
    }

    void setDirection(bool direction) {
      this->direction = direction;
      if (this->direction) {
        digitalWrite(dirPin, LOW);
      }
      else {
        digitalWrite(dirPin, HIGH);
      }
    }

    bool getDirection() {
      return direction;
    }

};

// Motor + Corresponding stpper
class MotorController {
  
  private:
  
    long position;
    FrescoMotor* motor;
    EndStopper* stopper;
    
    long axisStart = -1;
    long axisEnd = -1;
    long axisLength = -1;
  
  public:
  
    MotorController(FrescoMotor* motor, 
                    EndStopper* stopper) {
      this->motor = motor;
      this->stopper = stopper;
    }
    
    void goToPosition(long position) {
    }
    
    void goDelta(long stepsNumber) {
      if (stepsNumber > 0) {
        this->motor->setDirection(true);
      } else {
        this->motor->setDirection(false);
      }
      long stepsCounter = 0;
       while (stepsCounter < abs(stepsNumber)) {
        motor->step();
        stepsCounter++;
      }
    }
    
    void goToZero() {

      while (!stopper->getState()) {
        motor->step();
      }

      goDelta(-1000);
    }

    void rememberStartPosition() {
      long stepsCounter = 0;
      while (!stopper->getState()) {
        motor->step();
        stepsCounter++;
      }
      axisStart = stepsCounter;
    }

    void rememberEndPosition() {
      long stepsCounter = 0;
      while (!stopper->getState()) {
        motor->step();
        stepsCounter++;
      }
      axisEnd = stepsCounter;
    }

};


// Contains all motor controllers
class FrescoXYZ {

  // TODO: use std::sharedptr
  private:
  
    MotorController* xMotorController;
    MotorController* yMotorController;
    MotorController* zMotorController;
    
    long xLeftPostition = -1;
    long xRightPosition = -1;
    long yTopPosition = -1;
    long yBottomPosition = -1;
    long xLength = -1;
    long yLength = -1;
    
  public:
  
    FrescoXYZ(MotorController* xMotorController, 
              MotorController* yMotorController, 
              MotorController* zMotorController) {
    this->xMotorController = xMotorController;
    this->yMotorController = yMotorController;
    this->zMotorController = zMotorController;
    this->xLength = 0;
    this->yLength = 0;
    
  }

  void setPosition(long x, 
                   long y, 
                   long z) {
    
  }
  
  void moveDelta(long x, 
                 long y, 
                 long z) {
    
  }

  void goToZero() {
    xMotorController->goToZero();
    yMotorController->goToZero();
    zMotorController->goToZero();
  }

  long getXLength() {
    
  }

  long getYLength() {
    
  }
  
  void perform(CommandType commandType) {
    switch (commandType) {
      case GoToZero:
        this->goToZero();
        break;
      case GoToZeroVerticalZ:
        this->zMotorController->goToZero();
        this->zMotorController->goDelta(-10000);
        break;
      case MoveDeltaXY:
        this->yMotorController->goDelta(5);
        this->xMotorController->goDelta(5);
      case SetPosition:
        break;
      case MoveDelta:
        this->zMotorController->goDelta(-10);
        break;
      case GoDownBy1StepVerticalZ:
        this->zMotorController->goDelta(10);
        break;
      case SetBottomRight:
        break;
      case SetTopLeft:
        break;
    }
  }
  
};


class Parser {

 public:
 
    CommandType parse(String line) {
      char firstLetter = line[0];
      if (firstLetter == 'Z') {
        return GoToZero;
      } 
      else if (firstLetter == 'V') {
        return GoToZeroVerticalZ;
      }
      else if (firstLetter == 'N') {
        return GoDownBy1StepVerticalZ;
      }
      else if (firstLetter == 'M') {
        return MoveDeltaXY;
      }
      else if (firstLetter == 'P') {
        return SetPosition;
      }
      else if (firstLetter == 'D') {
        return MoveDelta;
      }
      else if (firstLetter == 'T') {
        return SetTopLeft;
      }
      else if (firstLetter == 'B') {
        return SetBottomRight;
      }
      else {
        return Unknown;
      }
    }
  
};

int stepPins[] = {XS1,YS1,ZS1,AS1, XS2, YS2, ZS2, AS2, XS3, YS3, ZS3, AS3};
int dirPins[] = {XD1, YD1, ZD1, AD1, XD2, YD2, ZD2, AD2, XD3, YD3, ZD3, AD3};
int ESPins[] = {ES1, ES2, ES3, ES4, ES5, ES6, ES7, ES8, ES9, ES10, ES11, ES12};

void setupPinsModeEndSetEnabled() {
  
  for (int i = 0; i < NUM_MOTORS; i++){
    pinMode(stepPins[i], OUTPUT);
    pinMode(dirPins[i], OUTPUT);
    pinMode(ESPins[i], INPUT);
  }
  
  pinMode(X_DIR, OUTPUT); pinMode(X_STP, OUTPUT);
  pinMode(Y_DIR, OUTPUT); pinMode(Y_STP, OUTPUT);

  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);
}

FrescoXYZ* frescoXYZ;
Parser* frescoParser;

void setup() {
  Serial.begin (250000); 
  Serial.setTimeout(25);

  setupPinsModeEndSetEnabled();
  
  FrescoMotor* xMotor = new FrescoMotor(XS1, XD1);
  FrescoMotor* yMotor = new FrescoMotor(YS1, YD1);
  FrescoMotor* zMotor = new FrescoMotor(ZS1, ZD1);

  EndStopper* xStopper = new EndStopper(ES1);
  EndStopper* yStopper = new EndStopper(ES2);
  EndStopper* zStopper = new EndStopper(ES3);

  MotorController* xMotorController = new MotorController(xMotor, xStopper);
  MotorController* yMotorController = new MotorController(yMotor, yStopper);
  MotorController* zMotorController = new MotorController(zMotor, zStopper);

  frescoXYZ = new FrescoXYZ(xMotorController, yMotorController, zMotorController);

  frescoParser = new Parser();
}

void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readString();
    CommandType commandType = frescoParser->parse(line);
    frescoXYZ->perform(commandType);
  }
}

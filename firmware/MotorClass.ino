
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
/////////////////////////

int stepPins[] = {XS1,YS1,ZS1,AS1, XS2, YS2, ZS2, AS2, XS3, YS3, ZS3, AS3};
int dirPins[] = {XD1, YD1, ZD1, AD1, XD2, YD2, ZD2, AD2, XD3, YD3, ZD3, AD3};
int ESPins[] = {ES1, ES2, ES3, ES4, ES5, ES6, ES7, ES8, ES9, ES10, ES11, ES12};

bool mPressed = false;



class frescoMotor{

   private:
    int pinDir;
    int pinStep;
    long pos;
    int movePeriod; // move once every movePeriod mils
    bool isMoving;
    int currentStep;
    long stepsToRun;
    int stepDelay;
    byte stopPin;
    long test;
    int movingIncrementDecrement;
  public:
    frescoMotor(){}
    frescoMotor(int stepp, int dir)
    {
      this->pinDir = dir;
      this->pinStep = stepp;
      this->pos = 0;
      this->stepsToRun = 0;
      this->stepDelay = MOTOR_DELAY; 
      this-> stopPin = 0; 
    }
    setParams(byte stepp, byte dir){
      pinDir = dir;
      pinStep = stepp;
      pos = 0;
      stepsToRun = 0;
      stepDelay = MOTOR_DELAY; 
      stopPin = 0;
      test = 0; 
    }
    
    void setStopper (byte stpr){
      stopPin = stpr;
      pinMode(stopPin, INPUT);
    }

    
    void setMotorDelay(int del){
      stepDelay= del;
      
    }
    
    void setRunning (int directionM, int speedM, long steps){
      digitalWrite (pinDir, directionM);
      if (directionM == LOW)
        movingIncrementDecrement = -1;
      else
        movingIncrementDecrement = 1;
      isMoving = true;
      movePeriod = 1/speedM;
      stepsToRun = steps;
    }
    bool isRunning(){
      return isMoving;
    }
    void stopRunning(){
      isMoving = false;
      currentStep = 0;
      stepsToRun = 0;
    }

    void oneStep() {
      digitalWrite (pinStep, HIGH);
      delayMicroseconds (stepDelay);
      digitalWrite (pinStep, LOW);
      delayMicroseconds (stepDelay);
      
    }
    
    void run(){
          

      if (!isMoving) return;

      if (stepsToRun<=0) {
        stopRunning();
        Serial.println(-1); ////////////is thgis the best to put signal of stop? or is there a way not to loose the commands?
        return;
      }
      pos+=movingIncrementDecrement;
      currentStep++;
      stepsToRun--;
      
      oneStep();
    }
    int getPosition(){
      return pos;    
    }
    void runToZero(){
      test = 0;
      digitalWrite (pinDir, HIGH);
      while (digitalRead(stopPin)==1){
        test++;
        oneStep();
      }
      digitalWrite (pinDir, LOW);
      for (int i = 0; i < STEPS_AFTER_ZERO; i++){
        oneStep();
        
      }
      stopRunning();
      currentStep = 0;
      pos = 0;

    }
    
};



frescoMotor motors[NUM_MOTORS];

//this one doesn't work:
/*frescoMotor motors2[] = {(XS1, XD1), (YS1, YD1), (ZS1, ZD1)}, (AS1, AD1), 
                         (XS2, XD2), (YS2, YD2), (ZS2, ZD2), (AS2, AD2),
                         (XS3, XD3), (YS3, YD3), (ZS3, ZD3), (AS3, AD3)};*/



frescoMotor xM(XS1, XD1);
frescoMotor yM(Y_STP, Y_DIR);




bool runMotors(){

  bool isRunning = false;
  for (int i = 0; i < NUM_MOTORS; i++){
    if (motors[i].isRunning()){

      isRunning = true;
      motors[i].run();
    }
  }
  return isRunning;
}

void setup() {
  Serial.begin (250000);
  Serial.setTimeout (25);
  for (int i = 0; i < NUM_MOTORS; i++){
    pinMode (stepPins[i], OUTPUT);
    pinMode (dirPins[i], OUTPUT);
    pinMode (ESPins[i], INPUT);
    motors[i].setParams(stepPins[i],dirPins[i]);
    motors[i].setStopper(ESPins[i]);
    motors[i].setMotorDelay(MOTOR_DELAY); 
  }
  pinMode(X_DIR, OUTPUT); pinMode(X_STP, OUTPUT);
  pinMode(Y_DIR, OUTPUT); pinMode(Y_STP, OUTPUT);

  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);
 
}

void loop() {

//check if anything is running
  if (!mPressed){
    if (runMotors()) return;
  }
  else {
    runMotors();
  }
if (Serial.available()>0) {


    
    String line = Serial.readString();
    char action = line[0];
    String motor = line.substring(2,4);
    //Serial.println(motor.toInt());
    String steps = line.substring(5);
    //Serial.println(steps.toInt());
    
    if (action == 'Z'){
      motors[0].runToZero();
      motors[1].runToZero();
    }

    if (action == 'S') {
      
      motors[motor.toInt()].stopRunning();
      mPressed = false;
    }
    
    if (action == 'P') {

      if (steps.toInt()<0) {
        motors[motor.toInt()].setRunning(LOW, 1000, abs(steps.toInt()));
      }
      else {
        motors[motor.toInt()].setRunning(HIGH, 1000, abs(steps.toInt()));
      }
    }
    
    if (action == 'M') {
      if (steps.toInt()<0) {
        motors[motor.toInt()].setRunning(LOW, 1000, 1000000*abs(steps.toInt()));
      }
      else {
        motors[motor.toInt()].setRunning(HIGH, 1000, 1000000*abs(steps.toInt()));
      }
      mPressed = true;
    }

    if (action == 'X')
      Serial.println(motors[motor.toInt()].getPosition());
      delay(100);
    }  
}

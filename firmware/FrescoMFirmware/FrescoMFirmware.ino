#include "Pins.h" 
#include "EndStopper.h"
#include "Command.h"
#include "EndStopper.h"
#include "FrescoMotor.h"
#include "FrescoXYZ.h"
#include "MotorController.h"
#include "Parser.h"
#include "Manifold.h"

int stepPins[] = {XS1, YS1, ZS1, AS1, XS2, YS2, ZS2, AS2, XS3, YS3, ZS3, AS3};
int dirPins[] = {XD1, YD1, ZD1, AD1, XD2, YD2, ZD2, AD2, XD3, YD3, ZD3, AD3};
int endStopperPins[] = {ES1, ES2, ES3, ES4, ES5, ES6, ES7, ES8, ES9, ES10, ES11, ES12};

void setupPinsModeEndSetEnabled() {
  
  for (int i = 0; i < NUM_MOTORS; i++){
    pinMode(stepPins[i], OUTPUT);
    pinMode(dirPins[i], OUTPUT);
    pinMode(endStopperPins[i], INPUT);
  }

  pinMode(EN, OUTPUT);
  pinMode(LEDW, OUTPUT);
  digitalWrite(EN, LOW);
  digitalWrite(LEDW, LOW);
}

void setupSerial() {
  Serial.begin (250000); 
  Serial.setTimeout(25);
}

FrescoXYZ* frescoXYZ;
Parser* frescoParser;

void setup() {
  setupSerial();

  setupPinsModeEndSetEnabled();
  
  FrescoMotor* xMotor = new FrescoMotor(XS1, XD1);
  FrescoMotor* yMotor = new FrescoMotor(YS1, YD1);
  FrescoMotor* zMotor = new FrescoMotor(ZS1, ZD1);

  EndStopper* xStopper = new EndStopper(ES1);
  EndStopper* yStopper = new EndStopper(ES2);
  EndStopper* zStopper = new EndStopper(ES3);

  MotorController* xMotorController = new MotorController(xMotor, xStopper, true);
  MotorController* yMotorController = new MotorController(yMotor, yStopper, true);
  MotorController* zMotorController = new MotorController(zMotor, zStopper, true);

  FrescoMotor* manifoldZMotor = new FrescoMotor(AS1, AD1);
  EndStopper* manifoldZStopper = new EndStopper(ES4);
  
  MotorController* manifoldZController = new MotorController(manifoldZMotor, manifoldZStopper, false);

  FrescoMotor* pump0Motor = new FrescoMotor(XS2, XD2);
  MotorController* pump0 = new MotorController(pump0Motor, NULL, true);

  FrescoMotor* pump1Motor = new FrescoMotor(YS2, YD2);
  MotorController* pump1 = new MotorController(pump1Motor, NULL, true);
  
  MotorController *pumps[] = {pump0, pump1};
  Manifold* manifold = new Manifold(manifoldZController, 2, pumps);

  frescoXYZ = new FrescoXYZ(xMotorController, yMotorController, zMotorController, manifold);
  frescoParser = new Parser();
}

void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readString();
    Command command = frescoParser->parse(line);
    frescoXYZ->perform(command);
  }
}

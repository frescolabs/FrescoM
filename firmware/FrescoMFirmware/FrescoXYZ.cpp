#include "FrescoXYZ.h"    
#include "Point.h"
#include <EEPROM.h>

#define BOTTOM_RIGHT_X_KEY 1
#define BOTTOM_RIGHT_Y_KEY 5
#define TOP_LEFT_X_KEY 9
#define TOP_LEFT_Y_KEY 13

FrescoXYZ::FrescoXYZ(MotorController* xMotorController, 
                     MotorController* yMotorController, 
                     MotorController* zMotorController) {
                      
  this->xMotorController = xMotorController;
  this->yMotorController = yMotorController;
  this->zMotorController = zMotorController;
      
  this->xLeftPostition = -1;
  this->xRightPosition = -1;
  this->yTopPosition = -1;
  this->yBottomPosition = -1;
  this->xLength = -1;
  this->yLength = -1;
}

  void FrescoXYZ::setPosition(long x, 
                              long y, 
                              long z) {
      this->xMotorController->goToPosition(x);
      this->yMotorController->goToPosition(y);
      this->zMotorController->goToPosition(z);
  }
  
  void FrescoXYZ::moveDelta(long x, 
                            long y, 
                            long z) {
      this->xMotorController->goDelta(x);
      this->yMotorController->goDelta(y);
      this->zMotorController->goDelta(z);
  }

  void FrescoXYZ::goToZero() {
    xMotorController->goToZero();
    yMotorController->goToZero();
    zMotorController->goToZero();
  }

  long FrescoXYZ::getXLength() {
    // TODO: Implement
  }

  long FrescoXYZ::getYLength() {
    // TODO: Implement
  }

  Point FrescoXYZ::getBottomRight() {
    Point point = Point(0, 0);
    point.x = xMotorController->getAxisStart();
    point.y = yMotorController->getAxisEnd();
    return point;
  }
  
  Point FrescoXYZ::getTopLeft() {
    Point point = Point(0, 0);
    point.x = xMotorController->getAxisEnd();
    point.y = yMotorController->getAxisStart();
    return point;
  }
  
  void FrescoXYZ::perform(Command command) {
    switch (command.type) {
      case GoToZero:
        this->goToZero();
        break;
      case GoToZeroVerticalZ:
        this->zMotorController->goToZero();
        break;
      case SetPosition:
        this->setPosition(command.parameter0.toInt(), command.parameter1.toInt(), command.parameter2.toInt());
        break;
      case MoveDelta:
        this->moveDelta(command.parameter0.toInt(), command.parameter1.toInt(), command.parameter2.toInt());
        break;
      case SetBottomRight:
        this->xMotorController->rememberStartPosition();
        this->yMotorController->rememberEndPosition();
        this->saveBottomRightPosition();
        break;
      case SetTopLeft:
        this->xMotorController->rememberEndPosition();
        this->yMotorController->rememberStartPosition();
        this->saveTopLeftPosition();
        break;
      case GetTopLeftBottomRightCoordinates:
        // TODO: Move serial response to another class
        Point topLeft = this->restoreTopLeftPosition();
        Point bottomRight = this->restoreBottomRightPosition();
        Serial.print("Response " + String(topLeft.x) + " " + String(topLeft.y) + " " + String(bottomRight.x) + " " + String(bottomRight.y) + "\n");
        break;
    }
  }

  void FrescoXYZ::saveBottomRightPosition() {
    Point point = this->getBottomRight();
    this->EEPROMWritelong(BOTTOM_RIGHT_X_KEY, point.x);
    this->EEPROMWritelong(BOTTOM_RIGHT_Y_KEY, point.y);
  }
  
  void FrescoXYZ::saveTopLeftPosition() {
    Point point = this->getTopLeft();
    this->EEPROMWritelong(TOP_LEFT_X_KEY, point.x);
    this->EEPROMWritelong(TOP_LEFT_Y_KEY, point.y);
  }

  long FrescoXYZ::EEPROMReadlong(long address) {
    long four = EEPROM.read(address);
    long three = EEPROM.read(address + 1);
    long two = EEPROM.read(address + 2);
    long one = EEPROM.read(address + 3);
    return ((four << 0) & 0xFF) + ((three << 8) & 0xFFFF) + ((two << 16) & 0xFFFFFF) + ((one << 24) & 0xFFFFFFFF);
  }

  void FrescoXYZ::EEPROMWritelong(int address, long value) {
    byte four = (value & 0xFF);
    byte three = ((value >> 8) & 0xFF);
    byte two = ((value >> 16) & 0xFF);
    byte one = ((value >> 24) & 0xFF);
    EEPROM.write(address, four);
    EEPROM.write(address + 1, three);
    EEPROM.write(address + 2, two);
    EEPROM.write(address + 3, one);
  }

  Point FrescoXYZ::restoreBottomRightPosition() {
    Point point = Point(this->EEPROMReadlong(BOTTOM_RIGHT_X_KEY), this->EEPROMReadlong(BOTTOM_RIGHT_Y_KEY));
    return point;
  }
  
  Point FrescoXYZ::restoreTopLeftPosition() {
    Point point = Point(this->EEPROMReadlong(TOP_LEFT_X_KEY), this->EEPROMReadlong(TOP_LEFT_Y_KEY));
    return point;
  }
  

#include "FrescoXYZ.h"    
#include "Point.h"
#include <EEPROM.h>
#include "Pins.h"

#define BOTTOM_RIGHT_X_KEY 1
#define BOTTOM_RIGHT_Y_KEY 5
#define TOP_LEFT_X_KEY 9
#define TOP_LEFT_Y_KEY 13

FrescoXYZ::FrescoXYZ(MotorController* xMotorController, 
                     MotorController* yMotorController, 
                     MotorController* zMotorController,
                     Manifold* manifold,
                     MOSFETLED* whiteLed,
                     DriverLED* blueLed) {
                      
  this->xMotorController = xMotorController;
  this->yMotorController = yMotorController;
  this->zMotorController = zMotorController;
  this->manifold = manifold;
  this->whiteLed = whiteLed;
  this->blueLed = blueLed;
      
  this->xLeftPostition = -1;
  this->xRightPosition = -1;
  this->yTopPosition = -1;
  this->yBottomPosition = -1;
  this->xLength = -1;
  this->yLength = -1;

  this->responder = new Responder();
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
    zMotorController->goToZero();
    xMotorController->goToZero();
    yMotorController->goToZero();
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
    
    Response response;
    // By default is Done, every operation can change it
    response.type = Done;
    
    // For some reason switch doesn't work here after some cases, so had to rewrite to if / else  
    if (command.type == GoToZero) {
        this->goToZero();
    }
    else if (command.type == GoToZeroVerticalZ) {
        this->zMotorController->goToZero();
    }
    else if (command.type == ManifoldDelta) {
        this->manifold->goDeltaZ(command.parameter0.toInt());
    }
    else if (command.type == ManifoldZero) {
        this->manifold->goToZeroVerticalZ();
    }
    else if (command.type == DeltaPump) {
        this->manifold->deltaPump(command.parameter0.toInt(), command.parameter1.toInt());
    }
    else if (command.type == SetPosition) {
        this->setPosition(command.parameter0.toInt(), command.parameter1.toInt(), command.parameter2.toInt());
    }
    else if (command.type == MoveDelta) {
        this->moveDelta(command.parameter0.toInt(), command.parameter1.toInt(), command.parameter2.toInt());
    }
    else if (command.type == SetBottomRight) {
        this->xMotorController->rememberStartPosition();
        this->yMotorController->rememberEndPosition();
        this->saveBottomRightPosition();
    }
    else if (command.type == SetTopLeft) {
        this->xMotorController->rememberEndPosition();
        this->yMotorController->rememberStartPosition();
        this->saveTopLeftPosition();
    }
    else if (command.type == GetTopLeftBottomRightCoordinates) {
        Point topLeft = this->restoreTopLeftPosition();
        Point bottomRight = this->restoreBottomRightPosition();
        response.type = GetTopLeftBottomRightCoordinatesResponse;
        response.parameter0 = String(topLeft.x);
        response.parameter1 = String(topLeft.y);
        response.parameter2 = String(bottomRight.x);
        response.parameter3 = String(bottomRight.y);
    }
    else if (command.type == ManifoldZero) {
        this->manifold->goToZeroVerticalZ();
    }
    else if (command.type == SwitchLedW) {
        this->whiteLed->set(command.parameter0.toInt() == 1);
    }
    else if (command.type == SwitchLedB) {
        this->blueLed->set(command.parameter0.toInt() == 1);
    }
    else if (command.type == Unknown) {
      response.type = UnknownCommand;
    }

    responder->respond(response);
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
  

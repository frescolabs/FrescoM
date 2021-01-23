#include "Responder.h"
#include "Command.h"

void Responder::respond(Response response) {
  if (response.type == Done) {
      Serial.print("Done \n");
  }
  else if (response.type == GetTopLeftBottomRightCoordinatesResponse) {
      Serial.print("EdgeCoordinates " + response.parameter0 + " " + response.parameter1 + " " + response.parameter2 + " " + response.parameter3 + "\n");
  }
  else if (response.type == UnknownCommand) {
      Serial.print("UnknownCommand \n");
  }
}

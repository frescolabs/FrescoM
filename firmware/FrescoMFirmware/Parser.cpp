#include "Parser.h"

int countDividersNumber(String string, char divider) {
  int dividersNumber = 0;
  for (int i = 0; i++; i < string.length()) {
    if (string[i] == divider) {
      dividersNumber++;
    }
  }
  return dividersNumber;
}

Command Parser::parse(String line) {
  
  int coursor = 0;
  int dividerCount = 0;
  int previousDividerIndex = 0;
  
  Command command;

  line.concat(' ');
  
  while (coursor < line.length()) {
    
    if (line[coursor] == ' ') {
      if (dividerCount == 0) {
        command.name = line.substring(0, coursor);
      }
      else if (dividerCount == 1) {
        command.parameter0 = line.substring(previousDividerIndex, coursor);
      }
      else if (dividerCount == 2) {
        command.parameter1 = line.substring(previousDividerIndex, coursor);
      }
      else if (dividerCount == 3) {
        command.parameter2 = line.substring(previousDividerIndex, coursor);
      }
      
      previousDividerIndex = coursor;
      dividerCount++;
    }
    
    coursor++;
  }
 
  if (command.name.compareTo("Zero") == 0) {
    command.type = GoToZero;
  } 
  else if (command.name.compareTo("VerticalZero") == 0) {
    command.type = GoToZeroVerticalZ;
  }
  else if (command.name.compareTo("SetPosition") == 0) {
    command.type = SetPosition;
  }
  else if (command.name.compareTo("Delta") == 0) {
    command.type = MoveDelta;
  }
  else if (command.name.compareTo("RememberTopLeft") == 0) {
    command.type = SetTopLeft;
  }
  else if (command.name.compareTo("RememberBottomRight") == 0) {
    command.type = SetBottomRight;
  }
  else if (command.name.compareTo("GetTopLeftBottomRightCoordinates") == 0) {
    command.type = GetTopLeftBottomRightCoordinates;
  }
  else {
    command.type = Unknown;
  }

  return command;
}

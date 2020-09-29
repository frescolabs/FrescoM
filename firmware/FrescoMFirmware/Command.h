#ifndef Command_h
#define Command_h

#include <Arduino.h>

/*
 *  Protocol of communication with Fresco Arch:
 *  
 *  At first you need to define RememberTopLeft and RememberBottomRight by
 *  alligning top left and bottom right wells with an objective.
 *  
 *  This will set global coordinates.
 * 
 *  Commands:
 *  
 *  Zero -> Go to Zero
 *  VerticalZero -> Go to Zero for Z
 *  Position 100 1000 100 -> Set Position
 *  Delta 0 0 10 -> Move to Delta
 *  RememberTopLeft -> Remember top left
 *  RememberBottomRight -> Remember bottom right
 *  GetTopLeftBottomRightCoordinates -> Send coordinates for the plate
 *  
 */

enum CommandType {
  GoToZero,
  GoToZeroVerticalZ,
  SetPosition,
  MoveDelta,
  SetTopLeft,
  SetBottomRight,
  GetTopLeftBottomRightCoordinates,
  Unknown
};

struct Command {
  CommandType type;
  String name;
  String parameter0;
  String parameter1;
  String parameter2;
};

#endif

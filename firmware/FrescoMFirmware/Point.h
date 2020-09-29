#ifndef Point_h
#define Point_h

#include "Command.h"

struct Point {

  Point::Point(long x, long y) {
    this->x = x;
    this->y = y;
  }

  long x;
  long y;
  
};

#endif

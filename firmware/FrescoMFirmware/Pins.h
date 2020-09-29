#ifndef Pins_h
#define Pins_h


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

#endif

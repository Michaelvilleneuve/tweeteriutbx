/***************************************************
  This is a library for our I2C LED Backpacks

  Designed specifically to work with the Adafruit LED Matrix backpacks
  ----> http://www.adafruit.com/products/872
  ----> http://www.adafruit.com/products/871
  ----> http://www.adafruit.com/products/870

  These displays use I2C to communicate, 2 pins are required to
  interface. There are multiple selectable I2C addresses. For backpacks
  with 2 Address Select pins: 0x70, 0x71, 0x72 or 0x73. For backpacks
  with 3 Address Select pins: 0x70 thru 0x77

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h>
#include <stdbool.h>
#include "Adafruit_GFX.h"
#include "Adafruit_LEDBackpack.h"

#define SLAVE_ADDRESS 0x12


int dataReceived = 0;
String socialMessage;
bool initArithmo = 0;
Adafruit_8x8matrix matrix[4];
static const uint8_t PROGMEM
arithmo_a[] = {B001110,B010010,B100010,B101010,B100010,B101010,B101010,B111110},
arithmo_r[] = {B111100,B100110,B101010,B101010,B100010,B101010,B101010,B111110},
arithmo_i[] = {B111110,B110110,B111110,B110110,B110110,B110110,B110110,B111110},
arithmo_t[] = {B111110,B100010,B110110,B010100,B010100,B010100,B010100,B011100},
arithmo_h[] = {B111110,B101010,B101010,B100010,B101010,B101010,B111010,B111110},
arithmo_m[] = {B001110,B011010,B110010,B100010,B100010,B101010,B101010,B111110},
arithmo_o[] = {B001110,B010010,B100010,B101010,B101010,B101010,B100010,B111110};

void setup() {
  Serial.println("Arduino is up");
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  for(int i = 0 ; i < 4 ; i++) {
    Adafruit_8x8matrix matrix[i] = Adafruit_8x8matrix();
  }
  for(int i = 0 ; i < 4 ; i++) {
    matrix[i].begin(0x70 + i);
  }
}

void initMatrix() {
  for (int i = 0 ; i < 4 ; i++) {
    matrix[i].setTextSize(1);
    matrix[i].setTextWrap(false);
    matrix[i].setTextColor(LED_ON);
  }
}



void receiveEvent(int byteCount){
  String message = "";
  Serial.println("ReceiveEvent: " + byteCount);
  while (Wire.available()) {
    char c = Wire.read();
    message = message + (String)c;
  }
  socialMessage = message;
  if(initArithmo == 0) {
    initArithmo = 1;
  }
}



void writeDisplayMessage(String message, int displayDelay) {
  int messageLength = message.length();
  for (int x = 8 ; x >= - (messageLength * 6) - 24 ; x--) {
    for (int i = 0 ; i < 4 ; i++) {
      matrix[i].clear();
      matrix[i].setCursor(x + (i * 8), 0);
      matrix[i].print(message);
      matrix[i].writeDisplay();
    }
    delay(displayDelay);
  }
}

/*void writeDisplayFollow(String social, float number, int displayDelay) {
  String message = social + ":";
  if(number >= 1000000) {
    number /= 1000000;
    message = message + number + "M";
  }
  else if(number >= 100000) {
    number /= 1000;
    message = message + int(number) + "K";
  }
  else {
    message = message + int(number);
  }
  writeDisplayMessage(message, displayDelay);
}*/

void writeDisplayMatrix(String matrixName, int displayDelay) {
  if(matrixName == "arithmo") {
    for (int x = 8 ; x >= -44 - 24 ; x--) {
      for (int i = 0 ; i < 4 ; i++) {
        matrix[i].clear();
        matrix[i].drawBitmap(x + (i * 8) + 0, 0, arithmo_a, 8, 8, LED_ON);
        matrix[i].drawBitmap(x + (i * 8) + 6, 0, arithmo_r, 8, 8, LED_ON);
        matrix[i].drawBitmap(x + (i * 8) + 12, 0, arithmo_i, 8, 8, LED_ON);
        matrix[i].drawBitmap(x + (i * 8) + 18, 0, arithmo_t, 8, 8, LED_ON);
        matrix[i].drawBitmap(x + (i * 8) + 24, 0, arithmo_h, 8, 8, LED_ON);
        matrix[i].drawBitmap(x + (i * 8) + 30, 0, arithmo_m, 8, 8, LED_ON);
        matrix[i].drawBitmap(x + (i * 8) + 36, 0, arithmo_o, 8, 8, LED_ON);
        matrix[i].writeDisplay();
      }
      delay(displayDelay);
    }
  }
}



void loop() {
  for (int i = 0 ; i < 4 ; i++) {
    matrix[i].clear();
  }
  initMatrix();

  if(initArithmo == 0) {
    writeDisplayMatrix("arithmo", 50);
  }
  if(initArithmo == 0) {
    writeDisplayMessage("...Initialisation...", 10);
  }

  writeDisplayMessage(socialMessage, 40);

  delay(1000);
}

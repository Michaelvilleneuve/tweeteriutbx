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
#include "Adafruit_GFX.h"
#include "Adafruit_LEDBackpack.h"

Adafruit_8x8matrix matrix[4];

/*static const uint8_t PROGMEM
arithmo_A[] = {
  B001110,
  B010010,
  B100010,
  B101010,
  B100010,
  B101010,
  B101010,
  B111110
},
arithmo_R[] = {
  B111100,
  B100110,
  B101010,
  B101010,
  B100010,
  B101010,
  B101010,
  B111110
},
arithmo_I[] = {
  B111110,
  B110110,
  B111110,
  B110110,
  B110110,
  B110110,
  B110110,
  B111110
},
arithmo_T[] = {
  B111110,
  B100010,
  B110110,
  B010100,
  B010100,
  B010100,
  B010100,
  B011100
},
arithmo_H[] = {
  B111110,
  B101010,
  B101010,
  B100010,
  B101010,
  B101010,
  B111010,
  B111110
},
arithmo_M[] = {
  B001110,
  B011010,
  B110010,
  B100010,
  B100010,
  B101010,
  B101010,
  B111110
},
arithmo_0[] = {
  B001110,
  B010010,
  B100010,
  B101010,
  B101010,
  B101010,
  B100010,
  B111110
};*/

void setup() {
  Serial.begin(9600);
  Serial.println("8x8 LED Matrix Test");
  for(uint8_t i = 0 ; i < 4 ; i++) {
    Adafruit_8x8matrix matrix[i] = Adafruit_8x8matrix();
  }
  for(uint8_t i = 0 ; i < 4 ; i++) {
    matrix[i].begin(0x70 + i);
  }
}

void initMatrix() {
  for (int8_t i = 0 ; i < 4 ; i++) {
    matrix[i].setTextSize(1);
    matrix[i].setTextWrap(false);
    matrix[i].setTextColor(LED_ON);
  }
}

void writeDisplayMessage(String msg) {
  
  uint8_t temp = msg.length();
  for (int8_t x = 8 ; x >= -(temp*6)-24; x--) {
    for (int8_t i = 0 ; i < 4 ; i++) {
      matrix[i].clear();
      matrix[i].setCursor(x + (i * 8), 0);
      matrix[i].print(msg);
      matrix[i].writeDisplay();
    }
    delay(100);
  }
}

/*void writeDisplayMatrix() {
  matrix[0].drawBitmap(0, 0, arithmo_A, 8, 8, LED_ON);
  matrix[0].writeDisplay();
  matrix[1].writeDisplay();
  matrix[2].writeDisplay();
  matrix[3].writeDisplay();
  delay(2500);
}*/

void loop() {
  for (int8_t i = 0 ; i < 4 ; i++) {
    matrix[i].clear();
  }
  initMatrix();
  
  writeDisplayMessage("Projet");
  writeDisplayMessage("Arithmo");
  writeDisplayMessage("Twitter:123459");
  writeDisplayMessage("Twitter:12345");
  
  /*writeDisplayMatrix(arithmo_M);*/

  delay(1000);
}

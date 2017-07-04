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
#include <stdbool.h>

Adafruit_8x8matrix matrix[4];
bool init_arithmo = 0;
static const uint8_t PROGMEM
arithmo_a[] = {B001110,B010010,B100010,B101010,B100010,B101010,B101010,B111110},
arithmo_r[] = {B111100,B100110,B101010,B101010,B100010,B101010,B101010,B111110},
arithmo_i[] = {B111110,B110110,B111110,B110110,B110110,B110110,B110110,B111110},
arithmo_t[] = {B111110,B100010,B110110,B010100,B010100,B010100,B010100,B011100},
arithmo_h[] = {B111110,B101010,B101010,B100010,B101010,B101010,B111010,B111110},
arithmo_m[] = {B001110,B011010,B110010,B100010,B100010,B101010,B101010,B111110},
arithmo_o[] = {B001110,B010010,B100010,B101010,B101010,B101010,B100010,B111110};

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

void writeDisplayMessage(String message, int displayDelay) {
  uint8_t messageLength = message.length();
  for (int8_t x = 8 ; x >= -(messageLength * 6) - 24 ; x--) {
    for (int8_t i = 0 ; i < 4 ; i++) {
      matrix[i].clear();
      matrix[i].setCursor(x + (i * 8), 0);
      matrix[i].print(message);
      matrix[i].writeDisplay();
    }
    delay(displayDelay);
  }
}

void writeDisplayFollowers(String social, float number, int displayDelay) {
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
}

void writeDisplayMatrixLogoArithmo(int displayDelay) {
  for (int8_t x = 8 ; x >= -44 - 24 ; x--) {
    for (int8_t i = 0 ; i < 4 ; i++) {
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
  init_arithmo = 1;
}

void loop() {
  for (int8_t i = 0 ; i < 4 ; i++) {
    matrix[i].clear();
  }
  initMatrix();

  if(init_arithmo == 0) {
    writeDisplayMatrixLogoArithmo(50);
  }
  
  writeDisplayFollowers("Twitter", 1234567, 40);
  writeDisplayFollowers("Twitch", 12345, 40);
  writeDisplayFollowers("Facebook", 123456, 40);
  writeDisplayFollowers("Instagram", 1234, 40);

  delay(1000);
}

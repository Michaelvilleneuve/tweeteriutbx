#include <Wire.h>

#define SLAVE_ADDRESS 0x12
int dataReceived = 0;

void setup() {
    Serial.begin(9600);
    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
}

void loop() {
    delay(100);
}

void receiveData(int byteCount){
    while(Wire.available()) {
        dataReceived = Wire.read();
        Serial.print("Donnee recue : ");
        Serial.println(dataReceived);
    }
}

void sendData(){
    int envoi = dataReceived + 1;
    Wire.write(envoi);
}

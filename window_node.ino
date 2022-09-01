#include <SPI.h>
#include <RF24.h>
#include <RF24Network.h>
#include <LowPower.h>

RF24 radio(9,10);
RF24Network windows(radio);

const uint16_t centralNode = 00;
const uint16_t thisNode = 01; // node adress

float val = 0.0;
int batteryLevel = 29;
float analogValue;
float voltage;

void setup(){
  SPI.begin();
  radio.begin();
  windows.begin(80, thisNode);
  radio.setDataRate(RF24_250KBPS);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
  analogReference(INTERNAL);
  analogValue = analogRead(A3);

  pinMode(A3, INPUT);
  pinMode(2, INPUT);
  digitalWrite(2, HIGH);
}

void loop(){
  if(digitalRead(2) == LOW) val = 1.0;
  else val = 0.0;
  
  RF24NetworkHeader header(centralNode);
  if(batteryLevel >= 30){
    analogValue = analogRead(A3);
    voltage = analogValue * (3.3/1024.0);
    radio.powerUp();
    windows.write(header, &voltage, sizeof(voltage));
    radio.powerDown();
    batteryLevel = 0;
  }
  else{
    radio.powerUp();
    windows.write(header, &val, sizeof(val));
    radio.powerDown();
  }
  batteryLevel++;
  LowPower.powerDown(SLEEP_2S, ADC_OFF, BOD_OFF);
}

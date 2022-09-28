#include <SPI.h>
#include <RF24.h>
#include <RF24Network.h>
#include <LowPower.h>
#include <DHT.h>

#define DHT22PIN 2
#define DHTTYPE DHT22
DHT dht(DHT22PIN, DHTTYPE);
RF24 radio(9,10);
RF24Network windows(radio);

const uint16_t centralNode = 00;
const uint16_t thisNode = 05; // node adress

float val = 0.0;
int batteryLevel = 29;
float analogValue;
float voltage;
float h, oldH;
float t, oldT;
bool whichNode = false;

void setup(){
  Serial.begin(9600);
  SPI.begin();
  dht.begin();
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
  RF24NetworkHeader header(centralNode);
  if(batteryLevel >= 30){
    analogValue = analogRead(A3);
    voltage = analogValue * (7.2/1024.0);
    if(whichNode == true) voltage += 1000.0;
    //Serial.print("Napiecie: ");           //wyświetlenie napiecia
    //Serial.print(voltage);
    //Serial.println("V");
    radio.powerUp();
    windows.write(header, &voltage, sizeof(voltage));
    radio.powerDown();
    batteryLevel = 0;
  }
    //Serial.print("Wilgotnosc: ");              //wyświetlenie wartości wilgotności
    //Serial.print(h);
    //Serial.println(" %");
  oldT = t;
  t = dht.readTemperature();
  delay(2000);
  
  oldH = (h - 100.0);
  h = dht.readHumidity();
  delay(2000);
  h += 100.0;

  if(whichNode == true){
    t += 1000.0;
    h += 1000.0;
  }
  if((batteryLevel % 2) == 0){
    radio.powerUp();
    windows.write(header, &t, sizeof(t));  
    radio.powerDown();
  }

  else{
    radio.powerUp();
    windows.write(header, &h, sizeof(h));  
    radio.powerDown();
  }
  
  batteryLevel++;
  LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);
}

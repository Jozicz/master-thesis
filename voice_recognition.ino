#include <SoftwareSerial.h>
#include "VoiceRecognitionV3.h"

VR myVR(10,11);

uint8_t buf[64];

bool CHECK_STATE = 0, BATHROOM = 0, WHICH_BATHROOM = 0, SWITCH_ALARM = 0;

void printSignature(uint8_t *buf, int len)
{
  int i;
  for(i=0; i<len; i++){
    if(buf[i]>0x19 && buf[i]<0x7F){
      Serial.write(buf[i]);
    }
    else{
      Serial.print("[");
      Serial.print(buf[i], HEX);
      Serial.print("]");
    }
  }
}

void printVR(uint8_t *buf)
{
  Serial.println("VR Index\tGroup\tRecordNum\tSignature");

  Serial.print(buf[2], DEC);
  Serial.print("\t\t");

  if(buf[0] == 0xFF){
    Serial.print("NONE");
  }
  else if(buf[0]&0x80){
    Serial.print("UG ");
    Serial.print(buf[0]&(~0x80), DEC);
  }
  else{
    Serial.print("SG ");
    Serial.print(buf[0], DEC);
  }
  Serial.print("\t");

  Serial.print(buf[1], DEC);
  Serial.print("\t\t");
  if(buf[3]>0){
    printSignature(buf+4, buf[3]);
  }
  else{
    Serial.print("NONE");
  }
  Serial.println("\r\n");
}

void setup()
{
  myVR.begin(4800);
  Serial.begin(115200);
    
  if(myVR.clear() == 0){
    Serial.println("Recognizer cleared.");
  }else{
    Serial.println("Not find VoiceRecognitionModule.");
    Serial.println("Please check connection and restart Arduino.");
    while(1);
  }
  myVR.load((uint8_t)0);  // CHECK STATE
  myVR.load((uint8_t)1);  // BATHROOM
  myVR.load((uint8_t)2);  // SWITCH ALARM
}

void loop()
{
  int ret;
  ret = myVR.recognize(buf, 50);
  if(ret>0){
    switch(buf[1]){
      case 0:     // CHECK STATE
        myVR.clear();
        myVR.load((uint8_t)4);  // first
        myVR.load((uint8_t)5);  // second
        myVR.load((uint8_t)6);  // third
        myVR.load((uint8_t)7);  // fourth
        myVR.load((uint8_t)10); // all
        myVR.load((uint8_t)3);  // exit
        CHECK_STATE = 1;
        Serial.write("Check state of which window?\n");
        break;
      case 1:     // BATHROOM
        myVR.clear();
        myVR.load((uint8_t)4);  // first
        myVR.load((uint8_t)5);  // second
        myVR.load((uint8_t)3);  // exit
        BATHROOM = 1;
        Serial.write("Check state of which bathroom?\n");
        break;
      case 2:     // SWITCH ALARM
        myVR.clear();
        myVR.load((uint8_t)11); // on
        myVR.load((uint8_t)12); // off
        myVR.load((uint8_t)3);  // exit
        SWITCH_ALARM = 1;
        Serial.write("Switch the alarm on or off?");
        break;
      case 3:     // EXIT
        myVR.clear();
        myVR.load((uint8_t)0);  // check state
        myVR.load((uint8_t)1);  // bathroom
        myVR.load((uint8_t)2);  // switch alarm
        CHECK_STATE = 0;
        BATHROOM = 0;
        WHICH_BATHROOM = 0;
        SWITCH_ALARM = 0;
        break;
      case 4: case 5: case 6: case 7: case 10:   // FIRST, SECOND, THIRD, FOURTH, ALL
        if(CHECK_STATE){
          myVR.clear();
          myVR.load((uint8_t)0);  // check state
          myVR.load((uint8_t)1);  // bathroom
          myVR.load((uint8_t)2);  // switch alarm
          CHECK_STATE = 0;
          if(buf[1] == 4)
            Serial.write("First window is ...");
          else if(buf[1] == 5)
            Serial.write("Second window is ...");
          else if(buf[1] == 6)
            Serial.write("Third window is ...");
          else if(buf[1] == 7)
            Serial.write("Fourth window is ...");
          else if(buf[1] == 10)
            Serial.write("All windows are ...");
        }
        else if(BATHROOM){
          myVR.clear();
          myVR.load((uint8_t)9);  // temperature
          myVR.load((uint8_t)1);  // humidity
          myVR.load((uint8_t)3);  // exit
          if(buf[1] == 4){
            WHICH_BATHROOM = 1;
            Serial.write("First bathroom");
          }
          if(buf[1] == 5){
            WHICH_BATHROOM = 1;
            Serial.write("Second bathroom");
          }
          BATHROOM = 0;
        }
        break;
      case 8:     // TEMPERATURE
        if(WHICH_BATHROOM){
          myVR.clear();
          myVR.load((uint8_t)0);  // check state
          myVR.load((uint8_t)1);  // bathroom
          myVR.load((uint8_t)2);  // switch alarm
          WHICH_BATHROOM = 0;
          Serial.write("Temperature is ...");
        }
        break;
      case 9:     // HUMIDITY
        if(WHICH_BATHROOM){
          myVR.clear();
          myVR.load((uint8_t)0);  // check state
          myVR.load((uint8_t)1);  // bathroom
          myVR.load((uint8_t)2);  // switch alarm
          WHICH_BATHROOM = 0;
          Serial.write("Humidity is ...");
        }
        break;
      case 11:    // ON
        if(SWITCH_ALARM){
          myVR.clear();
          myVR.load((uint8_t)0);  // check state
          myVR.load((uint8_t)1);  // bathroom
          myVR.load((uint8_t)2);  // switch alarm
          SWITCH_ALARM = 0;
          Serial.write("Alarm switched on");
        }
        break;
      case 12:    // OFF
        if(SWITCH_ALARM){
          myVR.clear();
          myVR.load((uint8_t)0);  // check state
          myVR.load((uint8_t)1);  // bathroom
          myVR.load((uint8_t)2);  // switch alarm
          SWITCH_ALARM = 0;
          Serial.write("Alarm switched off");
        }
        break;
    }
    printVR(buf);
  }
}

#include <Wire.h>
#define ADDR 0b0100011

#include "DHT.h"
DHT dht;

#define DHT11_PIN 7

int pirPin = 32;
int pirStat = 0;  

void temperature(){
//  float dht_read = DHT.read11(DHT11_PIN);
float hum = dht.getTemperature();
  Serial.println(hum);
}

void humidity(){
//  float dht_read = DHT.read11(DHT11_PIN);
  Serial.println(dht.getHumidity());
}

void lightness(){
  int val = 0;
  Wire.beginTransmission(ADDR);
  Wire.write(0b00000111);
  Wire.endTransmission();
  Wire.beginTransmission(ADDR);
  Wire.write(0b00100000);
  Wire.endTransmission();
  delay(120);
  Wire.requestFrom(ADDR, 2);
  for (val = 0; Wire.available() >= 1; ) {
    char c = Wire.read();
    val = (val << 8) + (c & 0xFF);
  }
  val = val / 1.2;
//  Serial.print("lx: ");
  String to_ret = String(val);
  Serial.println(to_ret);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
//  Serial.println("Tutaj setup arduino");
  dht.setup(DHT11_PIN);
  pinMode(pirPin, INPUT);
  Wire.begin();
  Wire.beginTransmission(ADDR);
  Wire.write(0b00000001);
  Wire.endTransmission();
}
byte data;

char req;
boolean newData = false;

void getRequestedValue() {
    if (Serial.available() > 0) {
        req = Serial.read();
        newData = true;
    }
}

void processReq() {
    if (newData == true) {
      sendValue();
      newData = false;
    }
}

void sendValue(){
  switch (req){
      case 't':
      temperature();
      break;
      case 'h':
      humidity();
      break;
      case 'l':
      lightness();
      break;
    }
}
void loop() {
  getRequestedValue();
  processReq();
}

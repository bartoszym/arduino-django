/* ESP8266 TO PY: THE MICRO LIBRARY
 * Written by Junicchi
 * https://github.com/Kebablord

 * MAP
 - start(ssid,password)---> Connects to wifi with given username and password
 - waitUntilNewReq() -----> Waits until a new python request come, checks for requests regularly
 - returnThisInt(data) ---> sends your Integer data to localhost (python)
 - returnThisStr(data) ---> sends your String data to localhost (python)
 - getPath() -------------> gets the request path as string, ex: https://192.113.133/ledON -> "ledON"
*/

#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiClient.h>
const char* ssid = "Domek";
const char* password = "borysek2002";


// PORT
WiFiServer server(80);
WiFiClient client;
String rule;

void start(){
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.println("");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n");
  Serial.print("Połączono z ");
  Serial.println(WiFi.SSID());
  Serial.print("Adres IP: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("Ustawiono responder mDNS");
  } else {
    Serial.println("Błąd podczas ustawiania mDNS");
  }

  server.begin();
  Serial.println("Uruchomiono serwer TCP");

  MDNS.addService("http", "tcp", 80);
}

bool isNewRequest = false;

void CheckNewReq(){
  client = server.available();
  if (!client) {
    return;
  }

  while (client.connected() && !client.available()) {
    delay(1);
  }

  String req = client.readStringUntil('\r');
  int addr_start = req.indexOf(' ');
  int addr_end = req.indexOf(' ', addr_start + 1);
  if (addr_start == -1 || addr_end == -1) {
    Serial.print("Nieprawidłowy request: ");
    Serial.println(req);
    return;
  }
  req = req.substring(addr_start + 2, addr_end);
  Serial.print("Żądana ścieżka: ");
  Serial.println(req);

  rule = req;
  isNewRequest = true;
  client.flush();
}

void waitUntilNewReq(){
  do {CheckNewReq();} while (!isNewRequest);
  isNewRequest = false;
}

void returnThisStr(String final_data){
  String s;
  s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
  s += final_data;
  client.print(s);
  Serial.println("Powrót do klienta");
}
void returnThisInt(int final_data){
  returnThisStr(String(final_data));
}

String getPath(){
  return rule;
}

void returnData(){
  byte to_send = byte(rule.toInt());
  Serial.flush();
  while (Serial.available() > 0){
    Serial.read();
  }
  Serial.println(to_send);
  String received_data = Serial.readString();
  Serial.print("#");
  Serial.println(received_data);
  int val = received_data.toInt();
  returnThisInt(val);
}

void setup(void){
  Serial.begin(9600);
  start();
}

void loop(){
  waitUntilNewReq();
  returnData();
}

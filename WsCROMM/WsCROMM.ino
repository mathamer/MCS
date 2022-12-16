#include <SPI.h>
#include <WiFiNINA.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <ArduinoHttpClient.h> 
#include "MessageParser.h"
#include "arduino_secrets.h"

#include <utility/wifi_drv.h>
#define RGB_LED_GREEN 25
#define RGB_LED_RED 26
#define RGB_LED_BLUE 27

int sonda1 = 0;
int sonda2 = 0;
int sonda3 = 0;
int sonda4 = 0;
int sonda5 = 0;
int sonda6 = 0;

char ssid[] = SECRET_SSID;          
char pass[] = SECRET_PASS;
int status = WL_IDLE_STATUS;


char serverAddress[] = "192.168.4.8";
char serverPath[] = "/sensor";
int port = 31310;

String ServerMessage = "";
bool startExperiment = false;

// interval slanja podataka eksperimenta
const long interval = 2000;  
unsigned long previousMillis = 0;

WiFiClient wifi;
WebSocketClient client = WebSocketClient(wifi, serverAddress, port);
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

unsigned long getTime() {
  timeClient.update();
  unsigned long now = timeClient.getEpochTime();
  return now;
}

void SetLED(int r, int g, int b){
  WiFiDrv::analogWrite(RGB_LED_GREEN, r);
  WiFiDrv::analogWrite(RGB_LED_RED, g);
  WiFiDrv::analogWrite(RGB_LED_BLUE, b);
}

void setup() {
  WiFiDrv::pinMode(RGB_LED_GREEN, OUTPUT); 
  WiFiDrv::pinMode(RGB_LED_RED, OUTPUT); 
  WiFiDrv::pinMode(RGB_LED_BLUE, OUTPUT);

  SetLED(255, 211, 0);
    
  Serial.begin(9600);
  while (!Serial) {
    ; 
  }

  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    while (true);
  }


  String fv = WiFi.firmwareVersion();
  if (fv < "1.0.0") {
    Serial.println("Please upgrade the firmware");
  }

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }

//  configTime(0, 0, ntpServer);
  Serial.print("You're connected to the network");
  printCurrentNet();
  printWifiData();

}


String GenerateSensorData(bool status = false){
  String message = String(sonda1) + "," + String(sonda2) + "," + String(sonda3) + "," + String(sonda4) + "," + String(sonda5) + "," + String(sonda6);
  if(status) message = COMMAND_STATUS;
  return ParseSensorMessage(message, getTime());
}


void loop() {
  sonda1 = analogRead(0);
  sonda2 = analogRead(1);
  sonda3 = analogRead(2);
  sonda4 = analogRead(3);
  sonda5 = analogRead(4);
  sonda6 = analogRead(5);
  
  if(client.connected()){
    SetLED(0, 255, 0);
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval && startExperiment){
      SetLED(255, 0, 255);
      previousMillis = currentMillis;
      SendWsMessage(GenerateSensorData());
    }
    ReceiveWsMessage();
  }
  else{
    SetLED(255, 0, 0);
    Serial.println("starting WebSocket client");
    if(!client.connected()) client.begin(serverPath);
    Serial.print("Is client connected? -> ");
    Serial.println(client.connected());
  }
}



void SendWsMessage(String message){
  client.beginMessage(TYPE_TEXT);
  client.print(message);
  client.endMessage();
}

// read commands from websocket
void ReceiveWsMessage(){
  if(!client.connected()){
    Serial.println("Error sending data, client not connected");
  }
  int messageSize = client.parseMessage();
  if (messageSize > 0) {
    Serial.println("Received a message:");
    ServerMessage += client.readString();
    Serial.println(ServerMessage);
    if(ServerMessage.startsWith(COMMAND_START) && ServerMessage.endsWith(COMMAND_END)){
        ServerCommand command = ParseServerMessage(ServerMessage);
        if(!command.error){
          if(command.command == COMMAND_START_EXPERIMENT) startExperiment = true;
          if(command.command == COMMAND_STOP_EXPERIMENT) startExperiment  = false;
          if(command.command == COMMAND_STATUS) SendWsMessage(GenerateSensorData(true));
        }
        ServerMessage = "";
    }
    if(ServerMessage.length() > sizeof(COMMAND_START)){
      ServerMessage = ""; // in case of wrong or invalid command 
    }
  }
}


void printWifiData() {
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  Serial.println(ip);
}

void printCurrentNet() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.println(rssi);

  byte encryption = WiFi.encryptionType();
  Serial.print("Encryption Type:");
  Serial.println(encryption, HEX);
  Serial.println();
}

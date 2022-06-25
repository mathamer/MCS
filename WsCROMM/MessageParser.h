#include <ArduinoJson.h>

using namespace std;

#define COMMAND_START "START"
#define COMMAND_END "END"
#define COMMAND_START_EXPERIMENT "StartExperiment"
#define COMMAND_STOP_EXPERIMENT "StopExperiment"
#define COMMAND_STATUS "STATUS"

// arduino -> server 
class SensorCommand{
  public :
    String data;
    int timestamp;
};

// server -> arduino
class ServerCommand{
  public:
    String command;
    bool error;
};


ServerCommand ParseServerMessage(String message){
  message.replace(COMMAND_START, "");
  message.replace(COMMAND_END, "");
  Serial.println(message);

  DynamicJsonDocument doc(1024);
  deserializeJson(doc, message);

  ServerCommand command = ServerCommand();
  String cmd = doc["command"];
  command.command = cmd;
  command.error = false;
    
  return command; 
}

String ParseSensorMessage(String message, unsigned long timestamp){
  String response = "";
  
  DynamicJsonDocument doc(1024);
  doc["data"] = message;
  doc["timestamp"] = timestamp;
  serializeJson(doc, response);

  return response;
}

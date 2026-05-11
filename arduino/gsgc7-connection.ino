#include <SoftwareSerial.h>

SoftwareSerial Serial2(10, 11);

void setup() {
  // start communication with baud rate 9600
  Serial.begin(9600);   // Serial Monitor
  Serial2.begin(9600);  // RS232

  // wait a moment to allow serial ports to initialize
  delay(100);
  Serial.println("\nSerial Interfacer: UP\n");
}


void loop() {
  /*
  Read into string if serial available.
  If CR is received then return string and
  empty it in that order.
  */
  if (Serial2.available() > 0) {
    String content = Serial2.readString();
    Serial.println(content);
  }
  if (Serial.available() > 0){
    String command = Serial.readString();
    bool ans = false;
    
    while (!ans){
      if (Serial2.isListening()){
        
        bool ack = false;

        Serial2.flush();
        Serial2.print(command + " \r\n");
        Serial.println("Message sent... " + command);
        delay(140);

        while (Serial2.available()){
          String response = Serial2.readString();
          Serial.println(response);
          ack = true;
        }

        if (!ack) {
          Serial.println("<NOACK>");
        }

        ans = true;
// 
      }
    }
  }
}

// install IRremote(latest 4.x branch)
#include <IRremote.hpp>
// set the correct pins
#define IR_RECEIVE_PIN 2
#define LED 3

void setup()
{

  Serial.begin(9600); // // Establish serial communication
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK); // Start the receiver
  pinMode(LED, OUTPUT);
  // to make sure that it actually works
  digitalWrite(LED, HIGH);
  delay(100);
  digitalWrite(LED, LOW);
}

void loop() {
  // ...
  if (IrReceiver.decode()) {
      Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX); // Print "old" raw data
      // for the external led to flash on input
      digitalWrite(LED, HIGH);
      delay(50);
      digitalWrite(LED, LOW);
      IrReceiver.resume(); // Enable receiving of the next value
  }
  
}
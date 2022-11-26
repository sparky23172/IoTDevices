// Base ESP8266

#define LED 15
#define LED2 5

// This function runs once on startup
void setup() {
  // Initialize the serial port
  Serial.begin(115200);

  // Configure LED pin as an output
  pinMode(LED, OUTPUT);
  pinMode(LED2, OUTPUT);

}

// This function runs over and over again in a continuous loop
void loop() {
  Serial.println("Starting loop");
  Serial.println("Light On");
  // Turn the LED on (HIGH is the voltage level)
  digitalWrite(LED, HIGH);
  digitalWrite(LED2, LOW);

  // Wait for 1000 milliseconds
  delay(1000);

  // Turn the LED off by making the voltage LOW
  Serial.println("Light Off");
  digitalWrite(LED, LOW);
  digitalWrite(LED2, HIGH);

  // Wait another 1000 milliseconds
  delay(1000);

  // Send a message over the serial port
  Serial.println("Finished loop");
}

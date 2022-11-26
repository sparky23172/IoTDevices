/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp8266-nodemcu-hc-sr04-ultrasonic-arduino/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*********/

const int trigPin = 12;
const int echoPin = 14;

//define sound velocity in cm/uS
#define SOUND_VELOCITY 0.034
#define CM_TO_INCH 0.393701
#define GREEN 16
#define YELLOW 5
#define RED 4
#define BLUE 0

long duration;
float distanceCm;
float distanceInch;
float distanceM;
float distanceFeet;

void setup() {
  Serial.begin(115200); // Starts the serial communication
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(GREEN, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(RED, OUTPUT);
  pinMode(BLUE, OUTPUT);
}

void loop() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance
  distanceCm = duration * SOUND_VELOCITY/2;
  
  // Convert to inches
  distanceInch = distanceCm * CM_TO_INCH;
  
  // Prints the distance on the Serial Monitor
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
  if (distanceCm > 100) {
    distanceM = distanceCm/100;
    Serial.print("Distance (m): ");
    Serial.println(distanceM);
  }
  Serial.print("Distance (inch): ");
  Serial.println(distanceInch);
  if (distanceInch > 12) {
    distanceFeet = distanceInch/12;
    Serial.print("Distance (ft): ");
    Serial.println(distanceFeet);
  }

  if (int(distanceCm) > 100){
    Serial.printf("[+] Red\n\n\n");
    digitalWrite(GREEN, LOW);
    digitalWrite(YELLOW, LOW);
    digitalWrite(RED, HIGH);
    digitalWrite(BLUE, LOW);
  } else if (int(distanceCm) > 20 && int(distanceCm) < 100){
    Serial.printf("[+] Yellow\n\n\n");
    digitalWrite(GREEN, LOW);
    digitalWrite(YELLOW, HIGH);
    digitalWrite(RED, LOW);
    digitalWrite(BLUE, LOW);
  } else if (int(distanceCm) < 20){
    Serial.printf("[+] Green\n\n\n");
    digitalWrite(GREEN, HIGH);
    digitalWrite(YELLOW, LOW);
    digitalWrite(RED, LOW);
    digitalWrite(BLUE, LOW);
  } else {
    Serial.printf("[+] Failure...\n\n\n");
    digitalWrite(GREEN, HIGH);
    digitalWrite(YELLOW, HIGH);
    digitalWrite(RED, HIGH);
    digitalWrite(BLUE, HIGH);
  }

  delay(1000);
}
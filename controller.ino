// Smart Traffic Light System - Arduino Controller
// Listens for 'L1' or 'L2' via Serial to switch traffic light LEDs

// Define LED pins for Lane 1
const int lane1_red = 2;
const int lane1_yellow = 3;
const int lane1_green = 4;

// Define LED pins for Lane 2
const int lane2_red = 5;
const int lane2_yellow = 6;
const int lane2_green = 7;

String command = "";

void setup() {
  // Initialize Serial Communication at 9600 baud rate to match Python script
  Serial.begin(9600);

  // Initialize all LED pins as OUTPUT
  pinMode(lane1_red, OUTPUT);
  pinMode(lane1_yellow, OUTPUT);
  pinMode(lane1_green, OUTPUT);
  
  pinMode(lane2_red, OUTPUT);
  pinMode(lane2_yellow, OUTPUT);
  pinMode(lane2_green, OUTPUT);

  // Initial State: Lane 1 gets Green, Lane 2 gets Red
  digitalWrite(lane1_green, HIGH);
  digitalWrite(lane1_red, LOW);
  digitalWrite(lane1_yellow, LOW);
  
  digitalWrite(lane2_red, HIGH);
  digitalWrite(lane2_green, LOW);
  digitalWrite(lane2_yellow, LOW);
}

void loop() {
  // Check if data is available from the Python script via USB
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');
    command.trim(); // Remove any extra hidden whitespace or return characters

    if (command == "L1") {
      // Transition Lane 2 to Red, Lane 1 to Green
      
      // 1. Turn on Lane 2 Yellow for a safe transition
      digitalWrite(lane2_green, LOW);
      digitalWrite(lane2_yellow, HIGH);
      delay(1500); 
      digitalWrite(lane2_yellow, LOW);
      
      // 2. Set Lane 2 to Red
      digitalWrite(lane2_red, HIGH);

      // 3. Set Lane 1 to Green
      digitalWrite(lane1_red, LOW);
      digitalWrite(lane1_green, HIGH);
      
    } else if (command == "L2") {
      // Transition Lane 1 to Red, Lane 2 to Green
      
      // 1. Turn on Lane 1 Yellow for a safe transition
      digitalWrite(lane1_green, LOW);
      digitalWrite(lane1_yellow, HIGH);
      delay(1500);
      digitalWrite(lane1_yellow, LOW);
      
      // 2. Set Lane 1 to Red
      digitalWrite(lane1_red, HIGH);

      // 3. Set Lane 2 to Green
      digitalWrite(lane2_red, LOW);
      digitalWrite(lane2_green, HIGH);
    }
  }
}

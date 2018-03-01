

#include <Keypad.h>


//const String KEY = "1234";
int numPasswords = 10;
int len;
int pirState = LOW;
const int boton = 11;

const int redLed = 14;
const int redPin= 13;
const int greenPin = 12;
const int bluePin = 10;
const int pirSens = 2;


unsigned long t1;
unsigned long t2;
boolean first;
boolean first1;

String keys[10] = {"1234"};
const byte ROWS = 4; 
const byte COLS = 3;
const byte maxAttempts = 3;
char hexaKeys[ROWS][COLS] = {
  {
    '1', '2', '3'
  }
  ,
  {
    '4', '5', '6'
  }
  ,
  {
    '7', '8', '9'
  }
  ,
  {
    '*', '0', '#'
  }
};

byte rowPins[ROWS] = {9, 8, 7, 6}; 
byte colPins[COLS] = {5, 4, 3};
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

String currentKey;
boolean doorOpen;
byte attempts;
boolean block;

void setup() {
  Serial.begin(9600);
  currentKey = "";
  doorOpen = false;
  attempts = 0;
  block = false;
  first = true;
  first1 = true;


  pinMode(redLed, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(pirSens , INPUT);

  pinMode(boton,INPUT);

  setColor(0,0,255);
}

void loop() {

  char customKey;
  if(digitalRead(boton)){
    setColor(0,255,0);
    doorOpen = true;
    if(first1){
      t1 = millis();
      first1 = false;
    }
    else{
      if(millis()-t1>5000){
        setColor(255,0,0);
        Serial.println("Door open more than 30s");
      }
    }
  }
  else{
    if(!first1&&doorOpen){
      first1 = true;
      setColor(0,0,255);
      doorOpen = false;
      Serial.println("Door closed");
    }
  }
  

  if(!block) {
    //Selected key parsed;
    customKey = customKeypad.getKey();
  }
  else {
    Serial.println("Number of attempts exceeded");
    setColor(255,0,0);
    delay(30000);
    setColor(0,0,255);
    currentKey = "";
    attempts = 0; 
    block=false;
  }

  //Verification of input and appended value
  if (customKey) {  
    currentKey+=String(customKey);
    Serial.print(currentKey);
    Serial.println("");
  }

  //If the current key contains '*' and door is open
  if(doorOpen && currentKey.endsWith("*")) {
    doorOpen = false;
    Serial.print("Door closed");
    Serial.println("");
    setColor(0,0,255);
    currentKey = "";
    first  = true;
  }
  //If the current key contains '#' reset attempt
  if(currentKey.endsWith("#")&&currentKey.length()<=keys[0].length()) {
    currentKey = "";
    Serial.print("Attempt deleted");
    Serial.println("");
  }

  //If current key matches the key length
  if (currentKey.length()== keys[0].length()) {
    if(currentKey == keys[0]) {
      digitalWrite(10,HIGH);
      doorOpen = true;
      Serial.print("Door opened!!");
      Serial.println("");
      if(currentKey.endsWith("*")){
          Serial.println("si");
      }
      else{
        Serial.println("no");
      }
      
      setColor(0,255,0);
      attempts = 0;

      if(first){
         t1 = millis();
         first = false;
      }
      else{
        
        if(millis()-t1>5000){
          setColor(255,0,0);
        }
      }
    }
    else {
      attempts++;
      currentKey = "";
      Serial.print("Number of attempts: "+String(attempts));
      Serial.println("");
      setColor(255,0,0);
      delay(1000);
      setColor(0,0,255);
    }
  }
//  else if(currentKey.length()> keys[0].length()){
////    Serial.println("Door opened!!" );
////    Serial.println("entra a long mayor");
//     if(doorOpen && currentKey.endsWith("*")) {
//        doorOpen = false;
//        Serial.println("ENTRO A CERRAR EN LONG");
//        setColor(0,0,255);
//        currentKey = "";
//        first  = true;
//     }
////    setColor(0,255,0);
//  }
  if(attempts>=maxAttempts) {
    block = true;
  }

  if (digitalRead(pirSens)) {            // check if the input is HIGH
    digitalWrite(redLed, HIGH);  // turn LED ON
    if (pirState == LOW) {
      // we have just turned on
      Serial.println("Motion detected!");
     
      // We only want to print on the output change, not state
      pirState = HIGH;
    }
  } 
  else {
    digitalWrite(redLed, LOW); // turn LED OFF
    if (pirState == HIGH){
      // we have just turned of
      Serial.println("Motion ended!");
      // We only want to print on the output change, not state
      pirState = LOW;
    }
  }
  delay(100);
}

void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(redPin, redValue);
  analogWrite(greenPin, greenValue);
  analogWrite(bluePin, blueValue);
}


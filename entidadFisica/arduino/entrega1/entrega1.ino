
#include <EEPROM.h>
#include <Keypad.h>

//const String KEY = "1234";
int numPasswords = 10;
int len;
int pirState = LOW;
const int boton = 11;

const int redLed = 22;  //movement
const int redLed2 = 24; //battery
const int redPin = 13;
const int greenPin = 12;
const int bluePin = 10;
const int pirSens = 2;
const int battery = A0; //reads Battery
const int buzzer = 26;

unsigned long t1;
unsigned long t2;

//vars healthcheck
unsigned long timeH;

boolean first;
boolean first1;
boolean printOpen;
boolean printOpen1;

String str;                             //String que lee por serial
String comandoActual[3] = {"", "", ""}; //Informacion actual de los comandos

const byte ROWS = 4;
const byte COLS = 3;
const byte maxAttempts = 3;
char hexaKeys[ROWS][COLS] = {
    {'1', '2', '3'},
    {'4', '5', '6'},
    {'7', '8', '9'},
    {'*', '0', '#'}};

byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {5, 4, 3};
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

String currentKey;
boolean doorOpen;
byte attempts;
boolean block;

void setup()
{
  Serial.begin(9600);
  deleteAllPasswords();
  currentKey = "";
  doorOpen = false;
  attempts = 0;
  block = false;
  first = true;
  first1 = true;
  printOpen = true;
  printOpen1 = true;
  str = "";

  // Healthcheck
  timeH = millis();

  pinMode(redLed, OUTPUT);
  pinMode(redLed2, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(pirSens, INPUT);
  pinMode(boton, INPUT);

  setColor(0, 0, 255);
}

void loop()
{
  int batter = analogRead(battery);
  float voltage = batter * (5.0 / 1023.0);
  char customKey;

  //healthcheck cada 30s
  //para probar
  if (millis() - timeH > 10000)
  //para entrega
  // if (millis() - timeH > 30000)
  {
    Serial.println("OK");
    timeH = millis();
  }

  if (digitalRead(boton))
  {
    setColor(0, 255, 0);
    doorOpen = true;
    if (first1)
    {
      t1 = millis();
      first1 = false;
    }
    else
    {
      if (millis() - t1 > 5000)
      {
        setColor(255, 0, 0);
        digitalWrite(buzzer, HIGH);
        delay(1000);
        if (printOpen)
        {
          Serial.println("Door open more than 30s");
          printOpen = false;
        }
      }
    }
  }
  else
  {
    printOpen = true;
    if (!first1 && doorOpen)
    {
      first1 = true;
      setColor(0, 0, 255);
      doorOpen = false;
      Serial.println("Door closed");
      digitalWrite(buzzer, LOW);
    }
  }

  if (!block)
  {
    //Selected key parsed;
    customKey = customKeypad.getKey();
  }
  else
  {
    Serial.println("Number of attempts exceeded");
    setColor(255, 0, 0);
    digitalWrite(buzzer, HIGH);
    delay(30000);
    setColor(0, 0, 255);
    digitalWrite(buzzer, LOW);
    currentKey = "";
    attempts = 0;
    block = false;
  }

  //Verification of input and appended value
  if (customKey)
  {
    currentKey += String(customKey);
    Serial.print(currentKey);
    Serial.println("");
  }

  //If the current key contains '*' and door is open
  if (doorOpen && currentKey.endsWith("*"))
  {
    doorOpen = false;
    Serial.print("Door closed");
    doorOpen = false;
    printOpen1 = true;
    Serial.println("");
    setColor(0, 0, 255);
    currentKey = "";
    first = true;
  }
  //If the current key contains '#' reset attempt
  if (currentKey.endsWith("#") && currentKey.length() <= 5)
  {
    currentKey = "";
    Serial.print("Attempt deleted");
    Serial.println("");
  }

  //If current key matches the key length

  if (currentKey.length() == 4)
  {
    if (compareKey(currentKey))
    {
      digitalWrite(10, HIGH);
      doorOpen = true;
      Serial.print("Door opened!!");

      if (currentKey.endsWith("*"))
      {
        Serial.println("si");
      }
      else
      {
        Serial.println("no");
      }

      setColor(0, 255, 0);
      attempts = 0;

      if (first)
      {
        t1 = millis();
        first = false;
      }
      else
      {

        if (millis() - t1 > 5000)
        {
          setColor(255, 0, 0);
          digitalWrite(buzzer, HIGH);
          delay(1000);
          //door opened for too long
          if (printOpen1)
          {
            Serial.println("Door open more than 30s");
            printOpen1 = false;
          }
        }
      }
    }
    else
    {
      attempts++;
      currentKey = "";
      Serial.print("Number of attempts: " + String(attempts));
      Serial.println("");
      setColor(255, 0, 0);
      digitalWrite(buzzer, HIGH);
      delay(1000);
      setColor(0, 0, 255);
      digitalWrite(buzzer, LOW);
    }
  }
  if (attempts >= maxAttempts)
  {
    block = true;
  }

  if (digitalRead(pirSens))
  {                             // check if the input is HIGH
    digitalWrite(redLed, HIGH); // turn LED ON
    digitalWrite(buzzer, HIGH);
    delay(1000);
    if (pirState == LOW)
    {
      // we have just turned on
      Serial.println("Motion detected!");

      // We only want to print on the output change, not state
      pirState = HIGH;
    }
  }
  else
  {
    digitalWrite(redLed, LOW); // turn LED OFF
    digitalWrite(buzzer, LOW);
    if (pirState == HIGH)
    {
      // we have just turned of
      Serial.println("Motion ended!");
      // We only want to print on the output change, not state
      pirState = LOW;
    }
  }

  //Battery
  if (voltage < 1.2)
  {
    digitalWrite(redLed2, HIGH);
    digitalWrite(buzzer, HIGH);
    delay(2000);
    Serial.println("Low Battery");
  }
  else
  {
    digitalWrite(redLed2, LOW);
    digitalWrite(buzzer, LOW);
  }

  if (Serial.available() > 0)
  {
    // read the incoming byte:
    str = Serial.readString();
    processCommand(str);

    if (comandoActual[0] == "CHANGE_PASS")
    {
      Serial.println("Change password");
      int temp_index = comandoActual[1].toInt();
      int temp_key = comandoActual[2].toInt();
      updatePassword(temp_key, temp_index);
    }
    else if (comandoActual[0] == "ADD_PASS")
    {
      Serial.println("Add password");
      int temp_index = comandoActual[1].toInt();
      int temp_key = comandoActual[2].toInt();
      addPassword(temp_key, temp_index);
    }
    else if (comandoActual[0] == "DEL_PASS")
    {
      Serial.println("Delete password");
      int temp_index = comandoActual[1].toInt();
      deletePassword(temp_index);
    }
    Serial.println(compareKey("5678"));
    Serial.println(compareKey("1234"));
    Serial.println(compareKey("0000"));
    Serial.println(compareKey("1111"));
  }

  delay(100);
}

void setColor(int redValue, int greenValue, int blueValue)
{
  analogWrite(redPin, redValue);
  analogWrite(greenPin, greenValue);
  analogWrite(bluePin, blueValue);
}

// Method that compares a key with stored keys
boolean compareKey(String key)
{
  int acc = 3;
  int codif, arg0, arg1;
  for (int i = 0; i < 20; i++)
  {

    codif = EEPROM.read(i);
    while (codif != 0)
    {
      if (codif % 2 == 1)
      {
        arg0 = EEPROM.read(acc);
        arg1 = EEPROM.read(acc + 1) * 256;
        arg1 += arg0;
        if (String(arg1) == key)
        {
          return true;
        }
      }
      acc += 2;
      codif >>= 1;
    }
    acc = (i + 1) * 16 + 3;
  }
  return false;
}

// Methods that divides the command by parameters
void processCommand(String command)
{
  char temp[command.length()];
  command.toCharArray(temp, command.length());
  char *p;
  int i = 0;
  p = strtok(temp, ";");
  while (p != NULL)
  {
    comandoActual[i++] = p;
    p = strtok(NULL, ";");
  }
}

//Method that adds a password in the specified index
void addPassword(int val, int index)
{
  byte arg0 = val % 256;
  byte arg1 = val / 256;
  EEPROM.write((index * 2) + 3, arg0);
  EEPROM.write((index * 2) + 4, arg1);
  byte i = 1;
  byte location = index / 8;
  byte position = index % 8;
  i <<= position;
  byte j = EEPROM.read(location);
  j |= i;
  EEPROM.write(location, j);
}

//Method that updates a password in the specified index
void updatePassword(int val, int index)
{
  byte arg0 = val % 256;
  byte arg1 = val / 256;
  EEPROM.write((index * 2) + 3, arg0);
  EEPROM.write((index * 2) + 4, arg1);
}

//Method that deletes a password in the specified index
void deletePassword(int index)
{
  byte i = 1;
  byte location = index / 8;
  byte position = index % 8;
  i <<= position;
  byte j = EEPROM.read(location);
  j ^= i;
  EEPROM.write(location, j);
}

//Method that deletes all passwords
void deleteAllPasswords()
{
  //Password reference to inactive
  for (int i = 0; i < 20; i++)
  {
    EEPROM.write(i, 0);
  }
}

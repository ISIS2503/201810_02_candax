#include <EEPROM.h>
//#include <string.h>



int incomingByte1 = 0; 
int incomingByte2 = 0; 

String str1 = "";

String comandoActual[3]={"","",""};

void setup()
{
  Serial.begin(9600);
  deleteAllPasswords();
//  addPassword(1234, 0);
//  addPassword(2222, 1);    
}

void loop()
{
//  Serial.println(compareKey("1234"));
//  Serial.println(compareKey("2222"));
//  Serial.println(compareKey("1123"));
//  Serial.println("----");
// send data only when you receive data:

  if (Serial.available() > 0 ) {
          // read the incoming byte:
          str1 = Serial.readString();
          processCommand(str1);

          if(comandoActual[0] == "CHANGE_PASS"){
            Serial.println("Change password");
            int temp_index = comandoActual[1].toInt();
            int temp_key = comandoActual[2].toInt();
            updatePassword(temp_key,temp_index);
          }
          else if(comandoActual[0] == "ADD_PASS"){
            Serial.println("Add password");
            int temp_index = comandoActual[1].toInt();
            int temp_key = comandoActual[2].toInt();
            addPassword(temp_key,temp_index);
          }
          else if(comandoActual[0] == "DEL_PASS"){
            Serial.println("Delete password");
            int temp_index = comandoActual[1].toInt();
            deletePassword(temp_index);
          }

          Serial.println(compareKey("5678"));
          Serial.println(compareKey("1234"));
          Serial.println(compareKey("0000"));
          Serial.println(compareKey("1111"));
//          Serial.println(comandoActual[1]);
//          Serial.println(comandoActual[2]);
          
//          incomingByte2 = Serial.read();
//          incomingByte1 /= 256;
//          incomingByte1 += incomingByte2%256;

          // say what you got:
          
  }

}

// Method that compares a key with stored keys
boolean compareKey(String key) {
  int acc = 3;
  int codif, arg0, arg1; 
  for(int i=0; i<20; i++) {
    
    codif = EEPROM.read(i);
    while(codif!=0) {
      if(codif%2==1) {
        arg0 = EEPROM.read(acc);
        arg1 = EEPROM.read(acc+1)*256;
        arg1+= arg0;
        if(String(arg1)==key) {
          return true;
        }
      }
      acc+=2;
      codif>>=1;
    }
    acc=(i+1)*16+3;
    
  }
  return false;
}

// Methods that divides the command by parameters
void processCommand(String command) {
  char temp[command.length()];
  command.toCharArray(temp, command.length());
  char* p;
  int i = 0;
  p = strtok(temp,";");
  while(p != NULL){
    comandoActual[i++] = p;
    p = strtok(NULL,";");
  }
}

//Method that adds a password in the specified index
void addPassword(int val, int index) {
  byte arg0 = val%256;
  byte arg1 = val/256;
  EEPROM.write((index*2)+3,arg0);
  EEPROM.write((index*2)+4,arg1);
  byte i = 1;
  byte location = index/8;
  byte position = index%8;
  i<<=position;
  byte j = EEPROM.read(location);
  j |= i;
  EEPROM.write(location,j);
}

//Method that updates a password in the specified index
void updatePassword(int val, int index) {
  byte arg0 = val%256;
  byte arg1 = val/256;
  EEPROM.write((index*2)+3,arg0);
  EEPROM.write((index*2)+4,arg1);
}

//Method that deletes a password in the specified index
void deletePassword(int index) {
  byte i = 1;
  byte location = index/8;
  byte position = index%8;
  i<<=position;
  byte j = EEPROM.read(location);
  j ^= i;
  EEPROM.write(location,j);
}

//Method that deletes all passwords
void deleteAllPasswords() {
  //Password reference to inactive
  for( int i = 0 ; i<20 ; i++){
    EEPROM.write(i,0);
  }
}

#include <PubSubClient_1.h>
#include <ESP8266WiFi.h>

//DEFINES
#define TOPIC_SUBSCRIBE        "yale.uniandes.ml337.key"
#define TOPIC_PUBLISH          "alarms.res1.house1"
#define SIZE_BUFFER_DATA       150

//VARIABLES
String   idDevice = "ISIS2503";
boolean  stringComplete = false;
String   inputString = "";
char     bufferData [SIZE_BUFFER_DATA];

// CLIENTE WIFI & MQTT
WiFiClient       clientWIFI;
PubSubClient     clientMQTT(clientWIFI);

// CONFIG WIFI
const char* ssid = "isis2503";
const char* password = "Yale2018.";

// CONFIG MQTT
// CONFIG MQTT
unsigned char m2mqtt_ca_bin_crt[] = {
  0x30, 0x82, 0x03, 0xfb, 0x30, 0x82, 0x02, 0xe3, 0xa0, 0x03, 0x02, 0x01,
  0x02, 0x02, 0x09, 0x00, 0xc4, 0x6c, 0x11, 0xc4, 0x9d, 0x18, 0x2c, 0xcb,
  0x30, 0x0d, 0x06, 0x09, 0x2a, 0x86, 0x48, 0x86, 0xf7, 0x0d, 0x01, 0x01,
  0x0b, 0x05, 0x00, 0x30, 0x81, 0x93, 0x31, 0x0b, 0x30, 0x09, 0x06, 0x03,
  0x55, 0x04, 0x06, 0x13, 0x02, 0x43, 0x4f, 0x31, 0x0f, 0x30, 0x0d, 0x06,
  0x03, 0x55, 0x04, 0x08, 0x0c, 0x06, 0x42, 0x6f, 0x67, 0x6f, 0x74, 0x61,
  0x31, 0x0f, 0x30, 0x0d, 0x06, 0x03, 0x55, 0x04, 0x07, 0x0c, 0x06, 0x42,
  0x6f, 0x67, 0x6f, 0x74, 0x61, 0x31, 0x11, 0x30, 0x0f, 0x06, 0x03, 0x55,
  0x04, 0x0a, 0x0c, 0x08, 0x55, 0x6e, 0x69, 0x61, 0x6e, 0x64, 0x65, 0x73,
  0x31, 0x0f, 0x30, 0x0d, 0x06, 0x03, 0x55, 0x04, 0x0b, 0x0c, 0x06, 0x43,
  0x61, 0x6e, 0x64, 0x61, 0x78, 0x31, 0x12, 0x30, 0x10, 0x06, 0x03, 0x55,
  0x04, 0x03, 0x0c, 0x09, 0x41, 0x72, 0x71, 0x75, 0x69, 0x73, 0x6f, 0x66,
  0x74, 0x31, 0x2a, 0x30, 0x28, 0x06, 0x09, 0x2a, 0x86, 0x48, 0x86, 0xf7,
  0x0d, 0x01, 0x09, 0x01, 0x16, 0x1b, 0x65, 0x73, 0x74, 0x75, 0x64, 0x69,
  0x61, 0x6e, 0x74, 0x65, 0x73, 0x40, 0x75, 0x6e, 0x69, 0x61, 0x6e, 0x64,
  0x65, 0x73, 0x2e, 0x65, 0x64, 0x75, 0x2e, 0x63, 0x6f, 0x30, 0x1e, 0x17,
  0x0d, 0x31, 0x38, 0x30, 0x35, 0x30, 0x35, 0x30, 0x35, 0x33, 0x36, 0x35,
  0x32, 0x5a, 0x17, 0x0d, 0x32, 0x38, 0x30, 0x35, 0x30, 0x32, 0x30, 0x35,
  0x33, 0x36, 0x35, 0x32, 0x5a, 0x30, 0x81, 0x93, 0x31, 0x0b, 0x30, 0x09,
  0x06, 0x03, 0x55, 0x04, 0x06, 0x13, 0x02, 0x43, 0x4f, 0x31, 0x0f, 0x30,
  0x0d, 0x06, 0x03, 0x55, 0x04, 0x08, 0x0c, 0x06, 0x42, 0x6f, 0x67, 0x6f,
  0x74, 0x61, 0x31, 0x0f, 0x30, 0x0d, 0x06, 0x03, 0x55, 0x04, 0x07, 0x0c,
  0x06, 0x42, 0x6f, 0x67, 0x6f, 0x74, 0x61, 0x31, 0x11, 0x30, 0x0f, 0x06,
  0x03, 0x55, 0x04, 0x0a, 0x0c, 0x08, 0x55, 0x6e, 0x69, 0x61, 0x6e, 0x64,
  0x65, 0x73, 0x31, 0x0f, 0x30, 0x0d, 0x06, 0x03, 0x55, 0x04, 0x0b, 0x0c,
  0x06, 0x43, 0x61, 0x6e, 0x64, 0x61, 0x78, 0x31, 0x12, 0x30, 0x10, 0x06,
  0x03, 0x55, 0x04, 0x03, 0x0c, 0x09, 0x41, 0x72, 0x71, 0x75, 0x69, 0x73,
  0x6f, 0x66, 0x74, 0x31, 0x2a, 0x30, 0x28, 0x06, 0x09, 0x2a, 0x86, 0x48,
  0x86, 0xf7, 0x0d, 0x01, 0x09, 0x01, 0x16, 0x1b, 0x65, 0x73, 0x74, 0x75,
  0x64, 0x69, 0x61, 0x6e, 0x74, 0x65, 0x73, 0x40, 0x75, 0x6e, 0x69, 0x61,
  0x6e, 0x64, 0x65, 0x73, 0x2e, 0x65, 0x64, 0x75, 0x2e, 0x63, 0x6f, 0x30,
  0x82, 0x01, 0x22, 0x30, 0x0d, 0x06, 0x09, 0x2a, 0x86, 0x48, 0x86, 0xf7,
  0x0d, 0x01, 0x01, 0x01, 0x05, 0x00, 0x03, 0x82, 0x01, 0x0f, 0x00, 0x30,
  0x82, 0x01, 0x0a, 0x02, 0x82, 0x01, 0x01, 0x00, 0xe0, 0x32, 0xa3, 0xb3,
  0xfc, 0x27, 0x4e, 0x85, 0x79, 0x35, 0xc3, 0xfb, 0x36, 0x8f, 0x3c, 0xca,
  0x17, 0xb8, 0x0c, 0x7d, 0xf0, 0xc0, 0x80, 0xb1, 0xa4, 0x50, 0x73, 0x26,
  0x81, 0xd4, 0x4c, 0x25, 0xfc, 0x2c, 0x65, 0x0d, 0x89, 0xfd, 0xad, 0x94,
  0xf7, 0xf9, 0x9a, 0xe9, 0xbd, 0xd8, 0x28, 0x9e, 0xa8, 0xcf, 0xda, 0x6b,
  0x40, 0xf4, 0x50, 0x6f, 0xb1, 0x41, 0x36, 0xbb, 0xe6, 0x4c, 0x91, 0x3e,
  0x28, 0xb9, 0xdc, 0x64, 0x23, 0x1e, 0xdd, 0xd9, 0x5f, 0x09, 0x30, 0x3d,
  0xa9, 0xcf, 0xb9, 0xeb, 0x07, 0x32, 0xfd, 0xb9, 0x8d, 0x6c, 0xc9, 0xed,
  0x4c, 0xef, 0x13, 0x72, 0x21, 0x5a, 0xcf, 0x00, 0xb7, 0xb4, 0x05, 0x7a,
  0xbf, 0xa5, 0xe7, 0x07, 0x6c, 0x88, 0x37, 0xb9, 0x24, 0x87, 0xb1, 0x23,
  0xf3, 0x78, 0x8e, 0xcb, 0x6d, 0xa1, 0x01, 0xff, 0x6d, 0x82, 0x9b, 0xd0,
  0xf1, 0xd0, 0x17, 0x0b, 0x22, 0xf1, 0xa8, 0x03, 0xea, 0x7d, 0xdf, 0x88,
  0x18, 0xb7, 0x3b, 0x53, 0x4c, 0xf3, 0xfe, 0x38, 0x66, 0xad, 0xd8, 0x17,
  0x11, 0x0d, 0xbc, 0xad, 0x55, 0x47, 0x22, 0xc3, 0x64, 0xad, 0x20, 0x31,
  0xb5, 0x95, 0x89, 0x2d, 0xc9, 0xef, 0xbe, 0xa9, 0x37, 0xc4, 0x49, 0x67,
  0xde, 0xc9, 0x46, 0xc6, 0x40, 0x6a, 0x4b, 0x1a, 0x16, 0xa7, 0xf7, 0x3d,
  0xf0, 0x53, 0x02, 0xa8, 0xd6, 0xd7, 0xe9, 0xa7, 0xa9, 0xe6, 0x2b, 0x70,
  0x13, 0xe4, 0xb9, 0x08, 0x6e, 0xfe, 0x4e, 0x5c, 0xf3, 0x52, 0xfe, 0x01,
  0xc1, 0x8a, 0x7c, 0xb6, 0x87, 0x82, 0x6b, 0x49, 0xf3, 0x6d, 0x5e, 0x58,
  0x6d, 0x10, 0xab, 0xf0, 0x93, 0xfe, 0xa1, 0xe7, 0xf1, 0x41, 0xd6, 0x34,
  0x8d, 0x1e, 0x93, 0xe7, 0x02, 0x89, 0x69, 0xd2, 0x14, 0x49, 0xb6, 0x20,
  0xcb, 0x07, 0x9c, 0x11, 0xdf, 0x03, 0xfc, 0x3d, 0x30, 0xb1, 0x3e, 0xe1,
  0x02, 0x03, 0x01, 0x00, 0x01, 0xa3, 0x50, 0x30, 0x4e, 0x30, 0x1d, 0x06,
  0x03, 0x55, 0x1d, 0x0e, 0x04, 0x16, 0x04, 0x14, 0x09, 0xdf, 0x71, 0xea,
  0x68, 0xfe, 0xd2, 0xf3, 0x26, 0xab, 0xff, 0x1f, 0x97, 0xde, 0xf4, 0x87,
  0x31, 0x5a, 0x4d, 0x52, 0x30, 0x1f, 0x06, 0x03, 0x55, 0x1d, 0x23, 0x04,
  0x18, 0x30, 0x16, 0x80, 0x14, 0x09, 0xdf, 0x71, 0xea, 0x68, 0xfe, 0xd2,
  0xf3, 0x26, 0xab, 0xff, 0x1f, 0x97, 0xde, 0xf4, 0x87, 0x31, 0x5a, 0x4d,
  0x52, 0x30, 0x0c, 0x06, 0x03, 0x55, 0x1d, 0x13, 0x04, 0x05, 0x30, 0x03,
  0x01, 0x01, 0xff, 0x30, 0x0d, 0x06, 0x09, 0x2a, 0x86, 0x48, 0x86, 0xf7,
  0x0d, 0x01, 0x01, 0x0b, 0x05, 0x00, 0x03, 0x82, 0x01, 0x01, 0x00, 0xbe,
  0x53, 0x45, 0xe1, 0x08, 0x82, 0x99, 0x76, 0x42, 0xa0, 0xda, 0xd2, 0xd5,
  0xd6, 0x20, 0x69, 0xc5, 0xfa, 0xbf, 0xe1, 0x18, 0xb0, 0xda, 0x82, 0xab,
  0xe6, 0x5a, 0x0d, 0xcb, 0x36, 0x63, 0x38, 0x7a, 0xc0, 0x56, 0x03, 0xc1,
  0x89, 0x75, 0x8a, 0x18, 0x0b, 0xba, 0x4c, 0xf8, 0xa5, 0x5b, 0x41, 0x99,
  0x2a, 0x0a, 0xad, 0x1e, 0xcc, 0x8f, 0x6d, 0x0f, 0x1a, 0xeb, 0xc6, 0xdd,
  0x2e, 0x18, 0x0e, 0x7c, 0x5e, 0x89, 0x23, 0x20, 0xba, 0x71, 0xf0, 0x9b,
  0x05, 0xb2, 0x7b, 0x6c, 0xac, 0x12, 0xb8, 0x92, 0x70, 0xde, 0x35, 0xf6,
  0xf9, 0x0e, 0x2e, 0x1e, 0x98, 0x40, 0xd6, 0xb6, 0x7c, 0x8d, 0x35, 0x05,
  0x55, 0x1d, 0xaf, 0x3c, 0x58, 0xfa, 0xe5, 0xb0, 0x59, 0x5f, 0xb5, 0xb3,
  0xe9, 0x44, 0x0c, 0x88, 0x02, 0xec, 0x4e, 0xf8, 0xc7, 0x3a, 0x97, 0x90,
  0x8f, 0x2f, 0x6b, 0xb0, 0x7b, 0x92, 0xa4, 0x0b, 0x4d, 0xbd, 0x8a, 0xd3,
  0x87, 0xff, 0xbf, 0x3f, 0xe3, 0x86, 0x09, 0x6c, 0x2a, 0xda, 0x63, 0x39,
  0xf7, 0xc6, 0x10, 0x3c, 0xa5, 0x57, 0x2e, 0x1b, 0x9d, 0xcf, 0x47, 0xa2,
  0xde, 0x6f, 0xe7, 0x79, 0x18, 0x99, 0x5d, 0x5e, 0x63, 0x5e, 0xb8, 0xbb,
  0x9e, 0x46, 0xfd, 0x43, 0x81, 0x05, 0xcb, 0x01, 0xf9, 0x3b, 0xfa, 0x36,
  0xff, 0xb6, 0xe2, 0xcd, 0x22, 0x12, 0xc9, 0xcc, 0xec, 0xf7, 0x58, 0x55,
  0xa6, 0x1d, 0xce, 0x50, 0x05, 0xa3, 0x40, 0x39, 0xf4, 0x04, 0xbe, 0x31,
  0x34, 0x55, 0x48, 0x63, 0x30, 0xd2, 0xfe, 0x52, 0x83, 0x48, 0x06, 0x6d,
  0xa7, 0xab, 0x68, 0x0c, 0xed, 0x54, 0xde, 0xc5, 0x66, 0x8d, 0x95, 0xc7,
  0x60, 0x34, 0xdb, 0x4a, 0x1f, 0xfe, 0x33, 0xf8, 0xf1, 0xe2, 0xb7, 0xca,
  0x19, 0xe3, 0xe8, 0xbb, 0xae, 0x38, 0xa8, 0x66, 0x6c, 0xda, 0xf5, 0x06,
  0x7e, 0xfd, 0xc6
};

unsigned int m2mqtt_ca_bin_crt_len = 1023;

IPAddress serverMQTT (172,24,41,153);
const uint16_t portMQTT = 8083;
const char* usernameMQTT = "microcontrolador";
const char* passwordMQTT = "Isis2503";

// FUNCTIONS
String macToStr(const uint8_t* mac) {
  String result;
  for (int i = 0; i < 6; ++i) {
    result += String(mac[i], 16);
    if (i < 5)
      result += ':';
  }
  return result;
}

void connectWIFI() {
  // Conectar a la red WiFi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  if(WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
  }

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // Obtain MAC Address
  uint8_t mac[6];
  WiFi.macAddress(mac);
  idDevice = macToStr(mac);
  Serial.print("MAC Address: ");
  Serial.println(idDevice);

  // Obtain IP Address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void reconnectWIFI() {
  // Conectar a la red WiFi
  if(WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
  }

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

boolean connectMQTT() {
  boolean connectMQTT = false;
  if (!clientMQTT.connected()) {
    if (clientMQTT.connect(idDevice.c_str(), usernameMQTT, passwordMQTT)) {
      connectMQTT = true;
    }
  }
  else {
    connectMQTT = true;
  }

  if(connectMQTT) {
    if(clientMQTT.subscribe(TOPIC_SUBSCRIBE)) {
      // Serial.println("Subscribe OK");
    }
  }
  return connectMQTT;
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.write(payload, length);
  Serial.println();
}

void setup() {
  Serial.begin(9600);
  inputString.reserve(150);
  // clientWIFI.setCACert(m2mqtt_ca_bin_crt, m2mqtt_ca_bin_crt_len);

  clientMQTT.setServer(serverMQTT, portMQTT);
  clientMQTT.setCallback(callback);
  connectWIFI();
  delay(1000);
  if (connectMQTT()) {
    Serial.println("MQTT connected!!!");
  }
  delay(1000);
}

void processData() {
  if (stringComplete) {
    if (WiFi.status() != WL_CONNECTED) {
      reconnectWIFI();
    }

    if (WiFi.status() == WL_CONNECTED) {
      if (!clientMQTT.connected()) {
        connectMQTT();
      }

      if (clientMQTT.connected()) {
        if(clientMQTT.publish(TOPIC_PUBLISH, bufferData)) {
          inputString = "";
          stringComplete = false;
        }
      }
    }
  }
  clientMQTT.loop();
}

void receiveData() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;

    if (inChar == '\n') {
      inputString.toCharArray(bufferData, SIZE_BUFFER_DATA);
      stringComplete = true;
    }
  }
}

void loop() {
  receiveData();
  processData();
}

#include <Wire.h>
#include <SoftwareSerial.h>
#include <HardwareSerial.h>
#include <Adafruit_BMP280.h>
#include <MPU6050_light.h>
#include <TinyGPS++.h>
#include <ArduinoJson.h>
#include <SD.h>

Adafruit_BMP280 bmp;
MPU6050 mpu(Wire);
TinyGPSPlus gps;

#define MPU_ADDR 0x68
#define BMP_SCK 13
#define BMP_MISO 12
#define BMP_MOSI 11
#define BMP_CS 10

#define SD_SPI_CS 5
#define FILE_NAME "Team-Astropeep-Data.txt"

#define GPS_RX_PIN 16
#define GPS_TX_PIN 17

HardwareSerial xbeeSerial(1);
HardwareSerial gpsSerial(2);


DynamicJsonDocument jsonDoc(512);

String TelemetryPackage;
int PacketCount;
int Count;
const String Team_Id = "2022ASI-002";
String FSW_State = "";
String TimeStamp;
String GpsTime;
float Pressure, Temperature, Altitude, Voltage, GpsLatitude, GpsLongitude, GpsAltitude, GpsSats;
float a_x, a_y, a_z, gyro_x, gyro_y, gyro_z, AngleX, AngleY, AngleZ;
File myFile;



void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600, SERIAL_8N1, 1, 3);
  xbeeSerial.begin(9600, SERIAL_8N1, 16, 17);
  Wire.begin();
  mpu.begin();
  mpu.calcOffsets(true, true);
  Wire.write(0);
  Wire.endTransmission(true);
  if (!bmp.begin(0x76)) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
  }
}


void loop() {

  Pressure = getPressure();
  Temperature = getTemperature();
  Altitude = getAltitude();
  Temperature = mpu.getTemp();
  gyro_x = mpu.getGyroX();
  gyro_y = mpu.getGyroY();
  gyro_z = mpu.getGyroZ();
  a_x = mpu.getAccX();
  a_y = mpu.getAccY();
  a_z = mpu.getAccZ();
  AngleX = mpu.getAngleX();
  AngleY = mpu.getAngleY();
  AngleZ = mpu.getAngleZ();
  Voltage = getVolt();
  GpsLatitude = getGPSlat();
  GpsLongitude = getGPSlon();
  GpsAltitude = getGPSalti();
  GpsSats = getGPSsats();
  Voltage = getVolt();
  TimeStamp = GpsTime;

  mpu.update();

  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }
  
  if (gps.date.isValid() && gps.time.isValid()) {
    GpsTime = String(gps.time.hour()) + ":" + String(gps.time.minute()) + ":" + String(gps.time.second());
  }

  float ref_height = 213.46;
  float ref_alt = GpsAltitude - ref_height;

  if (Altitude == ref_alt && Count == 0){
    FSW_State = "Ground";
  }

  else if (Altitude > 100 && Count == 0){
    Count++;
  }

  else if (Altitude < 500 && Altitude > 100 && Count == 1){
    FSW_State = "Descent";
  }

  else if (Altitude < 100 && Count == 1){
    FSW_State = "Landing";
  }

  else {
    FSW_State = "Ascent";
  }

  jsonDoc["Team_Id"] = Team_Id;
  jsonDoc["TimeStamp"] = TimeStamp;
  jsonDoc["PacketCount"] = PacketCount;
  jsonDoc["Altitude"] = Altitude;
  jsonDoc["Pressure"] = Pressure;
  jsonDoc["Temperature"] = Temperature;
  jsonDoc["Voltage"] = Voltage;
  jsonDoc["GpsTime"] = GpsTime;
  jsonDoc["GpsLatitude"] = GpsLatitude;
  jsonDoc["GpsLongitude"] = GpsLongitude;
  jsonDoc["GpsAltitude"] = GpsAltitude;
  jsonDoc["GpsSats"] = GpsSats;
  jsonDoc["a_x"] = a_x;
  jsonDoc["a_y"] = a_y;
  jsonDoc["a_z"] = a_z;
  jsonDoc["gyro_x"] = gyro_x;
  jsonDoc["gyro_y"] = gyro_y;
  jsonDoc["gyro_z"] = gyro_z;
  jsonDoc["FSW_State"] = FSW_State;
  jsonDoc["AngleX"] = AngleX;
  jsonDoc["AngleY"] = AngleY;
  jsonDoc["AngleZ"] = AngleZ;
  

  String jsonData;
  serializeJson(jsonDoc, jsonData);
  const char* dataPacket = jsonData.c_str();
  sendPacket(dataPacket);
  jsonDoc.clear();

  myFile = SD.open(FILE_NAME, FILE_WRITE);
  if (myFile) {
    myFile.print(dataPacket);
    myFile.println();
    myFile.close();
  } else {
    Serial.print(F("SD Card: Issue encountered while attempting to open the file "));
    Serial.println(FILE_NAME);
  }
  
  // Serial.println(dataPacket);

  delay(10);

  PacketCount++;

}



float getPressure() {
  float pressure = bmp.readPressure();
  return pressure;
}

float getTemperature() {
  float temp = bmp.readTemperature();
  return temp;
}

float getAltitude() {
  float alti = bmp.readAltitude(1005);
  return alti;
}

float getVolt() {
  int offset = 20;
  int volt = analogRead(12);
  double voltage = map(volt, 0, 1023, 0, 2500) + offset;
  voltage /= 100;
  return voltage;
}

float getGPSlat() {
  float lat = 0;
  if (gps.location.isValid()) {
    lat = gps.location.lat();
  }
  return lat;
}

float getGPSlon() {
  float lon = 0;
  if (gps.location.isValid()) {
    lon = gps.location.lng();
  }
  return lon;
}

float getGPSalti() {
  float alti = 0;
  if (gps.location.isValid()) {
    alti = gps.altitude.meters();
  }
  return alti;
}

int getGPSsats() {
  int sats = 0;
  if (gps.satellites.isValid()) {
    sats = gps.satellites.value();
  }
  return sats;
}



void sendPacket(const char* data) {

  byte startDelimiter = 0x7E;

  byte frameType = 0x10;
  byte frameID = 0x01;

  byte destAddr[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF};
  byte destAddr16[] = {0xFF, 0xFE};

  byte options = 0x00;

  byte radius = 0x00;

  char dataCopy[strlen(data) + 1];
  strcpy(dataCopy, data);

  char* token = strtok(dataCopy, ",");
  while (token != NULL) {
    byte* dataBytes = (byte*)token;
    size_t dataLength = strlen(token);

    uint16_t packetLength = 14 + dataLength;

    uint8_t checksum = 0xFF - ((frameType + frameID + destAddr[0] + destAddr[1] + destAddr[2] +
                               destAddr[3] + destAddr[4] + destAddr[5] + destAddr[6] + destAddr[7] +
                               destAddr16[0] + destAddr16[1] + options + radius +
                               sum(dataBytes, dataLength)) & 0xFF);


    xbeeSerial.write(startDelimiter);
    xbeeSerial.write(packetLength >> 8);
    xbeeSerial.write(packetLength & 0xFF);
    xbeeSerial.write(frameType);
    xbeeSerial.write(frameID);
    xbeeSerial.write(destAddr, sizeof(destAddr));
    xbeeSerial.write(destAddr16, sizeof(destAddr16));
    xbeeSerial.write(options);
    xbeeSerial.write(radius);
    xbeeSerial.write(dataBytes, dataLength);
    xbeeSerial.write(checksum);

    delay(10);

    token = strtok(NULL, ",");
  }
}


uint8_t sum(const byte* data, size_t length) {
  uint8_t sum = 0;
  for (size_t i = 0; i < length; i++) {
    sum += data[i];
  }
  return sum;
}

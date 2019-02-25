#include <Arduino.h>

#include <EEPROM.h>

#include <SPI.h>
#include <RH_RF95.h>

#include <Wire.h>

#include <SoftwareSerial.h>

// ===== RFM95 =====
// frequency
#define RF95_FREQ 915.0
// pins
#define RFM95_CS 4
#define RFM95_RST 2
#define RFM95_INT 3
// singleton instance of the radio driver
RH_RF95 rf95 (RFM95_CS, RFM95_INT);

#define MESSAGE_LENGTH 19

#define LOCATION_ID 1736

// already included #include <Wire.h> // must be included here so that Arduino library object file references work
// SWITCH TO DS1307 STUFF!
#include <RtcDS1307.h>
RtcDS1307<TwoWire> Rtc(Wire);

// start addresses at 2, as addresses 0 and 1 are reserved for the device's
// id (stored in base64)
int startAddr = 2;
int addr = 2;
int sendAddr = 2;

void setup() {
	// ===== Transciever Setup =====
	pinMode(RFM95_RST, OUTPUT);
	digitalWrite(RFM95_RST, HIGH);

	Serial.begin(9600);

	while(!Serial) {
		delay(1);
	}

	delay(100);

	// digital reset of transciever
	digitalWrite(RFM95_RST, LOW);
	delay(10);
	digitalWrite(RFM95_RST, HIGH);
	delay(10);

	// initialize transciever
	while( !rf95.init() ) {}

	// set frequency
	if ( !rf95.setFrequency(RF95_FREQ) ) {
		while(1);
	}
	// set transmission power -- max!
	rf95.setTxPower(23, false);
}

int count = 0;

void loop() {

	delay(10000);

    char sendMsg[19] = "ABBCDFJPVi3BZCQDp"; // Fibonacci seq. for fun (to 233)
    sendMsg[18] = 0; // null terminator

	// Send the message!
	rf95.send((uint8_t *)sendMsg, MESSAGE_LENGTH);
	delay(10);
	rf95.waitPacketSent();

    // ===== RECIEVE =====
	// listen for other packets
	if( rf95.available() ) {
		uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
   		uint8_t len = sizeof(buf);

		if( rf95.recv(buf, &len) ) {
			Serial.print(F("REC:"));
      		Serial.println((char*)buf);
            Serial.println(rf95.lastRssi());
        }
	}

}

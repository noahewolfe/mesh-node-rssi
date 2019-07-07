#include <Arduino.h>

#include <EEPROM.h>

#include <SPI.h>
#include <RH_RF95.h>

#include <SoftwareSerial.h>
#include <Wire.h>

#include <LiquidCrystal.h>
#define LCD_LIGHT_PIN A3

LiquidCrystal lcd(14, 15, 9, 10, 5, 16);

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

void setup() {

    lcd.begin(16, 2);
    lcd.setCursor(0,0);

    lcd.print(F("Hello, world!"));

	// ===== Transciever Setup =====
	pinMode(RFM95_RST, OUTPUT);
	digitalWrite(RFM95_RST, HIGH);

	Serial.begin(9600);

	while(!Serial) {
		delay(1);
	}

	delay(100);

    pinMode(LCD_LIGHT_PIN, OUTPUT);
    digitalWrite(LCD_LIGHT_PIN, HIGH); // HIGH ONLY FOR TESTING -- SET TO LOW!

    lcd.clear();

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

    rf95.setSignalBandwidth(62500); // lowest
    rf95.setSpreadingFactor(12); // highest
    rf95.setCodingRate4(8); // highest.. denom. value

	// set transmission power -- max!
	rf95.setTxPower(23, false);
}

int counter = 0;
long start_time = 0.0;
long end_time = 0.0;

void loop() {

    // ===== RECIEVE =====
	// listen for other packets
	if( rf95.available() ) {
		uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
   		uint8_t len = sizeof(buf);

		if( rf95.recv(buf, &len) ) {
			Serial.print(F("REC:"));
      		Serial.println((char*)buf);
            Serial.println(rf95.lastRssi());
            lcd.print(rf95.lastRssi());
        }
	}

    lcd.clear();

    /*
    char sendMsg[17] = "ABBCDFJPVi3BZCQ";
    sendMsg[16] = 0; // null terminator
    */

    // ===== TRANSMIT =====
	// Send the message!
    char counter_msg[19];
    itoa(counter, counter_msg, 10);

    start_time = millis();
	rf95.send((uint8_t *)counter_msg, MESSAGE_LENGTH);
	delay(10);
	rf95.waitPacketSent();
    end_time = millis();

    lcd.setCursor(0,1);
    lcd.print(end_time - start_time);

    counter++;

    delay(60000); // send once a minute, b/c at high power, can only do
    // 1% duty cycle
    // will need to measure sending rate to better understand this

}

/**
 * @file main.ino
 * @author Hankyul Kwon (khk4502@gmail.com)
 * @brief This code is edited for control dummy car's LED and BLE.
 * @version 0.1
 * @date 2021-11-27
 * 
 * @copyright Copyright (c) 2021
 * 
 */

#include "BluetoothSerial.h"
#include "esp_bt_device.h"
#include <string.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

// Value setting
#define CHARGE_STEP             5      // charging step by 'TIMER_INTERRUPT_TERM'
#define TIMER_INTERRUPT_TERM    100    // milli seconds

// Pin setting
int PIN_WIRLESS_CHARGING = 13;      // Input pin of wireless charging signal
int PIN_CHARGE_LEVEL_LED[5] = { 12, 14, 27, 26, 25 };

BluetoothSerial SerialBT;

// Timer interrupt setting
volatile bool interruptCounter=false;
hw_timer_t * timer = NULL;

bool isCharging = false;
int chargeLevel = 0;
char serial_buf[100] = { 0, };

void sendPercentage() {
    int serial_buf_len = strlen(serial_buf);
    Serial.println(serial_buf);
    for (int i = 0; i < serial_buf_len; i++) {
        //while (!SerialBT.available()) continue;
        //SerialBT.read();
        SerialBT.write(serial_buf[i]);
    }
    SerialBT.write('\0');
    if (SerialBT.available()) {
        
    }
}

void IRAM_ATTR timerIntrptFunc() {
    Serial.println("Timer Interrupt Called");
    if (!isCharging) {
        isCharging = digitalRead(PIN_WIRLESS_CHARGING);
        if (chargeLevel > 0) chargeLevel -= CHARGE_STEP;
    } else {
        // Charging Complete: Negate 'isCharging' signal.
        Serial.println("Charge step");
        if (chargeLevel >= 100) {
            isCharging = false;
        } else {
            chargeLevel += CHARGE_STEP;
        }
    }
    if (chargeLevel >= 20 ) digitalWrite(PIN_CHARGE_LEVEL_LED[0], HIGH);
    else                    digitalWrite(PIN_CHARGE_LEVEL_LED[0], LOW);
    if (chargeLevel >= 40 ) digitalWrite(PIN_CHARGE_LEVEL_LED[1], HIGH);
    else                    digitalWrite(PIN_CHARGE_LEVEL_LED[1], LOW);
    if (chargeLevel >= 60 ) digitalWrite(PIN_CHARGE_LEVEL_LED[2], HIGH);
    else                    digitalWrite(PIN_CHARGE_LEVEL_LED[2], LOW);
    if (chargeLevel >= 80 ) digitalWrite(PIN_CHARGE_LEVEL_LED[3], HIGH);
    else                    digitalWrite(PIN_CHARGE_LEVEL_LED[3], LOW);
    if (chargeLevel >= 100) digitalWrite(PIN_CHARGE_LEVEL_LED[4], HIGH);
    else                    digitalWrite(PIN_CHARGE_LEVEL_LED[4], LOW);
    sprintf(serial_buf, "%d", chargeLevel);
    sendPercentage();
}

void printDeviceAddress() {
    const uint8_t *point = esp_bt_dev_get_address();

    for (int i = 0; i < 6; i++) {
        char str[3];

        sprintf(str, "%02X", (int)point[i]);
        Serial.print(str);

        if (i < 5) {
        Serial.print(":");
        }
    }
}

void interrupt_init(){              //timer interrupt freq is 80Mhz
    timer = timerBegin(0, 80, true);  //division 80=1Mhz
    timerAttachInterrupt(timer, &timerIntrptFunc, true);
    timerAlarmWrite(timer, 1000000, true);    //count 1000000 = 1sec,1000=1msec
    timerAlarmEnable(timer);
}

void setup() {
    Serial.begin(115200);
    SerialBT.begin("ElectricCarTest"); // Bluetooth device name
    Serial.println("Charging started...");
    Serial.println("Device Name: ElectricCar");
    Serial.print("BT MAC: ");
    printDeviceAddress();
    Serial.println();
    isCharging = false;

    pinMode(PIN_WIRLESS_CHARGING, INPUT);   // Wireless Charging Input signal
    for (int i = 0; i < 5; i++) {
        pinMode(PIN_CHARGE_LEVEL_LED[i], OUTPUT);
    }
    //attachInterrupt(digitalPinToInterrupt(PIN_WIRLESS_CHARGING), startBLE, RISING);
    SerialBT.connected(5000);

    // Setup Timer Interrupt Function
    interrupt_init();
}

void loop() {
    //Serial.println("Testing");
}

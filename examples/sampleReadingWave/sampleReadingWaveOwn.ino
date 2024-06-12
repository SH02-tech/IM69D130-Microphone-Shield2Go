#include <I2S.h>

/*
 * This example reads audio data from Infineon's IM69D130 Microphone Shield2Go 
 * and prints it on the serial monitor.
 * 
 * Open the serial monitor with baudrate of 1000000 to see the results.
 * 
 * Note: if 2 channels are used, the values returned from I2S.read() will be from both channels and thus look noisy
 * In this case, both values need to be separated.
 */

uint8_t status;

void setup() {
  Serial.begin(1000000);
  I2S.disableMicrophones();

  // Enable the microphone when word select is low
  status = I2S.enableMicrophoneLow();

  // Enable the microphone when word select is high
  // I2S.enableMicrophoneHigh();
  // Get the activated microphones
  // You can compare against NO_MICROPHONE, MICROPHONE_LOW, MICROPHONE_HIGH, MICROPHONE_LOW_HIGH
  // e.g. I2S.getMicrophones() == NO_MICROPHONE
  // I2S.getMicrophones();

  // Start I2S with I2S_PHILIPS_MODE, 12 kHz sampling rate and 20 bits per sample
  // Returns 0 if everything okay, otherwise value > 0
  I2S.begin(I2S_PHILIPS_MODE, 12000, 20);
}

void loop() {
  // I2S is very demanding in terms of data rate
  // Uncomment the line with I2S.getOverflow() to see whether the internal buffer has an overflow or not
  if (status == 1) {
    while (I2S.available() > 0) {
      // Read one value from the internal buffer and return it on the serial console
      int32_t value = I2S.read();

      Serial.println(value);

      // To measure sizes:
      // size_t size = Serial.println(value);
      // Serial.println("Value:");
      // Serial.println(size);

      // Serial.println(sizeof("\r"));
      // if(I2S.getOverflow() == true) Serial.println("Overflow");

      // if(I2S.getOverflow() == true){
      //   // Serial.println("Overflow");
      //   I2S.flush();
      // }
    }
  } else {
    Serial.println("Not good.");
  }

}

import numpy as np
import struct
import wave
from serial import Serial

DEVICE = "COM7"
BAUDRATE = 1000000
SAMPLE_RATE = 12000
NUM_INSTANTS = SAMPLE_RATE * 5 # 5 seconds

BATCH_SIZE = 28 # sent in blocks of 7 bytes (see original Arduino code)

NUM_CHANNELS = 1
SAMPLE_WIDTH = 4 # 32 bits -> 4 bytes
COMPRESSION_TYPE = "NONE"
COMPRESSION_NAME = "not compressed"

def get_sound(total_instants: int) -> np.array:
    sound_values = [] # converted to np.array right before return
    serial_instance = Serial(DEVICE, BAUDRATE)

    num_instants = 0

    while num_instants < total_instants:
        if serial_instance.in_waiting >= BATCH_SIZE:
            returned_value = serial_instance.read(BATCH_SIZE)
            returned_value = returned_value.split(b'\r')

            for bytes_value in returned_value:
                print(bytes_value)

                numeric_string = bytes_value.decode("utf-8").strip().lstrip('\r')

                if numeric_string.lstrip('-').isnumeric():
                    print(numeric_string)

                    value = int(numeric_string)
                    # value = int.from_bytes(bytes_value, byteorder='big', signed=True)
                    # converted_value = int(float((float(value)/524288)*(2147483647)))
                    
                    if -524288 < value and value < 524287:
                        value_ext = int(float((float(value)/524288)*(2147483647)))
                        # print(value_ext)
                        sound_values.append(value_ext)
                        num_instants += 1

    # Data processed. 

    print("Data processed.")
    print("Beginning of audio:", sound_values[:10])
    print("End of audio", sound_values[len(sound_values)-10:])

    return np.array(sound_values)

def main():
    sound_values = get_sound(NUM_INSTANTS)
    
    with wave.open("output.wav", 'wb') as wavfile:
        wavfile.setparams((NUM_CHANNELS, SAMPLE_WIDTH, SAMPLE_RATE, NUM_INSTANTS, COMPRESSION_TYPE, COMPRESSION_NAME))
        for value in sound_values:
            # print("value", value)
            data = struct.pack('i', value)
            wavfile.writeframes(data)

if __name__ == '__main__':
    main()
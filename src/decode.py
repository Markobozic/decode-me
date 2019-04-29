from scipy.io import wavfile
from goertzel import goertzel
import sys

SAMPLING_RATE = 48000
MARK_TARGET_FREQUENCY = 2225
SPACE_TARGET_FREQUENCY = 2025
SAMPLING_SIZE = 160


def split(l):
    temp = []
    final_list = []
    for item in l:
        temp.append(item)
        if len(temp) == 160:
            final_list.append(temp)
            temp = []

    return final_list


if __name__ == '__main__':
    fs, data = None, None
    try:
        if str(sys.argv[1]).endswith('.wav'):
            fs, data = wavfile.read(str(sys.argv[1]))
        else:
            raise Exception('The supplied file was not a valid WAVE file ending in .wav')
    except IOError:
        print IOError

    full_list_of_samples = list(split(data))
    binary_list = ''
    decoded_message = ''

    for sample in full_list_of_samples:
        space = goertzel(sample, SAMPLING_RATE, SPACE_TARGET_FREQUENCY, SAMPLING_SIZE)
        mark = goertzel(sample, SAMPLING_RATE, MARK_TARGET_FREQUENCY, SAMPLING_SIZE)
        if mark > space:
            binary_list += '1'
        else:
            binary_list += '0'

    full_binary_list = [binary_list[i:i + 10] for i in range(0, len(binary_list), 10)]

    for each in full_binary_list:
        decoded_message += chr(int(each[1:9][::-1], 2))

    print decoded_message

import matplotlib.pyplot as plt # For ploting
import numpy as np # to work with numerical data efficiently
from scipy.io import wavfile
import pprint
import wave as wav
import struct
import sys

fs, data = wavfile.read('bozic.wav')


# implement a goertzel filter next
def goertzel(samples, target_frequency, n):
    '''(NumpyArray, Int, Int) -> Magnitude(Complex Number)'''
    # implementation provided by Bart Massey source code can be found here:
    # https://moodle.cs.pdx.edu/mod/page/view.php?id=88
    w0 = (2 * np.pi * target_frequency) / fs
    norm = np.exp(1j * w0 * n)
    coeffs = np.array([-1j * w0 * k for k in range(n)])
    y = np.abs(norm * np.dot(coeffs, samples))
    return y


def goertzel_mag(samples, sampling_rate, target_freq, sample_length):
    # algorithm has been borrowed from embedded.com.
    # Link: https://www.embedded.com/design/configurable-systems/4024443/The-Goertzel-Algorithm
    k = 0.5 + ((sample_length * target_freq) / sampling_rate)
    omega = (2.0 * np.pi / sample_length) * k
    sine = np.sin(omega)
    cosine = np.cos(omega)
    coeff = 2.0 * cosine

    q1 = 0.0
    q2 = 0.0

    for i in range(sample_length):
        q0 = coeff * q1 - q2 + samples[i]
        q2 = q1
        q1 = q0

    real = (q1 - q2 * cosine)
    imag = (q2 * sine)

    magnitude = np.sqrt(real * real + imag * imag)
    return magnitude


def goertzel2(samples, freq, filter_length):
    s_prev = 0.0
    s_prev2 = 0.0
    normalizedfreq = freq / 48000
    coeff = 2 * np.cos(2*np.pi*normalizedfreq)
    for each in range(filter_length):
        s = samples[each] + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s

    power = s_prev2 * s_prev2 + s_prev * s_prev - coeff * s_prev * s_prev2
    return power


def split(l):
    temp = []
    final_list = []
    for item in l:
        temp.append(item)
        if len(temp) == 160:
            final_list.append(temp)
            temp = []

    return final_list


def split_binary(l):
    temp = []
    final_list = []
    for item in l:
        temp.append(item)
        if len(temp) == 10:
            final_list.append(temp)
            temp = []

    return final_list


if __name__ == '__main__':
    subset_samples = []
    binary_list = []
    counter = 0
    for each in data:
        if each != 0:
            subset_samples.append(each)

    full_list_of_samples = list(split(subset_samples))

    for sample in full_list_of_samples:
        space = goertzel_mag(sample, 48000, 2025, 160)
        mark = goertzel_mag(sample, 48000, 2225, 160)
        if mark > space:
            binary_list.append(1)
        else:
            binary_list.append(0)

    list = split_binary(binary_list)
    for each in list:
        print '\n' + str(each)



# # Get the signal file.
# wavfile = wav.open('bozic.wav')
#
# # Channels per frame.
# channels = wavfile.getnchannels()
#
# # Bytes per sample.
# width = wavfile.getsampwidth()
#
# # Sample rate
# rate = wavfile.getframerate()
#
# # Number of frames.
# frames = wavfile.getnframes()
#
# # Length of a frame
# frame_width = width * channels
#
#
# # Get the signal and check it.
# max_sample = None
# min_sample = None
# wave_bytes = wavfile.readframes(frames)
# # Iterate over frames.
# for f in range(0, len(wave_bytes), frame_width):
#     frame = wave_bytes[f : f + frame_width]
#     # Iterate over channels.
#     for c in range(0, len(frame), width):
#         # Build a sample.
#         sample_bytes = frame[c : c + width]
#         # XXX Eight-bit samples are unsigned
#         sample = struct.unpack("<i",sample_bytes)[0]
#         # Check extrema.
#         if max_sample == None:
#             max_sample = sample
#         if min_sample == None:
#             min_sample = sample
#         if sample > max_sample:
#             max_sample = sample
#         if sample < min_sample:
#             min_sample = sample
#
# wavfile.close()
#
# print("min: {}  max: {}".format(min_sample, max_sample))

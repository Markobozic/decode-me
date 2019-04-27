import matplotlib.pyplot as plt # For ploting
import numpy as np # to work with numerical data efficiently
from scipy.io import wavfile
import wave as wav
import struct
import sys

fs, data = wavfile.read('bozic.wav')


# implement a goertzel filter next
def goertzel(samples, target_frequency, n):
    '''(NumpyArray, Int, Int) -> Magnitude(Complex Number)'''
    # implementation provided by Bart Massey source code can be found here: https://moodle.cs.pdx.edu/mod/page/view.php?id=88
    w0 = (2 * np.pi * target_frequency) / fs
    norm = np.exp(1j * w0 * n)
    coeffs = np.array([-1j * w0 * k for k in range(n)])
    y = np.abs(norm * np.dot(coeffs, samples))
    return y


def goertzel_mag(samples, sampling_rate, target_freq, numSamples):
    k = 0.5 + ((numSamples * target_freq) / sampling_rate)
    omega = (2.0 * np.pi * k) / numSamples
    sine = np.sin(omega)
    cosine = np.cos(omega)
    coeff = 2.0 * cosine

    q1 = 0.0
    q2 = 0.0

    for i in range(numSamples):
        q0 = coeff * q1 - q2 + samples[i]
        q2 = q1
        q1 = q0

    real = (q1 - q2 * cosine) / (numSamples / 2)
    imag = (q2 * sine) / (numSamples / 2)

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


# main
if __name__ == '__main__':
    None
    # samp_rate = 100.0
    # k = 2
    # y = np.arange(100)
    # z = np.sin(2*np.pi*k * (x/samp_rate))
    # test = goertzel2(y, 2, 100)
    # print y
    # print z
    # print test
    # Fs = 8000
    # f = 5
    # to_become_sample_array = 8000
    # a = np.arange(to_become_sample_array)
    # b = np.sin(2 * np.pi * f * a / Fs)
    # test2 = goertzel(a, 2025, len(a))
    # plt.plot(test2)
    # plt.xlabel('sample(n)')
    # plt.ylabel('voltage(V)')
    # plt.show()
    #
    # print goertzel2(a, 5, 8000)


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

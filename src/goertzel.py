import numpy as np


def goertzel(samples, sampling_rate, target_freq, sample_length):
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

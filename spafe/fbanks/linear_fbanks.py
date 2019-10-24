##############################################################################################
#                           linear-filter-banks implementation
##############################################################################################
import numpy as np


def linear_filter_banks(nfilts=20,
                        nfft=512,
                        fs=16000,
                        low_freq=None,
                        high_freq=None):
    """
    Compute linear-filterbanks. The filters are stored in the rows, the columns
    correspond to fft bins.

    Args:
        nfilt     (int) : the number of filters in the filterbank.
                          (Default 20)
        nfft      (int) : the FFT size.
                          (Default is 512)
        fs        (int) : sample rate/ sampling frequency of the signal.
                          (Default 16000 Hz)
        low_freq  (int) : lowest band edge of mel filters.
                          (Default 0 Hz)
        high_freq (int) : highest band edge of mel filters.
                          (Default samplerate/2)

    Returns:
        (numpy array) array of size nfilt * (nfft/2 + 1) containing filterbank.
        Each row holds 1 filter.
    """
    # init freqs
    high_freq = high_freq or fs / 2
    low_freq = low_freq or 0

    # compute points evenly spaced in mels (points are in Hz)
    mel_points = np.linspace(low_freq, high_freq, nfilts + 2)

    # we use fft bins, so we have to convert from Hz to fft bin number
    bin = np.floor((nfft + 1) * mel_points / fs)
    fbank = np.zeros([nfilts, nfft // 2 + 1])

    # compute amps of fbanks
    for j in range(0, nfilts):
        b0, b1, b2 = bin[j], bin[j + 1], bin[j + 2]
        fbank[j, int(b0):int(b1)] = (np.arange(int(b0), int(b1)) -
                                     int(b0)) / (b1 - b0)
        fbank[j, int(b1):int(b2)] = (int(b2) -
                                     np.arange(int(b1), int(b2))) / (b2 - b1)

    return np.abs(fbank)

import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import math


def adaptive_peak_detection(signal, initial_window_size, initial_threshold):
    peaks = []

    for i in range(len(signal)):
        # Dinamikus ablakméret beállítása
        window_half_size = initial_window_size // 2
        local_std = np.std(signal[max(0, i - window_half_size):min(len(signal), i + window_half_size + 1)])
        window_size = initial_window_size + int(local_std)
        window_size = max(3, window_size)

        if i < window_size // 2 or i >= len(signal) - window_size // 2:
            continue

        # Dinamikus küszöbérték beállítása
        threshold_half_size = math.floor(initial_threshold // 2)
        local_mean = np.mean(signal[max(0, i - threshold_half_size):min(len(signal), i + threshold_half_size + 1)])
        threshold = local_mean

        local_window = signal[i - window_size // 2:i + window_size // 2 + 1]
        if signal[i] == max(local_window) and signal[i] > threshold:
            peaks.append((i, signal[i]))

    return peaks

def peak_detection(signal, window_size, threshold):
    peaks = []
    for i in range(len(signal)):
        if i < window_size // 2 or i >= len(signal) - window_size // 2:
            continue
        if signal[i] == max(signal[i - window_size // 2:i + window_size // 2 + 1]) and signal[i] > threshold:
            peaks.append((i, signal[i]))
    return peaks

if __name__ == '__main__':
    mat = scipy.io.loadmat(r'C:\Users\Anita\Documents\Optoforce\optoforce_raw_coords_739387.3772379295')
    mat_list = list(mat.items())
    mat_to_plot = mat_list[-1][1][0]
    plt.plot(mat_to_plot, '*-')
    peaks = adaptive_peak_detection(mat_to_plot, 10, 4)

    for i, val in peaks:
        #print(i, "_ ", val)
        plt.plot(i, val, 'ro')
    #print(peaks)
    plt.title("Optoforce measurement")
    plt.xlabel("datapoints in time")
    plt.ylabel("force amplitude")
    plt.show()
    input("vege")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

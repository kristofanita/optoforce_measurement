import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import math

def adaptive_peak_detection(signal, initial_window_size, initial_threshold):
    peaks = []

    for i in range(len(signal)):
        # Dynamic window size setting
        window_half_size = initial_window_size // 2
        local_std = np.std(signal[max(0, i - window_half_size):min(len(signal), i + window_half_size + 1)])
        window_size = initial_window_size + int(local_std)
        window_size = max(3, window_size)

        if i < window_size // 2 or i >= len(signal) - window_size // 2:
            continue

        # Dynamic threshold setting
        threshold_half_size = math.floor(initial_threshold // 2)
        local_mean = np.mean(signal[max(0, i - threshold_half_size):min(len(signal), i + threshold_half_size + 1)])
        threshold = local_mean

        local_window = signal[i - window_size // 2:i + window_size // 2 + 1]
        if signal[i] == max(local_window) and signal[i] > threshold:
            peaks.append(i)

    return peaks

def find_wave_bounds(signal, peak_index, base_threshold=0.0):
    # Find left bound
    left_bound = peak_index
    while left_bound > 0 and signal[left_bound] > base_threshold:
        left_bound -= 1
    left_bound = max(left_bound, 0)

    # Find right bound
    right_bound = peak_index
    while right_bound < len(signal) - 1 and signal[right_bound] > base_threshold:
        right_bound += 1
    right_bound = min(right_bound, len(signal) - 1)

    return left_bound, right_bound

if __name__ == '__main__':
    mat = scipy.io.loadmat(r'C:\Users\Anita\Documents\Optoforce\meres1.mat')
    mat_list = list(mat.items())
    mat_to_plot = mat_list[-1][1][0]

    plt.plot(mat_to_plot, '*-')
    peaks = adaptive_peak_detection(mat_to_plot, 10, 4)

    for peak_index in peaks:
        plt.plot(peak_index, mat_to_plot[peak_index], 'ro')
        left_bound, right_bound = find_wave_bounds(mat_to_plot, peak_index)
        plt.plot([left_bound, right_bound], [mat_to_plot[peak_index]]*2, 'r--')

    plt.title("Optoforce measurement")
    plt.xlabel("Datapoints in time")
    plt.ylabel("Force amplitude")
    plt.show()
    input("vege")

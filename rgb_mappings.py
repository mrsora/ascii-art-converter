"""
All functions are used with np.apply_along_axis to convert the image into a single channel image.
"""
import numpy as np

def average(array: np.array) -> int:
    return np.mean(array)

def lightness(array: np.array) -> int:
    return (np.max(array) + np.min(array)) / 2

def luminosity(array: np.array) -> int:
    return 0.21 * array[0] + 0.72 * array[1] + 0.07 * array[2]
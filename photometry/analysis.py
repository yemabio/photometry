import numpy as np

def linear_fit(y_series, x_series):
    reg = np.polyfit(x_series, y_series, 1)
    
    a = reg[0]
    b = reg[1]
    
    y_fitted = a * x_series + b
    
    return y_fitted, a, b

def compute_delta_f_over_f(signal, baseline):
    normed_signal = (signal - baseline) / baseline  # this gives deltaF/F
    normed_signal *= 100  # get %
    return normed_signal


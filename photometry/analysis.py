import numpy as np
from photometry import utils

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

def convert_sig_to_df_f(signal, baseline, z_norm=False):
    fitted_baseline,_,_ = linear_fit(signal, baseline)
    if z_norm:
        return z_score(compute_delta_f_over_f(signal, fitted_baseline))
    else:
        return compute_delta_f_over_f(signal,fitted_baseline)

def subtract_pre_ttl(time_series, ttl, pre_pulse_interval):
    pulse_end = np.where(ttl == 1)[0][-1]
    # print(pulse_end)
    pre_ttl_mean = time_series[pulse_end+1-pre_pulse_interval:pulse_end+1].mean()
    # print(pre_ttl_mean)
    # print(len(time_series-pre_ttl_mean))
    # return (time_series - pre_ttl_mean)[pulse_end+1:]
    return(time_series - pre_ttl_mean)[pulse_end+1-pre_pulse_interval:]


def z_score(time_series):
    return (time_series-time_series.mean())/time_series.std()

def get_df_f_from_doric(filename, z_norm=False, subtract_pre_inj=0):
    data = utils.get_signal_and_baseline(filename, get_ttl=subtract_pre_inj)
    signal = data[0]
    baseline = data[1]

    df_f = convert_sig_to_df_f(signal, baseline, z_norm=z_norm)



    # if subtract_pre_inj:
        # signal = subtract_pre_ttl(data[0], data[2])
        # baseline = subtract_pre_ttl(data[1], data[2])
        
    # else:
        # signal = data[0]
        # baseline = data[1]
    
    if subtract_pre_inj:
        return subtract_pre_ttl(df_f, data[2], pre_pulse_interval=subtract_pre_inj)

    else:
        return df_f
        # return convert_sig_to_df_f(signal, baseline,z_norm=z_norm), np.where(data[2] == 1)[0][-1]
    # else:
        # return convert_sig_to_df_f(signal, baseline, z_norm=z_norm)


    


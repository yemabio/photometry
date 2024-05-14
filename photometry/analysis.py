import numpy as np
from photometry import utils
from scipy.ndimage import gaussian_filter1d

class DataFile:
    def __init__(self, 
                 filename, 
                 z_norm=False,
                 minutes_before_ttl_pulse=0,
                 baseline_mode='mean',
                 datatype=None,
                 frequency=0.0166,
                 smoothing=0,
                 ):
        self.filename = filename
        self.datatype=datatype
        self.minutes_before_ttl_pulse = minutes_before_ttl_pulse
        self.baseline_mode = baseline_mode
        self.frequency=frequency
        self.z_norm = z_norm
        self.baseline_interval = self.convert_min_to_timesteps()
        self.df_f = None
        self.ttl_end = 0
        self.extract_df_f()
        if smoothing:
            self.smoothed_df_f = gaussian_filter1d(self.df_f, smoothing)

    def convert_min_to_timesteps(self):
        return(int((self.minutes_before_ttl_pulse)*60/self.frequency))
    
    # def returner(self):
    #     return returner(self.frequency)
    
    def extract_df_f(self):
        extracted_df_f = get_df_f_from_doric(self.filename,z_norm=self.z_norm,baseline_interval=self.baseline_interval, baseline_mode=self.baseline_mode)
    # for file_id, file_obj in file_dict.items():
    #  = analysis.get_df_f_from_doric(file_obj.filename,z_norm=True, subtract_pre_inj=file_obj.pre_injection_interval)
        # if extracted_df_f[1]:
        self.df_f, self.ttl_end = extracted_df_f
        # else:
            # self.df_f = extracted_df_f 
# def returner(x):
#     return x+1
        

def linear_fit(y_series, x_series):
    reg = np.polyfit(x_series, y_series, 1)
    
    a = reg[0]
    b = reg[1]
    
    y_fitted = a * x_series + b
    
    return y_fitted, a, b

def compute_delta_f_over_f(signal, fitted_isosbestic):
    normed_signal = (signal - fitted_isosbestic) / fitted_isosbestic  # this gives deltaF/F
    normed_signal *= 100  # get %
    return normed_signal

def convert_sig_to_df_f(signal, isosbestic):
    fitted_isosbestic,_,_ = linear_fit(signal, isosbestic)
    # if z_norm:
        # return z_score(compute_delta_f_over_f(signal, fitted_isosbestic))
    # else:
    return compute_delta_f_over_f(signal,fitted_isosbestic)

def get_pulse_end(ttl):
    return np.where(ttl == 1)[0][-1]

def subtract_pre_ttl(time_series, ttl, pre_pulse_interval,baseline_mode):
    # pulse_end = np.where(ttl == 1)[0][-1]
    # print(pulse_end)
    # if baseline_mode == "mean":
        # pre_ttl_subtraction = time_series[pulse_end+1-pre_pulse_interval:pulse_end+1].mean()
    # elif baseline_mode == "median":
        # pre_ttl_subtraction = np.median(time_series[pulse_end+1-pre_pulse_interval:pulse_end+1])
    # print(pre_ttl_mean)
    # print(len(time_series-pre_ttl_mean))
    # return (time_series - pre_ttl_mean)[pulse_end+1:]
    pulse_end, pre_ttl_subtraction = extract_pre_ttl(time_series, ttl, pre_pulse_interval)
    if baseline_mode == "median":
        pre_ttl_subtraction = np.median(pre_ttl_subtraction)
    elif baseline_mode == "mean":
        pre_ttl_subtraction = np.mean(pre_ttl_subtraction)
    return((time_series - pre_ttl_subtraction)[pulse_end+1-pre_pulse_interval:], pulse_end)

def extract_pre_ttl(time_series, ttl, pre_pulse_interval):
    pulse_end = get_pulse_end(ttl)
    # if mode == "mean":
    pre_ttl = time_series[pulse_end+1-pre_pulse_interval:pulse_end+1]
    # elif mode == "median":
        # pre_ttl = np.median(time_series[pulse_end+1-pre_pulse_interval:pulse_end+1])
    return pulse_end, pre_ttl

def z_score(time_series, baseline_series=[], baseline_mode="mean"):
    if len(baseline_series) == 0:
        return (time_series-time_series.mean())/time_series.std()
    else:
        if baseline_mode=="mean":
            return (time_series-baseline_series.mean())/baseline_series.std()
        elif baseline_mode=="median":
            return (time_series-np.median(baseline_series))/baseline_series.std()

def get_df_f_from_doric(filename, z_norm, baseline_interval=0, baseline_mode="mean"):
    data = utils.get_signal_and_isosbestic(filename, get_ttl=baseline_interval)
    signal = data[0]
    isosbestic = data[1]
    if baseline_interval > 0:
        ttl = data[2]
    
    pulse_end = 0
    df_f = convert_sig_to_df_f(signal, isosbestic)

    if z_norm == 'standard':
        df_f = z_score(df_f)
        if baseline_interval:
            df_f, pulse_end = subtract_pre_ttl(df_f, ttl, pre_pulse_interval=baseline_interval,baseline_mode=baseline_mode)

    elif z_norm == 'baseline':
        pulse_end, pre_ttl = extract_pre_ttl(df_f, ttl, baseline_interval)
        df_f = z_score(df_f, baseline_series=pre_ttl,baseline_mode=baseline_mode)
    

    return df_f, pulse_end
        # return convert_sig_to_df_f(signal, baseline,z_norm=z_norm), np.where(data[2] == 1)[0][-1]
    # else:
        # return convert_sig_to_df_f(signal, baseline, z_norm=z_norm)


    


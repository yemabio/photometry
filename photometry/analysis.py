import numpy as np
from photometry import utils
from scipy.ndimage import gaussian_filter1d

class DataFile:
    def __init__(self, 
                 filename, 
                 minutes_before_ttl_pulse=0,
                 subtraction_mode='mean',
                 datatype=None,
                 frequency=0.0166,
                 z_norm=True,
                 smoothing=0,
                 ):
        self.filename = filename
        self.datatype=datatype
        self.minutes_before_ttl_pulse = minutes_before_ttl_pulse
        self.subtraction_mode = subtraction_mode
        self.frequency=frequency
        self.z_norm = z_norm
        self.pre_injection_interval = self.convert_min_to_timesteps()
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
        extracted_df_f = get_df_f_from_doric(self.filename,z_norm=self.z_norm,subtract_pre_inj=self.pre_injection_interval, subtraction_mode=self.subtraction_mode)
    # for file_id, file_obj in file_dict.items():
    #  = analysis.get_df_f_from_doric(file_obj.filename,z_norm=True, subtract_pre_inj=file_obj.pre_injection_interval)
        if len(extracted_df_f) == 2:
            self.df_f, self.ttl_end = extracted_df_f
        else:
            self.df_f = extracted_df_f 
# def returner(x):
#     return x+1
        

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

def get_pulse_end(ttl):
    return np.where(ttl == 1)[0][-1]

def subtract_pre_ttl(time_series, ttl, pre_pulse_interval,subtraction_mode):
    pulse_end = np.where(ttl == 1)[0][-1]
    # print(pulse_end)
    if subtraction_mode == "mean":
        pre_ttl_subtraction = time_series[pulse_end+1-pre_pulse_interval:pulse_end+1].mean()
    elif subtraction_mode == "median":
        pre_ttl_subtraction = np.median(time_series[pulse_end+1-pre_pulse_interval:pulse_end+1])
    # print(pre_ttl_mean)
    # print(len(time_series-pre_ttl_mean))
    # return (time_series - pre_ttl_mean)[pulse_end+1:]
    return(time_series - pre_ttl_subtraction)[pulse_end+1-pre_pulse_interval:]


def z_score(time_series):
    return (time_series-time_series.mean())/time_series.std()

def get_df_f_from_doric(filename, z_norm=False, subtract_pre_inj=0, subtraction_mode="mean"):
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
        return (subtract_pre_ttl(df_f, data[2], pre_pulse_interval=subtract_pre_inj,subtraction_mode=subtraction_mode),get_pulse_end(data[2]))

    else:
        return df_f
        # return convert_sig_to_df_f(signal, baseline,z_norm=z_norm), np.where(data[2] == 1)[0][-1]
    # else:
        # return convert_sig_to_df_f(signal, baseline, z_norm=z_norm)


    


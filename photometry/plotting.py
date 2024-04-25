import matplotlib.pyplot as plt
import numpy as np

#DO NOT EDIT: set plotting parameters

def plot_traces(file_dict, smoothed=False, ymin=-2,ymax=2):

    linewidth=.5
    fig, ax = plt.subplots(figsize=(4,1.5))
    ax.spines[['right','top']].set_visible(False)
    ax.set_ylabel(r'$\Delta$F/F')
# ax.vlines(pre_injection_interval,  
#            ymin = 0, ymax = 1, color = 'k', linewidth=linewidth, linestyle = '--', 
#            transform=ax.get_xaxis_transform(), label='Injection')
    ax.set_xlabel('Time (min.)')
    for i, (_, file_obj) in enumerate(file_dict.items()):
    
        if i == 0:
            x = np.arange(len(file_obj.df_f))
            x_inj_zero_idx = file_obj.ttl_end
            x -= x_inj_zero_idx
            x = [float(val)*file_obj.frequency/60 for val in x]
            ax.vlines(x[file_obj.ttl_end],  
            ymin = 0, ymax = 1, color = 'k', linewidth=linewidth, linestyle = '--', 
            transform=ax.get_xaxis_transform(),zorder=len(file_dict))
            if smoothed:
                ax.plot(x[file_obj.ttl_end-file_obj.pre_injection_interval:file_obj.ttl_end],file_obj.smoothed_df_f[file_obj.ttl_end-file_obj.pre_injection_interval:file_obj.ttl_end], linewidth=linewidth,label=file_obj.datatype,zorder=i, color=color_picker(file_obj))
                ax.plot(x[file_obj.ttl_end:],file_obj.smoothed_df_f[file_obj.ttl_end:], linewidth=linewidth,zorder=i,color=color_picker(file_obj))
            else:
                ax.plot(x[file_obj.ttl_end-file_obj.pre_injection_interval:file_obj.ttl_end],file_obj.df_f[file_obj.ttl_end-file_obj.pre_injection_interval:file_obj.ttl_end], linewidth=linewidth,label=file_obj.datatype,zorder=i, color=color_picker(file_obj))
                ax.plot(x[file_obj.ttl_end:],file_obj.df_f[file_obj.ttl_end:], linewidth=linewidth,zorder=i,color=color_picker(file_obj))
            

        else: 
            x_inj_to_end = x[x_inj_zero_idx:]
            x_start_to_inj = x[x_inj_zero_idx-file_obj.pre_injection_interval:x_inj_zero_idx]
            if smoothed:
                df_from_inj = file_obj.smoothed_df_f[file_obj.ttl_end:]
                df_pre_inj = file_obj.smoothed_df_f[file_obj.ttl_end-file_obj.pre_injection_interval:file_obj.ttl_end]
            else:
                df_from_inj = file_obj.df_f[file_obj.ttl_end:]
                df_pre_inj = file_obj.df_f[file_obj.ttl_end-file_obj.pre_injection_interval:file_obj.ttl_end]
            start_length = np.min([len(x_start_to_inj), len(df_pre_inj)])
            end_length = np.min([len(x_inj_to_end),len(df_from_inj)])
            ax.plot(x_inj_to_end[:end_length],df_from_inj[:end_length], linewidth=linewidth,label=file_obj.datatype,zorder=i,color=color_picker(file_obj))
            ax.plot(x_start_to_inj[:start_length],df_pre_inj[:start_length], linewidth=linewidth,zorder=i,color=color_picker(file_obj))
 
    ax.axhline(0, xmin=0, xmax=1, color ='k', linewidth=linewidth, linestyle='--',zorder=len(file_dict)+1)
    ax.legend(fontsize=5)

    ax.set_ylim((ymin,ymax))

def color_picker(file_obj):
    if file_obj.datatype == 'Saline':
        color='lightgray'
    elif file_obj.datatype == 'CNO':
        color='green'
    else:
        color='blue'
    return color





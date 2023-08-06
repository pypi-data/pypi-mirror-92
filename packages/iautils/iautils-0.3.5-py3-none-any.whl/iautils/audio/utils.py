import os, random
from pathlib import Path
import pandas as pd
import numpy as np
import librosa, cv2, soundfile
import matplotlib.pyplot as plt
from tqdm import tqdm
from nptdms import TdmsFile


################################################################
# save_waveform
################################################################
def save_waveform(y, sr, savepath, resample_sr=22050):
    '''
    html에서 재생가능한 waveform으로 resampling하여 저장
    '''
    try:
        soundfile.write(
            savepath, 
            librosa.resample(y, sr, resample_sr),
            resample_sr,
            subtype='PCM_32'
        )
    except Exception as ex:
        print(f"[ERROR] cannot write waveform {savepath.rsplit('/', 1)[-1]} - {ex}")
        
        
################################################################
# save_spectrogram
################################################################
def save_spectrogram(S, savepath=None, dpi=72, cmap='magma', vmin=None, vmax=None):
    '''
    save spectrogram using matplotlib's cmap
    
    params
      S
      savepath
      dpi
      cmap
      vmin
      vmax
      
    return
      (void)
    '''
    H, W = (x/dpi for x in S.shape)

    # figure without frame
    fig = plt.figure(frameon=False)
    fig.set_size_inches(W, H)

    # fill content on figure
    ax = plt.Axes(fig, [0., 0., 1., 1.,])
    ax.set_axis_off()
    fig.add_axes(ax)

    # draw
    ax.imshow(S, origin='lower', cmap=cmap, vmin=vmin, vmax=vmax)
    
    if savepath is not None:
        # close after save - avoid display
        fig.savefig(savepath, dpi=dpi)
        plt.close()
        
    else:
        plt.show()
        

################################################################
# save_rms
################################################################
def save_rms(x, savepath=None, ylim=None, States=None, steady=None, dpi=72, height=0.5, annotation=True, state_colors=None):
    '''
    report 용도
    
    params
      rms
      savepath
      height
      ylim
      dpi
      
    return
      (void)
    '''

    # 
    if state_colors is None:
        state_colors = {
            0: 'darkgray',
            1: 'red',
            2: 'tomato',
            4: 'orange'
        }
    
    # dataset
    data = pd.DataFrame({
        'x': np.arange(0, x.shape[0]),
        'y': x,
    })
    
    # States
    if States is not None:
        data['states'] = States

    # size
    H = height # inches
    W = x.shape[0]/dpi

    # create figure
    fig = plt.figure(frameon=False)
    fig.set_size_inches(W, H)

    # add axis
    ax = plt.Axes(fig, [0, 0, 1, 1])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    # set lims
    ax.set_xlim(0, x.shape[0])
    if ylim is not None:
        ax.set_ylim(ylim)
        
    # plot
    if States is None:
        ax.fill_between(data['x'], data['y'], color='darkgray')
    
    else:
        states_ = sorted(set(States))
        for state_ in states_:
            # filter
            data_ = data.loc[data['states']==state_, :]
            
            # label
            if steady is not None:
                lab_ = "Steady" if state_ == steady else ""
                color = "darkgray" if state_ == steady else "red"
            else:
                if W/x.shape[0]*data_.shape[0] > 1:
                    lab_ = f"State {state_}"
                else:
                    lab_ = f"S{state_}"
                color = state_colors[state_]
            
            # plot
            ax.fill_between(data_['x'], data_['y'], color=color)
            
            # if annotation
            if annotation:
                ax.text(
                    (data_['x'].min()+data_['x'].max())*.5, ax.get_ylim()[-1]*.5, 
                    s=lab_, 
                    horizontalalignment='center', verticalalignment='center', fontsize=12
                )

    # save image
    if savepath is not None:
        # close after save - avoid display
        fig.savefig(savepath, dpi=dpi)
        plt.close()
        
    else:
        plt.show()
        
        
# def save_rms(x, savepath=None, height=0.5, ylim=None, bkpts=None, states=None, steady=None, dpi=72, ):
#     '''
#     report 용도
    
#     params
#       rms
#       savepath
#       height
#       ylim
#       bkpts
#       states
#       steady
#       dpi
      
#     return
#       (void)
#     '''
    
#     #
#     data = pd.DataFrame({
#         'x': np.arange(0, x.shape[0]),
#         'y': x,
#         'states': states,
#     })
    
#     # size
#     H = height # inches
#     W = x.shape[0]/dpi

#     # create figure
#     fig = plt.figure(frameon=False)
#     fig.set_size_inches(W, H)

#     # add axis
#     ax = plt.Axes(fig, [0, 0, 1, 1])
#     ax.set_axis_off()
#     fig.add_axes(ax)

#     # plot
#     ax.fill_between(data['x'], data['y'], color='darkgray')

#     # xlim & ylim
#     ax.set_xlim(0, x.shape[0])
#     if ylim is not None:
#         ax.set_ylim(ylim)
        
#     # bkpts
#     if bkpts is not None:
#         cuts = [0] + bkpts + [x.shape[0]]
#         cuts_center = (np.array(cuts[1:]) + np.array(cuts[:-1]))/2
# #         cuts_color = 'black'
# #         cuts_lw = 1
# #         for xl in cuts:
# #             ax.axvline(xl, color=cuts_color, lw=cuts_lw)
            
#         # unsteady section
#         if states is not None:
#             if steady is not None:
#                 yc = ax.get_ylim()[1] / 2
#                 unsteady = data.loc[data['states']!=steady, :]
#                 ax.fill_between(unsteady['x'], unsteady['y'], color='red')
#                 ax.text(cuts_center[steady], yc, s='steady', fontsize=12)

#     #
#     if savepath is not None:
#         # close after save - avoid display
#         fig.savefig(savepath, dpi=dpi)
#         plt.close()
        
#     else:
#         plt.show()

        
################################################################
# load (y, sr)
################################################################
# class Loader(object):
    
#     def __init__(self, filetype, group=None, channel=None, sr=None):
        
#         filetype = filetype.strip('.').lower()
#         self.group = group
#         self.channel = channel
#         self.sr = sr
        
#         if filetype in ['wav', 'wave', 'waveform']:
#             self.filetype = 'wav'
#             self.loader = soundfile.read
#         elif filetype in ['tdms']:
#             self.filetype = 'tdms'
#             self.loader = None
            
#     def __call__(self, filepath):
        
#         if self.loader is None:
#             if self.filetype == 'tdms':
                
    

def load(filepath, group=None, channel=None, sr=None):
    '''
    universal file loader for audio files (wav, tdms)
    '''
    ext = filepath.rsplit('.', 1)[-1].lower()
    
    if ext == 'wav':
        y, sr = soundfile.read(filepath, samplerate=sr)
        return y, sr
    
    elif ext == 'tdms':
        # read group
        f = TdmsFile(filepath)
        if group is not None:
            try:
                g = f[group]
            except:
                print(f"There is no group name '{group}'. Available groups are:")
                for g in f.groups():
                    print(g.name, end=", ")
                return
        else:
            if len(f.groups()) == 1:
                g = f.groups()[0]
            else:
                print(f"You have multiple groups. Please select one:")
                for g in f.groups():
                    print(g.name, end=", ")
                return

        # read channel
        try:
            ch = g[channel]
            y = ch[:]
        except:
            print(f"Channel '{channel}' is not exist. Available channels are:")
            for ch in g.channels():
                print(ch.name, end=", ")
            return
        
        # read properties 'dt'
        try:
            sr = int(1/ch.properties['dt'])
        except Exception as ex:
            if ex == 'dt':
                print(f"sampling rate will be None because the channel '{channel}' has no property name 'dt'. please set sampling rate manually")
            else:
                print(ex)
            sr = None
            
        return y, sr
        
               
################################################################
#### AudioDataset (DEFAULT)
################################################################
class AudioDataset(object):
    
    def __init__(self, labels, prep, label_dtype=None):
        
        # pd.series to list
        self.filename = labels.filename.tolist()
        self.filepath = labels.filepath.tolist()
        
        # assume binery_cross_entropy if label's codes are object (string), bce requires float32 label
        if labels.label.dtype == object:
            self.label = labels.label.str.split('|', expand=True).astype(int).to_numpy()
            self.dtype = np.float32
        # assume cross_entropy if label's codes are integer, cross_entropy requires int64 label
        else:
            self.label = labels.label.tolist()
            self.dtype = np.int64
        
        # prep = load + transforms
        self.prep = prep

        # manual dtype
        if label_dtype:
            self.dtype = label_dtype
    
    def __len__(self):
        return len(self.label)
    
    def __getitem__(self, idx):
        
        # parse index
#         idx = idx.tolist() if torch.is_tensor(idx) else idx
        
        # get filename, filepath, y
        filename = self.filename[idx]
        filepath = self.filepath[idx]
#         y = torch.tensor(self.label[idx], dtype=self.dtype)
        y = self.dtype(self.label[idx])
        
        # prep: filepath -> load -> transform -> model input x
        x = self.prep(filepath)
        
        return x, y, filename

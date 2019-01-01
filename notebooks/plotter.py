import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

@interact(
    colormap=['viridis', 'plasma', 'inferno', 'magma', 'Greys', 'Greys_r'],
    section=widgets.RadioButtons(options=['inline', 'xline', 'timeslice'],
                                 value='inline',description='slicer',disabled=False),
    inline=widgets.IntSlider(value=300,min=0,max=600,step=1,
                             continuous_update=False,description='<font color="red">inline</>'),
    xline=widgets.IntSlider(value=240,min=0,max=480,step=1,
                            continuous_update=False,description='<font color="green">xline</>'),
    timeslice=widgets.IntSlider(value=125,min=0,max=250,step=1,
                                continuous_update=False,description='<font color="blue">timeslice</>'),
)
def seismic_plotter(colormap, section, inline, xline, timeslice):
    """Plot a chosen seismic ILine, XLine or Timeslice with a choice of colormaps"""
    
    # load a volume
    vol = np.load('../data/Penobscot_0-1000ms.npy')
    
    # sections dictionary
    sections = {
        'inline': {'amp': vol[inline,:,:].T, 'line': inline, 'shrink_val': 0.6, 
                  'axhline_y': timeslice, 'axhline_c': 'b', 
                  'axvline_x': xline, 'axvline_c': 'g',
                  'axspine_c': 'r'},
        'xline': {'amp': vol[:,xline,:].T, 'line': xline, 'shrink_val': 0.5, 
                  'axhline_y': timeslice, 'axhline_c': 'b', 
                  'axvline_x': inline, 'axvline_c': 'r',
                  'axspine_c': 'g'},
        'timeslice': {'amp': vol[:,:,timeslice], 'line': timeslice, 'shrink_val': 0.95, 
                  'axhline_y': xline, 'axhline_c': 'g', 
                  'axvline_x': inline, 'axvline_c': 'r',
                  'axspine_c': 'b'},
    }

    # scale amplitudes
    ma = np.percentile(vol, 98)
    
    # plot figure
    fig, ax = plt.subplots(figsize=(18, 6), ncols=1)

    sec = sections[section]    
    im = ax.imshow(sec['amp'], aspect=0.5, vmin=-ma, vmax=ma, cmap=colormap)
    ax.set_title(f'Penobscot_0-1000ms {section} {sec["line"]}')
    plt.colorbar(im, ax=ax, shrink=sec['shrink_val']).set_label(colormap)
     
    # add projected lines
    ax.axhline(y=sec['axhline_y'], linewidth=2, color=sec['axhline_c'])
    ax.axvline(x=sec['axvline_x'], linewidth=2, color=sec['axvline_c'])
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)     
        ax.spines[axis].set_color(sec['axspine_c'])
    
    plt.show()
    
    return

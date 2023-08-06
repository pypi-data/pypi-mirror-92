import numpy as np, pandas as pd
import sys


def zero_pad(X, pad_width, dims):
    """
    Pads the given array X with zeroes at the both end of given dims.
    Args:
        X: numpy.ndarray.
        pad_width: int, width of the padding.
        dims: int or tuple, dimensions to be padded.
    Returns:
        X_padded: numpy.ndarray, zero padded X.
    """
    dims = (dims) if isinstance(dims, int) else dims
    pad = [(0, 0) if idx not in dims else (pad_width, pad_width)
            for idx in range(len(X.shape))]
    X_padded = np.pad(X, pad, 'constant')
    return X_padded

def load_data(filename):
    data = pd.read_csv(filename,low_memory=False ,header=None)
    data = np.asarray(data)
    y=data[1:,0]
    x=data[1:,1:]
    x_3d=np.reshape(x,(x.shape[0],28,28))  

    return x,y,x_3d



    
# import numpy as np
import os
import itertools as it


def mat2pgf(mat):
    ret = []
    flag = True
    for index in it.product(*[range(s) for s in mat.shape]):
        if flag:
            ret = [[] for _ in range(len(index)+1)]
            flag = False
        for i in range(len(index)):
            ret[i].append(index[i])
        ret[-1].append(mat[index])
    return ret


def hist2pgf(counts, edges):
    # usage
    # h,b = np.histogram(data.EVac, bins='auto', density=True)
    # x,y = hist2pgfplot(h,b)
    x = []
    y = []
    x.extend([edges[0]]*2)
    y.extend([0, counts[0]])
    for i in range(len(counts)-1):
        x.extend([edges[i+1]]*2)
        y.extend([counts[i], counts[i+1]])
    x.extend([edges[-1]]*2)
    y.extend([counts[-1], 0])
    return x, y


def _fileExportNumpy(data, fname, header):
    s = ['{:.4g}']*data.shape[0]
    s.append('\n')
    s = ' '.join(s)
    with open(fname, 'w') as o:
        o.write(header)
        for line in data.T:
            o.write(s.format(*line))


def _fileExportList(data, fname, header):
    s = ['{:.4g}']*len(data)
    s.append('\n')
    s = ' '.join(s)
    with open(fname, 'w') as o:
        o.write(header)
        for line in zip(*data):
            o.write(s.format(*line))


def _fileExportHeader(header):
    if isinstance(header, str):
        header = header.strip()
        header += '\n'
    elif isinstance(header, (list, tuple)):
        header.append('\n')
        header = ' '.join(header)
    else:
        raise ValueError(
            'Data type of header unknown: {}'.format(type(data)))
    return header


def fileExport(data, fname, header, ow=False):
    if (not ow) and os.path.isfile(fname):
        raise FileExistsError(
            '{} exists and overwrite is {}!'.format(fname, ow))
    header = _fileExportHeader(header)
    # check if data is numpy array without loading numpy
    if 'numpy' in str(type(data)):
        _fileExportNumpy(data, fname, header,)
    elif isinstance(data, (list, tuple)):
        _fileExportList(data, fname, header)
    else:
        raise ValueError(
            'Data type of input data unknown: {}'.format(type(data)))


def terminalExport(X, Y, Z=None):
    if Z:
        if (len(X) != len(Y)) or (len(X) != len(Z)):
            raise ValueError('X, Y, Z are not of the same length!')
        for x, y, z in zip(X, Y, Z):
            print('({:.4g},{:.4g},{:.4g})'.format(x, y, z))
    else:
        if len(X) != len(Y):
            raise ValueError('X and Y are not of the same length!')
        for x, y in zip(X, Y):
            print('({:.4g},{:.4g})'.format(x, y))

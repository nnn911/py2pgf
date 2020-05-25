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


def fileExport(data, fname, header, ow=False):
    if (not ow) and os.path.isfile(fname):
        raise FileExistsError(
            '{} exists and overwrite is {}!'.format(fname, ow))
    s = ['{:.4g}']*data.shape[0]
    s.append('\n')
    s = ' '.join(s)
    header.append('\n')
    with open(fname, 'w') as o:
        if header:
            o.write(' '.join(header))
        for d in data.T:
            o.write(s.format(*d))


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

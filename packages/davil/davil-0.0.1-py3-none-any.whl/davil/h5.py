import h5py
import numpy as np

from src.davil import log


def groups(h5_file_path):
    h5_file = h5py.File(h5_file_path, mode='r')
    for h5_key in h5_file.keys():
        group_candidate = h5_file[h5_key]
        if not isinstance(group_candidate, h5py.Group):
            log.warn('Current value for key \'{}\' in .h5 file is not a valid h5 group but of type: {}. '
                     'Key will be skipped.'.format(h5_key, repr(type(group_candidate))))
            continue
        yield group_candidate, h5_key
    h5_file.close()


def datasets(group):
    for dataset_key in group.keys():
        data = group[dataset_key]
        yield np.array(data)

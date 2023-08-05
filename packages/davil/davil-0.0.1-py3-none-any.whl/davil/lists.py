import numbers
from functools import reduce
from typing import Iterable, List

import numpy as np


def filter_split(strings: List[str], patterns: List[str]):
    splits = []
    for pat in patterns:
        splits.append(list(filter(lambda x: pat in x, strings)))
    return tuple(splits)


def partition(lists, ratio, seed):
    x = [np.array(l) for l in lists]

    for arr in x:
        if arr.shape[0] != x[0].shape[0]:
            raise ValueError('All lists must have the same shape in first dimension!')

    if seed is not None:
        np.random.seed(seed)

    size = x[0].shape[0]

    idxs = np.arange(size)
    np.random.shuffle(idxs)

    split_idx = int(np.floor(size * (1 - ratio)))

    firsts = [arr[idxs[0:split_idx]] for arr in x]
    seconds = [arr[idxs[split_idx:size]] for arr in x]

    return firsts, seconds


def partition_train_test(lists, test_ratio=0.1, seed=None):
    firsts, seconds = partition(lists, ratio=test_ratio, seed=seed)
    return firsts, seconds


def partition_train_test_validation(lists, test_ratio=0.1, validation_ratio=0.2, seed=None):
    ref_ratio = test_ratio + validation_ratio
    train_partitions, tests_partitions = partition_train_test(lists, test_ratio=ref_ratio, seed=seed)

    validation_of_ref_ratio = validation_ratio / ref_ratio
    tests_partitions, val_partitions = partition_train_test(tests_partitions, test_ratio=validation_of_ref_ratio,
                                                            seed=seed)
    return train_partitions, tests_partitions, val_partitions


def shuffle_lists(*lists, seed=None):
    size = len(lists[0])
    for l in lists:
        assert len(l) == size

    np.random.seed(seed)

    arrs = [np.array(x) for x in lists]
    s = np.arange(size)
    np.random.shuffle(s)
    arrs = [list(x[s]) for x in arrs]

    return tuple(arrs)


def check_for_same_length(lists, names, expected_length=None, extra_message=None):
    if expected_length:
        length = expected_length
    else:
        length = len(lists[0])

    msg = 'All lists must have length' + str(length) + ': ' + repr(names)
    for l in lists:
        if len(l) is not length:
            if extra_message is not None:
                msg += '\n' + extra_message
            raise ValueError(msg)


def len_iterator(iterator):
    return sum(1 for _ in iterator)


def prod(iterable: Iterable[numbers.Number]):
    return reduce(lambda x, y: x * y, iterable)


def divide_list(l: List, partition_idxs: List[int]):
    compl_idxs = list(range(len(l)))
    compl_idxs = list(filter(lambda x: x not in partition_idxs, compl_idxs))
    return [l[i] for i in compl_idxs], [l[i] for i in partition_idxs]


def pop_idxs(l: List, pops: List[int]):
    ps = []
    pops.sort()
    for i, p in enumerate(pops):
        ps.append(l.pop(p - i))
    return ps


def windowed(iterator: iter, window_size: int, stride: int):
    current_batch = []
    skips = 0

    if stride < 1:
        raise ValueError('Stride must be larger zero. Else there will be an endless loop.')

    for i, x in enumerate(iterator):

        if skips > 0:
            skips -= 1
            continue

        if len(current_batch) < window_size:
            current_batch.append(x)

        elif len(current_batch) == window_size:
            yield list(current_batch)
            skips = stride - window_size
            for c in range(stride):
                if len(current_batch) != 0:
                    current_batch.pop(0)
            if skips <= 0:
                current_batch.append(x)
            else:
                skips -= 1

        else:
            raise AssertionError('Should not have happened. Implementation error.')

    if len(current_batch) > 0:
        yield current_batch

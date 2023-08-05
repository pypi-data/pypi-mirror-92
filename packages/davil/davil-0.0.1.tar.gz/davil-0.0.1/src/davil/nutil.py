from typing import List

import numpy as np
from scipy.interpolate import RectBivariateSpline


def copy_to_from_subarray(dst, subarray, point, subarray_mask=None, pivot='top_left'):
    """
    Copies the specified subarray to the specified destination at location offset. If subarray runs out of bounds,
    the subarray will be sliced to fit into the image.

    :param subarray_mask: Optional subarray mask withs shape [ds0, ds1, 1, ... , 1]. Must have distinct values [0, 1].
    Only locations corresponding to the value 1 in the mask will be copied.
    :param dst: Array to copy to with shape [d0, d1, d3, ... , dn]
    :param subarray: Subarray to copy into destination with shape [ds0, ds1, d3, ... , dn]
    :param point:  The matrix coordinates where to place the subarray
    :param pivot: Either 'top_left', or 'center'. Determines the position of the offset point relative to the subarray.
    'top_left': offset point refers to (0, 0) in subarray, hence it will be copied to the right and below.
    'center': offset point refers to ((subarray.shape[0]-1)/2, (subarray.shape[1]-1)/2), i.e. to the center point of the
    subarray. For this mode, the center of subarray must be defined, i.e. both dimensions must be uneven.
    :return: Dst with values copied from subarray at specified point.
    """

    if len(dst.shape) < 2 or len(subarray.shape) < 2:
        raise ValueError('Destination and subarray must be at minimum 2D arrays.')

    if len(dst.shape) is not len(subarray.shape):
        raise ValueError('Destination and subarray must have the same number of dimensions.')

    if subarray_mask is not None:
        if len(dst.shape) is not len(subarray.shape):
            raise ValueError('Subarray and mask must have the same number of dimensions.')

        if subarray_mask.shape[0:2] != subarray.shape[0:2]:
            raise ValueError('Subarray and mask must have the same size.')

        if len(subarray_mask.shape) > 2:
            for d in subarray_mask.shape[2:-1]:
                if d != 1:
                    raise ValueError('Subarray mask shape must be 1 in all but the first two dimensions.')

    if len(point) != 2:
        raise ValueError('Offset must be a 2D array index. However, length of offset was: {}'.format(len(point)))

    if point[0] < 0 or point[1] < 0:
        raise ValueError('Offset coordinates must be positive.')

    s = subarray.shape
    d = dst.shape

    # (y1,y2) and (x1,x2) are the dimension intervals in the destination array, hence where to copy to
    # (sy1,sy2) and (sx1,sx2) are the dimension intervals in the subarray
    if pivot == 'top_left':
        # offset will not be negative, hence can't run out of bounds in 'top_left' mode for start of interval
        y1 = point[0]
        # clip to max destination array size
        y2 = np.minimum(point[0] + s[0], d[0])
        x1 = point[1]
        x2 = np.minimum(point[1] + s[1], d[1])

        # in 'top_left' mode we can always use the start of the subarray
        sy1 = 0
        # ((offset[0] + s[0]) - d[0]) is the size of the part of the subarray that ran out of bounds. Will be negative
        # if we did not run out of bounds.
        # Hence, we subtract it from the size of the subarray to get the interval end. We also clip to the max subarray
        # size.
        sy2 = np.minimum(s[0] - ((point[0] + s[0]) - d[0]), s[0])
        sx1 = 0
        sx2 = np.minimum(s[1] - ((point[1] + s[1]) - d[1]), s[1])
    elif pivot == 'center':
        if s[0] % 2 == 0 or s[1] % 2 == 0:
            raise ValueError('Case of uneven size of subarray not yet implemented. '
                             'There is no distinct center point of the image.')
        # amount of pixels from the center to the border
        yh = int((s[0] - 1) / 2)
        # clip to min index, i.e. zero
        y1 = np.maximum(point[0] - yh, 0)
        # clip to max destination array size
        y2 = np.minimum(point[0] + yh + 1, d[0])
        xh = int((s[1] - 1) / 2)
        x1 = np.maximum(point[1] - xh, 0)
        x2 = np.minimum(point[1] + xh + 1, d[1])

        # if we run out of bounds at the start of the interval, (offset[0] - yh) will be negative meaning that we need
        # to clip the subarray with the absolute value of (offset[0] - yh).
        sy1 = np.abs(np.minimum(point[0] - yh, 0))
        # ((offset[0] + yh + 1) - d[0]) is the size of the part of the subarray that ran out of bounds. Will be negative
        # if we did not run out of bounds.
        # Hence, we subtract it from the size of the subarray to get the interval end. We also clip to the max subarray
        # size.
        sy2 = np.minimum(s[0] - ((point[0] + yh + 1) - d[0]), s[0])

        sx1 = np.abs(np.minimum(point[1] - xh, 0))
        sx2 = np.minimum(s[1] - ((point[1] + yh + 1) - d[1]), s[1])
    else:
        raise ValueError('Invalid pivot mode: {}'.format(pivot))

    if subarray_mask is not None:
        dst_slice = dst[y1:y2, x1:x2, ...]
        sub_slice = subarray[sy1:sy2, sx1:sx2, ...]
        mask_slice = subarray_mask[sy1:sy2, sx1:sx2, ...]

        dst[y1:y2, x1:x2, ...] = (dst_slice * np.logical_not(mask_slice)) + (sub_slice * mask_slice)
    else:
        dst[y1:y2, x1:x2, ...] = subarray[sy1:sy2, sx1:sx2, ...]


def copy_to_if_nonzero(dst, src, mask_func=lambda x: x):
    """
    Copies source array to destination array at locations where
    mask_func(src) is non zero. By default mask_func is the identity.
    """
    mask = mask_func(src) == 0

    if len(mask.shape) != 2:
        raise ValueError('Mask resulting from mask_func(src) must be two dimensional')

    if len(dst.shape) == 3:
        mask = np.expand_dims(mask, axis=2)

    d = (dst * mask) + src
    np.copyto(dst=dst, src=d)


def argwhere_to_tuples(argwhere_array):
    """
    Converts the output locations array of np.argwhere(...) to a list of tuples.

    :param argwhere_array: Output of np.argwhere(...).
    :return: List of tuples, each tuple representing one argwhere position.
    """
    return [tuple(x) for x in argwhere_array]


def eld(arr: np.ndarray):
    """
    Syntactic sugar to make expanding the last dimension shorter.
    :param arr: The input array with shape [d_0, ..., d_n].
    :return: The input array with shape [d_0, ..., d_n, 1]
    """
    return np.expand_dims(arr, axis=-1)


def mld(arr: np.ndarray):
    """
    Syntactic sugar to make max projection along the last dimension shorter.
    :param arr: The input array with shape [d_0, ..., d_n].
    :return: The input array with shape [d_0, ..., d_n-1]
    """
    return np.max(arr, axis=-1)


def sld(arrs: List[np.ndarray]):
    """
    Syntactic sugar to make stacking in the last dimension shorter.
    :param arrs: The input arrays with shape [d_0, ..., d_n].
    :return: The input arrays stacked with shape [d_0, ..., d_n, len(arrs)]
    """
    return np.stack(arrs, axis=-1)


def usld(arr: np.ndarray, squeeze=True):
    """
    Syntactic sugar to make unstacking in the last dimension shorter.
    :param squeeze: Whether to remove the singular last dimension from the resulting arrays.
    :param arr: The input array with shape [d_0, ..., d_n].
    :return: A list of arrays with shape [d_0, ..., d_n-1] (or shape [d_0, ..., d_n-1, 1] if squeeze is False) of
    length d_n.
    """
    s = np.split(arr, arr.shape[-1], axis=-1)
    if squeeze:
        return [np.squeeze(x, axis=-1) for x in s]
    else:
        return s


def cld(arrs: List[np.ndarray]):
    """
    Syntactic sugar to make concatenation in the last dimension shorter.
    :param arrs: The input arrays with shape [d_0, ..., d_n].
    :return: The input array with shape [d_0, ..., d_n * len(arrs)]
    """
    return np.concatenate(arrs, axis=-1)


def repeat_and_concat(arr: np.ndarray, repeats, axis=-1):
    """
    Repeats the specified array repeats times and concatenates the resulting list at the specified axis.

    :param arr: The array to repeat.
    :param repeats: How often the array should be repeated.
    :param axis: The axis to use for concatenation.
    :return: Repeated array concatenated at specified dimension.
    """
    arrs = [arr] * repeats
    return np.concatenate(arrs, axis=axis)


def index_grid(shape):
    """
    Create a two dimensional index grid with specified shape with 'ij' indexing.

    :param shape: Shape tuple/list specifying height and width.
    :return: Index array of shape [height, width].
    """
    if len(shape) != 2:
        raise ValueError('Shape must be 2-tuple: (height, width)')

    return np.stack(np.meshgrid(range(shape[0]), range(shape[1]), indexing='ij'), axis=-1)


def multitask_argmax(arr: np.ndarray, channels_per_task: int):
    """
    Applies np.argmax to grouped channels of the given array and returns the stacked result.

    :param arr: Array with shape [height, width, channels]
    :param channels_per_task: The number of consecutive channels to group. Meaning the given array will be split into
    groups of this size.
    :return: Stacked result of np.argmax applied to groups of channels.
    """
    arr_shape = arr.shape
    if len(arr_shape) != 3:
        raise ValueError('Given array must be three dimensional.')
    if arr_shape[-1] % channels_per_task != 0:
        raise ValueError('The number of channels of the given array must be divisible by the number of channels per'
                         'task.')

    tasks = []
    for i in range(0, arr_shape[-1], channels_per_task):
        sub = arr[..., i:i + channels_per_task]
        tasks.append(np.argmax(sub, axis=-1))
    return np.stack(tasks, axis=-1)


def resample_2d(arr: np.ndarray, locs: List[tuple], order=1):
    """
    Resampele the specified array at specified locations.

    :param arr: The array to resample of shape [height, width].
    :param locs: List of resample location tuples.
    :param order: Interpolation order.
    :return: Resampled values of the specified array at specified locations.
    """
    if len(arr.shape) != 2:
        raise ValueError('Specified array must be two dimensional.')

    ii = np.arange(arr.shape[0])
    jj = np.arange(arr.shape[1])

    interp = RectBivariateSpline(x=ii, y=jj, z=arr, kx=order, ky=order)

    np_locs = np.array(locs)
    return interp.ev(np_locs[:, 0], np_locs[:, 1])


def resample_2d_channelwise(arr: np.ndarray, locs: List[tuple], order=1):
    """
    Resampele the specified array at specified locations channelwise. Resampling will be done for each channel
    independently.

    :param arr: The array to resample of shape [height, width, channels].
    :param locs: List of resample location tuples.
    :param order: Interpolation order.
    :return: Resampled values of the specified array at specified locations.
    """
    if len(arr.shape) != 3:
        raise ValueError('Specified array must be three dimensional.')

    vals = []
    for i in range(arr.shape[2]):
        sub_arr = arr[..., i]
        vals.append(resample_2d(sub_arr, locs, order=order))

    return sld(vals)

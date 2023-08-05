import numpy as np


def precision_from_confusion(matrix, sparse_class_index):
    c = matrix
    i = sparse_class_index
    predicted_trues = np.sum(c[i, :])
    if predicted_trues == 0:
        return 0
    return c[i, i] / predicted_trues


def recall_from_confusion(matrix, sparse_class_index):
    c = matrix
    i = sparse_class_index
    condition_trues = np.sum(c[:, i])
    if condition_trues == 0:
        return 0
    return c[i, i] / condition_trues


def f1_from_confusion(matrix, sparse_class_index):
    p = precision_from_confusion(matrix, sparse_class_index)
    r = recall_from_confusion(matrix, sparse_class_index)

    if p == 0 or r == 0:
        return 0

    return (2 * p * r) / (p + r)


def accuracy_from_confusion(matrix):
    return np.trace(matrix) / np.sum(matrix)


def IoU_from_confusion(matrix, sparse_class_index):
    c = matrix
    i = sparse_class_index
    tp = c[i, i]
    fp = np.sum(c[i, :]) - tp
    fn = np.sum(c[:, i]) - tp

    tp_fp_fn = tp + fp + fn

    if tp_fp_fn == 0:
        return 0

    return tp / tp_fp_fn


def confusion_from_binary_matrix(gt, pred):
    inter = np.logical_and(gt, pred)
    tp = np.sum(inter)
    diff = pred - gt
    fp = np.sum(diff == 1)
    fn = np.sum(diff == -1)
    tn = np.sum((diff + inter) == 0)

    assert (tp + fp + fn + tn) == int(np.prod(gt.shape))

    return np.array([[tp, fp],
                     [fn, tn]])


def IoU_from_binary_matrix(gt, pred):
    intersection = np.logical_and(gt, pred)
    union = np.logical_or(gt, pred)

    return np.sum(intersection) / np.sum(union)

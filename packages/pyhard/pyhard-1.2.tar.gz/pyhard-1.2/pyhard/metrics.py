import numpy as np


def logloss(y_true: np.ndarray, y_pred: np.ndarray, eps=1e-15):
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.sum(y_true * np.log(y_pred), axis=1)


def brier(y_true: np.ndarray, y_pred: np.ndarray):
    return np.sum((y_pred - y_true) ** 2, axis=1)

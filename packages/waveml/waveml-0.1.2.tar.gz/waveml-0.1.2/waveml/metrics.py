import torch


def RMSE(y_true, y_pred):
    error = torch.sqrt(torch.mean((y_true - y_pred) ** 2))
    return error


def MSE(y_true, y_pred):
    error = torch.mean((y_true - y_pred) ** 2)
    return error


def MAE(y_true, y_pred):
    error = torch.mean(torch.abs(y_true - y_pred))
    return error


def MAPE(y_true, y_pred):
    error = torch.mean(torch.abs((y_true - y_pred) / y_true))
    return error

import numpy as np
from sklearn.metrics import mean_squared_error


def root_mean_squared_error(y_true, y_pred) -> float:
    """
    Root Mean Squared Error (RMSE)

    Primary evaluation metric for all regression models.
    """
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))

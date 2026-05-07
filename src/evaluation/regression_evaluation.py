from sklearn.metrics import mean_squared_error, r2_score
import numpy as np


def evaluate_regression_models(x_test, y_test, model):

    y_pred = model.predict(x_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"MSE: {mse:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")

    return mse, rmse, r2




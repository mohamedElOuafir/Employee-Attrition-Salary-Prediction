import os

import joblib
import pandas as pd
from predictors.dto.Employee import SalaryPredictionResponse, SalaryEmployee


REGRESSION_MODEL = "models/regression/best_regression_model.pkl"


attrition_regression_model = joblib.load(REGRESSION_MODEL)

def predict_salary(employee : SalaryEmployee):
    df_employee = pd.DataFrame([employee.__dict__])
    print(df_employee.to_string())


    predicted_salary = attrition_regression_model.predict(df_employee)[0]

    salary_prediction_response = SalaryPredictionResponse(predicted_salary)

    return salary_prediction_response


CLASSIFICATION_MODEL = "models/classification/best_classification_model.pkl"

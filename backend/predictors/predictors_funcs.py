import joblib
import pandas as pd
from predictors.dto.Employee import SalaryPredictionResponse, SalaryEmployee, AttritionEmployee, \
    AttritionPredictionResponse

REGRESSION_MODEL = "models/regression/best_regression_model.pkl"
attrition_regression_model = joblib.load(REGRESSION_MODEL)

def predict_salary(employee : SalaryEmployee):
    df_employee = pd.DataFrame([employee.__dict__])
    print(df_employee.to_string())


    predicted_salary = attrition_regression_model.predict(df_employee)[0]

    salary_prediction_response = SalaryPredictionResponse(predicted_salary)

    return salary_prediction_response




CLASSIFICATION_MODEL = "models/classification/best_classification_model.pkl"
attrition_classification_model = joblib.load(CLASSIFICATION_MODEL)

def predict_attrition(employee : AttritionEmployee):
    df_employee = pd.DataFrame([employee.__dict__])
    print(df_employee.to_string())


    predicted_attrition = int(attrition_classification_model.predict(df_employee)[0])
    print(predicted_attrition)
    prediction_label = 'Yes' if predicted_attrition == 1 else 'No'

    attrition_prediction_response = AttritionPredictionResponse(predicted_attrition, prediction_label)

    return attrition_prediction_response
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

regression_models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(),
    'Random Forest': RandomForestRegressor(),
    'XGBoost': XGBRegressor(),
}


def train_regression_base_model(x_train, y_train, binary_transformer, preprocessor):

    trained_models = {}


    for name, model in regression_models.items():
        print(f"Training with model :{name}...")

        pipeline = Pipeline([
            ("binary", binary_transformer),
            ("preprocessing", preprocessor),
            ("model", model)
        ])

        pipeline.fit(x_train, y_train)
        trained_models[name] = pipeline

    return trained_models



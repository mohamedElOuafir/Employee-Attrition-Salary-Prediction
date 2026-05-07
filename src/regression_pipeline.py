import os
import joblib
import numpy as np
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from src.data.load_data import load_data
from src.data.pre_processing import clean_data
from src.evaluation.regression_evaluation import evaluate_regression_models
from src.features.features_engineering import (
    one_hot_encoding_categorical_features,
    label_encoding_categorical_features_2,
    split_data_regression, binary_encoding_categorical_features, binary_map,
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from src.training.training_regression import train_regression_base_model
from src.visualisation.visualisation import plot_correlation_with_target, plot_regression_metrics


# =============================================================================
# CONFIGURATION
# =============================================================================

DATA_PATH = "../data/raw/IBM_HR_Employee_Attrition.csv"
MODEL_SAVE_DIR = "../models/regression"
BEST_MODEL_PATH = os.path.join(MODEL_SAVE_DIR, "best_regression_model.pkl")
TARGET_COLUMN = "MonthlyIncome"
RANDOM_STATE = 42

os.makedirs(MODEL_SAVE_DIR, exist_ok=True)

CATEGORICAL_FEATURES = [
    "BusinessTravel",
    "Department",
    "MaritalStatus",
    "JobRole",
    "EducationField",
    "Attrition",
    "OverTime",
    "Gender",
]

CATEGORICAL_FEATURES_ONE_HOT = [
    "BusinessTravel",
    "Department",
    "MaritalStatus",
    "JobRole",
    "EducationField",
]

CATEGORICAL_FEATURES_BINARY = [
    "Attrition",
    "OverTime",
    "Gender",
]

NUMERIC_FEATURES = [
    "Age",
    "DistanceFromHome",
    "NumCompaniesWorked",
    "PercentSalaryHike",
    "TotalWorkingYears",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
]

BINARY_MAP = {"Yes": 1, "No": 0, "Male": 1, "Female": 0}

EVALUATION_METRICS = ["mse", "rmse", "r2"]

# Hyperparameter search spaces per model (keys must match train_regression_base_model output)
# For regression, scoring is negative because sklearn minimizes by convention
HYPERPARAMETER_GRIDS = {
    "Linear Regression": {},

    "Decision Tree": {
        "model__max_depth": [None, 5, 10, 20, 30],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__criterion": ["squared_error", "absolute_error"],
    },

    "Random Forest": {
        "model__n_estimators": [100, 200, 300],
        "model__max_depth": [None, 5, 10, 20],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
    },


    "XGBoost": {
        "model__n_estimators": [100, 200, 300, 500],
        "model__learning_rate": [0.01, 0.05, 0.1, 0.2],
        "model__max_depth": [3, 5, 7, 9],
        "model__subsample": [0.6, 0.8, 1.0],
        "model__colsample_bytree": [0.6, 0.8, 1.0],
        "model__gamma": [0, 0.1, 0.3, 0.5],
        "model__reg_alpha": [0, 0.1, 1.0],
        "model__reg_lambda": [0.5, 1.0, 2.0],
    },
}



# =============================================================================
# PHASE 1 — DATA LOADING
# =============================================================================

print("=" * 60)
print("PHASE 1 — DATA LOADING")
print("=" * 60)

print("Loading data...")
df_employee_attrition = load_data(DATA_PATH)
print(f"Dataset loaded: {df_employee_attrition.shape[0]} rows, {df_employee_attrition.shape[1]} columns.\n")


# =============================================================================
# PHASE 2 — PRE-PROCESSING
# =============================================================================

print("=" * 60)
print("PHASE 2 — PRE-PROCESSING")
print("=" * 60)

# Cleaning the dataset
print("Cleaning data...")
df_employee_attrition, column_with_outliers = clean_data(df_employee_attrition)
print(f"Columns with detected outliers: {column_with_outliers}\n")

# Optional: Visualisation of distributions and outliers
# plot_distribution_categorical_features(df_employee_attrition, CATEGORICAL_FEATURES_ONE_HOT + CATEGORICAL_FEATURES_BINARY)
# plot_distribution_categorical_features(df_employee_attrition, CATEGORICAL_FEATURES_BINARY)
# plot_box_plots(df_employee_attrition, NUMERIC_FEATURES)

# Correlation matrix using label-encoded copy — for analysis only, not used in training
df_label_encoded = label_encoding_categorical_features_2(df_employee_attrition, CATEGORICAL_FEATURES)
# plot_correlation_matrix(df_label_encoded)
plot_correlation_with_target(df_label_encoded, TARGET_COLUMN)

# Encoding categorical variables
print("Encoding categorical features...")

# Binary encoding (Yes/No, Male/Female → 0/1)
df_employee_attrition = binary_encoding_categorical_features(df_employee_attrition, CATEGORICAL_FEATURES_BINARY, BINARY_MAP)

# Saving the binary encoding method
binary_transformer = FunctionTransformer(binary_map)

print("Binary encoding applied:")
print(df_employee_attrition[CATEGORICAL_FEATURES_BINARY].head())

# One-hot encoding for nominal multi-class features
"""df_employee_attrition = one_hot_encoding_categorical_features(
    df_employee_attrition, CATEGORICAL_FEATURES_ONE_HOT
)"""
print("\nOne-hot encoding applied. Updated columns:")
print(list(df_employee_attrition.columns))

# Saving the binary encoding method
preprocessor = ColumnTransformer(
    transformers=[
        ("onehot", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES_ONE_HOT),],
    remainder="passthrough"
)

# Splitting into train / test sets
print("\nSplitting data into train and test sets...")
x_train, x_test, y_train, y_test = split_data_regression(df_employee_attrition, NUMERIC_FEATURES)
print(f"Train size: {x_train.shape[0]} | Test size: {x_test.shape[0]}")
print(f"Features used: {list(x_train.columns)}\n")


# =============================================================================
# PHASE 3 — BASE MODEL TRAINING
# =============================================================================

print("=" * 60)
print("PHASE 3 — BASE MODEL TRAINING")
print("=" * 60)

print("Training base regression models (no tuning)...")
trained_regression_models = train_regression_base_model(x_train, y_train, binary_transformer, preprocessor)
print(f"Models trained: {list(trained_regression_models.keys())}\n")


# =============================================================================
# PHASE 4 — BASE MODEL EVALUATION
# =============================================================================

print("=" * 60)
print("PHASE 4 — BASE MODEL EVALUATION")
print("=" * 60)

models_names = []
mse_scores, rmse_scores, r2_scores = [], [], []

for name, model in trained_regression_models.items():
    print(f"Evaluating: {name}...")
    mse, rmse, r2 = evaluate_regression_models(x_test, y_test, model)

    models_names.append(name)
    mse_scores.append(mse)
    rmse_scores.append(rmse)
    r2_scores.append(r2)


base_metrics_values = [mse_scores, rmse_scores, r2_scores]

# Visualise base model metrics
plot_regression_metrics(EVALUATION_METRICS, models_names, base_metrics_values)

print("\nBase model evaluation complete.\n")


# =============================================================================
# PHASE 5 — HYPERPARAMETER TUNING
# =============================================================================

print("=" * 60)
print("PHASE 5 — HYPERPARAMETER TUNING")
print("=" * 60)

tuned_models = {}
tuned_models_names = []
tuned_mse, tuned_rmse, tuned_r2 = [], [], []

for name, model in trained_regression_models.items():
    print(f"\nTuning: {name}...")

    param_grid = HYPERPARAMETER_GRIDS.get(name)

    # Skip models with no defined grid or empty grid (e.g. Linear Regression)
    if param_grid is None or len(param_grid) == 0:
        print(f"  No hyperparameter grid defined for '{name}'. Keeping base model.")
        tuned_models[name] = model
        continue

    # Use RandomizedSearchCV for large grids, GridSearchCV for smaller ones
    total_combinations = np.prod([len(v) for v in param_grid.values()])
    print(f"  Search space size: {total_combinations} combinations.")

    if total_combinations > 50:
        print(f"  Using RandomizedSearchCV (n_iter={20})...")
        search = RandomizedSearchCV(
            estimator=model,
            param_distributions=param_grid,
            n_iter=20,
            scoring="r2",
            cv=5,
            n_jobs=-1,
            random_state=RANDOM_STATE,
            verbose=0,
        )
    else:
        print(f"  Using GridSearchCV...")
        search = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            scoring="r2",
            cv=5,
            n_jobs=-1,
            verbose=0,
        )

    search.fit(x_train, y_train)
    best_model = search.best_estimator_
    tuned_models[name] = best_model

    print(f"  Best params   : {search.best_params_}")
    print(f"  Best CV R²    : {search.best_score_:.4f}")

    # Evaluate tuned model on the test set
    mse, rmse, r2 = evaluate_regression_models(x_test, y_test, best_model)

    tuned_models_names.append(name)
    tuned_mse.append(mse)
    tuned_rmse.append(rmse)
    tuned_r2.append(r2)

    print(f"  Tuned — MSE={mse:.4f} | RMSE={rmse:.4f} | R²={r2:.4f}")

tuned_metrics_values = [tuned_mse, tuned_rmse, tuned_r2]

# Visualise tuned model metrics
plot_regression_metrics(EVALUATION_METRICS, tuned_models_names, tuned_metrics_values)

print("\nHyperparameter tuning complete.\n")


# =============================================================================
# PHASE 6 — BEST MODEL SELECTION & SAVING
# =============================================================================

print("=" * 60)
print("PHASE 6 — BEST MODEL SELECTION & SAVING")
print("=" * 60)

# Select the best model based on R² score (higher is better)
best_index = int(np.argmax(tuned_r2))
best_model_name = tuned_models_names[best_index]
best_model = tuned_models[best_model_name]

print(f"\nBest model : {best_model_name}")
print(f"  R²   : {tuned_r2[best_index]:.4f}")
print(f"  MSE  : {tuned_mse[best_index]:.4f}")
print(f"  RMSE : {tuned_rmse[best_index]:.4f}")

# Save the best model to disk
print(f"\nSaving best model to '{BEST_MODEL_PATH}'...")
joblib.dump(best_model, BEST_MODEL_PATH)
print("Best model saved successfully.")

# Save all tuned models individually
for name, model in tuned_models.items():
    safe_name = name.replace(" ", "_").lower()
    model_path = os.path.join(MODEL_SAVE_DIR, f"{safe_name}_regression_tuned.pkl")
    joblib.dump(model, model_path)
    print(f"  Saved: {model_path}")

print("\nAll tuned models saved.\n")


# =============================================================================
# PHASE 7 — INFERENCE TEST
# =============================================================================

print("=" * 60)
print("PHASE 7 — INFERENCE TEST")
print("=" * 60)

print("Loading best model from disk and running predictions on test set...")
loaded_model = joblib.load(BEST_MODEL_PATH)
sample_predictions = loaded_model.predict(x_test[:5])
print(f"Sample predictions (first 5 test samples): {np.round(sample_predictions, 2)}")
print(f"Actual values                             : {list(np.round(y_test[:5], 2))}")

print("\nPipeline for regression has terminated successfully!")
import os
import joblib
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder

from src.data.load_data import load_data
from src.data.pre_processing import clean_data
from src.evaluation.classification_evaluation import evaluate_classification_models
from src.features.features_engineering import (
    one_hot_encoding_categorical_features,
    split_data_classification,
    label_encoding_categorical_features_2,
    apply_smote_techniques,
    binary_encoding_categorical_features, binary_map,
)
from src.training.training_classification import train_classification_base_model
from src.visualisation.visualisation import plot_classification_metrics, plot_confusion_matrix, \
    plot_correlation_with_target

# =============================================================================
# CONFIGURATION
# =============================================================================

DATA_PATH = "../data/raw/IBM_HR_Employee_Attrition.csv"
MODEL_SAVE_DIR = "../models/classification"
BEST_MODEL_PATH = os.path.join(MODEL_SAVE_DIR, "best_classification_model.pkl")
TARGET_COLUMN = "Attrition"
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

EVALUATION_METRICS = ["accuracy", "recall", "precision", "f1", "roc_auc"]

# Hyperparameter search spaces per model (keys must match train_classification_base_model output)
HYPERPARAMETER_GRIDS = {
    "Logistic Regression": {
        "model__C": [0.01, 0.1, 1, 10, 100],
        "model__solver": ["lbfgs", "liblinear"],
        "model__max_iter": [1000, 2000, 3000, 4000],
    },
    "Random Forest": {
        "model__n_estimators": [100, 200, 300],
        "model__max_depth": [None, 5, 10, 20],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
    },
    "Decision Tree": {
        "model__max_depth": [None, 5, 10, 20],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__criterion": ["gini", "entropy"],
    },
    "Naive Bayes": {
        "model__var_smoothing": [1e-11, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5],
    },
    "XGBoost": {
        "model__n_estimators":     [100, 200, 300, 500],
        "model__learning_rate":    [0.01, 0.05, 0.1, 0.2],
        "model__max_depth":        [3, 5, 7, 9],
        "model__subsample":        [0.6, 0.8, 1.0],
        "model__colsample_bytree": [0.6, 0.8, 1.0],
        "model__gamma":            [0, 0.1, 0.3, 0.5],
        "model__reg_alpha":        [0, 0.1, 1.0],       # L1 regularization
        "model__reg_lambda":       [0.5, 1.0, 2.0],     # L2 regularization
        "model__scale_pos_weight": [1, 3, 5],
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

# Optional: Visualisation of distributions and correlation
# plot_distribution_categorical_features(df_employee_attrition, CATEGORICAL_FEATURES_ONE_HOT + CATEGORICAL_FEATURES_BINARY)
# plot_distribution_categorical_features(df_employee_attrition, CATEGORICAL_FEATURES_BINARY)
# plot_box_plots(df_employee_attrition, NUMERIC_FEATURES)

# Correlation matrix using label-encoded copy for analysis only
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
x_train, x_test, y_train, y_test = split_data_classification(
    df_employee_attrition, TARGET_COLUMN, NUMERIC_FEATURES
)
print(f"Train size: {x_train.shape[0]} | Test size: {x_test.shape[0]}\n")

# Handling class imbalance with SMOTE
print("Applying SMOTE to balance the training set...")
x_train, y_train = apply_smote_techniques(x_train, y_train)
print(f"Post-SMOTE train size: {x_train.shape[0]}\n")


# =============================================================================
# PHASE 3 — BASE MODEL TRAINING
# =============================================================================

print("=" * 60)
print("PHASE 3 — BASE MODEL TRAINING")
print("=" * 60)

print("Training base classification models (no tuning)...")
trained_classification_models = train_classification_base_model(x_train, y_train, binary_transformer, preprocessor)
print(f"Models trained: {list(trained_classification_models.keys())}\n")

classes = list(trained_classification_models.values())[0].classes_


# =============================================================================
# PHASE 4 — BASE MODEL EVALUATION
# =============================================================================

print("=" * 60)
print("PHASE 4 — BASE MODEL EVALUATION")
print("=" * 60)

models_names = []
accuracy_scores, recall_scores, precision_scores, f1_scores, roc_auc_scores = [], [], [], [], []
confusion_matrices = []

for name, model in trained_classification_models.items():
    print(f"Evaluating: {name}...")
    accuracy, recall, precision, f1, roc_auc, cm = evaluate_classification_models(x_test, y_test, model)

    models_names.append(name)
    accuracy_scores.append(accuracy)
    recall_scores.append(recall)
    precision_scores.append(precision)
    f1_scores.append(f1)
    roc_auc_scores.append(roc_auc)
    confusion_matrices.append(cm)


base_metrics_values = [accuracy_scores, recall_scores, precision_scores, f1_scores, roc_auc_scores]

# Visualise base model metrics
plot_classification_metrics(EVALUATION_METRICS, models_names, base_metrics_values)
plot_confusion_matrix(confusion_matrices, classes, models_names)

print("\nBase model evaluation complete.\n")


# =============================================================================
# PHASE 5 — HYPERPARAMETER TUNING
# =============================================================================

print("=" * 60)
print("PHASE 5 — HYPERPARAMETER TUNING")
print("=" * 60)

tuned_models = {}
tuned_models_names = []
tuned_accuracy, tuned_recall, tuned_precision, tuned_f1, tuned_roc_auc = [], [], [], [], []
tuned_cms = []

for name, model in trained_classification_models.items():
    print(f"\nTuning: {name}...")

    param_grid = HYPERPARAMETER_GRIDS.get(name)

    if param_grid is None:
        print(f"  No hyperparameter grid defined for '{name}'. Skipping tuning.")
        tuned_models[name] = model
        continue

    # Use RandomizedSearchCV for large grids, GridSearchCV for smaller ones
    total_combinations = np.prod([len(v) for v in param_grid.values()])
    print(f"  Search space size: {total_combinations} combinations.")

    if total_combinations > 50:
        print(f"  Using RandomizedSearchCV (n_iter=50)...")
        search = RandomizedSearchCV(
            estimator=model,
            param_distributions=param_grid,
            n_iter=50,
            scoring="roc_auc",
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
            scoring="roc_auc",
            cv=5,
            n_jobs=-1,
            verbose=0,
        )

    search.fit(x_train, y_train)
    best_model = search.best_estimator_
    tuned_models[name] = best_model

    print(f"  Best params: {search.best_params_}")
    print(f"  Best CV f1 score: {search.best_score_:.4f}")

    # Evaluate tuned model on test set
    accuracy, recall, precision, f1, roc_auc, cm = evaluate_classification_models(x_test, y_test, best_model)

    tuned_models_names.append(name)
    tuned_accuracy.append(accuracy)
    tuned_recall.append(recall)
    tuned_precision.append(precision)
    tuned_f1.append(f1)
    tuned_roc_auc.append(roc_auc)
    tuned_cms.append(cm)

    print(f"  Tuned — Accuracy={accuracy:.4f} | Recall={recall:.4f} | Precision={precision:.4f} | F1={f1:.4f} | ROC-AUC={roc_auc:.4f}")

tuned_metrics_values = [tuned_accuracy, tuned_recall, tuned_precision, tuned_f1, tuned_roc_auc]

# Visualise tuned model metrics
plot_classification_metrics(EVALUATION_METRICS, tuned_models_names, tuned_metrics_values)
plot_confusion_matrix(tuned_cms, classes, tuned_models_names)

print("\nHyperparameter tuning complete.\n")


# =============================================================================
# PHASE 6 — BEST MODEL SELECTION & SAVING
# =============================================================================

print("=" * 60)
print("PHASE 6 — BEST MODEL SELECTION & SAVING")
print("=" * 60)

# Select the best model based on F1 score (primary metric for imbalanced classification)
best_index = int(np.argmax(tuned_f1))
best_model_name = tuned_models_names[best_index]
best_model = tuned_models[best_model_name]

print(f"\nBest model: {best_model_name}")
print(f"  F1 Score  : {tuned_f1[best_index]:.4f}")
print(f"  Accuracy  : {tuned_accuracy[best_index]:.4f}")
print(f"  Recall    : {tuned_recall[best_index]:.4f}")
print(f"  Precision : {tuned_precision[best_index]:.4f}")
print(f"  ROC-AUC   : {tuned_roc_auc[best_index]:.4f}")

# Save the best model to disk
print(f"\nSaving best model to '{BEST_MODEL_PATH}'...")
joblib.dump(best_model, BEST_MODEL_PATH)
print("Best model saved successfully.")

# Also save all tuned models individually
for name, model in tuned_models.items():
    safe_name = name.replace(" ", "_").lower()
    model_path = os.path.join(MODEL_SAVE_DIR, f"{safe_name}_tuned.pkl")
    joblib.dump(model, model_path)
    print(f"  Saved: {model_path}")

print("\nAll tuned models saved.\n")


# =============================================================================
# PHASE 7 — INFERENCE TEST (optional smoke test)
# =============================================================================

print("=" * 60)
print("PHASE 7 — INFERENCE TEST")
print("=" * 60)

print("Loading best model from disk and running predictions on test set...")
loaded_model = joblib.load(BEST_MODEL_PATH)
sample_predictions = loaded_model.predict(x_test[:10])
print(f"Sample predictions (first 5 test samples): {sample_predictions}")
print(f"Actual labels                             : {list(y_test[:10])}")

print("\nPipeline for classification has terminated successfully!")
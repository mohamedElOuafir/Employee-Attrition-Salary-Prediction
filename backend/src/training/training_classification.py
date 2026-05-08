from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
import numpy as np

classification_models = {
    'Logistic Regression': LogisticRegression(max_iter=2000, class_weight='balanced'),
    'Decision Tree': DecisionTreeClassifier(random_state=42, class_weight='balanced'),
    'Random Forest': RandomForestClassifier(n_estimators=200 ,random_state=42, class_weight='balanced'),
    'Naive Bayes': GaussianNB(),
}


def train_classification_base_model(x_train, y_train, binary_transformer, preprocessor):

    rate = float(np.sum(y_train == 0)) / np.sum(y_train == 1)
    classification_models.update({'XGBoost' : XGBClassifier(random_state=42, scale_pos_weight=rate)})

    trained_models = {}

    for name, model in classification_models.items():
        print(f"Training with model :{name}...")

        pipeline = Pipeline([
            ("binary", binary_transformer),
            ("preprocessing", preprocessor),
            ("model", model)
        ])

        pipeline.fit(x_train, y_train)
        trained_models[name] = pipeline

    return trained_models



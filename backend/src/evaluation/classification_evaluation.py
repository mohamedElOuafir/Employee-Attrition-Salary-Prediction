import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix, \
    classification_report, roc_auc_score, precision_recall_curve


def evaluate_classification_models(x_test, y_test, model):

    y_prob= model.predict_proba(x_test)[:,1]

    precisions, recalls, thresholds = precision_recall_curve(y_test, y_prob)
    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
    best_idx = f1_scores.argmax()
    best_threshold = thresholds[best_idx]

    print(f"Meilleur seuil : {best_threshold:.3f}")

    # Prédiction avec le nouveau seuil
    y_pred = (y_prob >= best_threshold).astype(int)

    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)

    print(
        f"accuracy: {accuracy:.4f}, recall: {recall:.4f}, precision: {precision:.4f}, f1: {f1:.4f}, roc_auc: {roc_auc:.4f}\n"
    )

    return accuracy, recall, precision, f1, roc_auc, matrix



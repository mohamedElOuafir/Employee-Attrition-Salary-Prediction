import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import ConfusionMatrixDisplay
import math


def plot_distribution_categorical_features(df, columns):
    n = math.ceil(len(columns) / 2)
    fig, axes = plt.subplots(2, n, figsize=(12, 8))
    axes = axes.flatten()

    for i, column in enumerate(columns):
        counts = df[column].value_counts()
        axes[i].bar(counts.index, counts.values)
        axes[i].set_title(column)

    plt.tight_layout()
    plt.show()


def plot_box_plots(df, columns):
    dim = math.ceil(len(columns) / 4)
    fig, axes = plt.subplots(4, dim, figsize=(12, 8))
    axes = axes.flatten()

    for i, column in enumerate(columns):
        axes[i].boxplot(df[column])
        axes[i].set_title(column)

    plt.tight_layout()
    plt.show()



def plot_classification_metrics(metrics, models, metric_values):
    plt.figure(figsize=(10, 6))
    i = 0
    for metric in metrics:
        plt.subplot(2, 3, i + 1)
        plt.bar(models, metric_values[i])
        plt.title(metric)
        i = i + 1
    plt.show()



def plot_regression_metrics(metrics, models, metric_values):
    plt.figure(figsize=(10, 6))
    i = 0
    for metric in metrics:
        plt.subplot(2, 3, i + 1)
        plt.bar(models, metric_values[i])
        plt.title(metric)
        i = i + 1
    plt.show()



def plot_confusion_matrix(cms, classes, models):

    fig, axes = plt.subplots(3, 2, figsize=(12, 15))
    axes = axes.flatten()

    for i, cm in enumerate(cms):
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)

        disp.plot(cmap='Blues', colorbar=False, ax=axes[i])
        axes[i].set_title(f"Modèle {models[i]}")

    plt.tight_layout()
    plt.show()


def plot_correlation_matrix(df):
    corr = df.corr()
    plt.figure(figsize=(24,20))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.show()

def plot_correlation_with_target(df, target):
    corr = df.corr()[target]
    plt.figure(figsize=(10, 10))
    sns.heatmap(corr.to_frame(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.show()
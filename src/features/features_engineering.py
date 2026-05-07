import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import TargetEncoder, LabelEncoder, StandardScaler, OneHotEncoder
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN

def binary_encoding_categorical_features(df, columns, binary):
    for column in columns:
        df[column] = df[column].replace(binary)

    return df

def binary_map(df):
    df = df.copy()
    BINARY_MAP = {"Yes": 1, "No": 0, "Male": 1, "Female": 0}
    CATEGORICAL_FEATURES_BINARY = ["OverTime", "Gender"]

    for col in CATEGORICAL_FEATURES_BINARY:
        df[col] = df[col].map(BINARY_MAP).fillna(0)

    return df




def label_encoding_categorical_features(x_train, x_val, x_test, columns):
    # Label Encoding
    label_encoder = LabelEncoder()

    for col in columns:
        x_train[col] = label_encoder.fit_transform(x_train[col])
        x_val[col] = label_encoder.fit_transform(x_val[col])
        x_test[col] = label_encoder.fit_transform(x_test[col])

    return x_train, x_val, x_test


def label_encoding_categorical_features_2(df, columns):
    # Label Encoding
    label_encoder = LabelEncoder()

    for col in columns:
        df[col] = label_encoder.fit_transform(df[col])

    return df


def one_hot_encoding_categorical_features(df, columns):

    # One-Hot Encoding
    encoder = OneHotEncoder(handle_unknown="ignore")
    encoded = encoder.fit_transform(df[columns])

    # convert to DataFrame
    encoded_df = pd.DataFrame(
        encoded.toarray(),
        columns=encoder.get_feature_names_out(columns)
    )
    # reset index for concatenation
    encoded_df.index = df.index

    # concat
    df_final = pd.concat([df.drop(columns=columns), encoded_df], axis=1)

    return df_final


def target_encoding_categorical_features(x_train, x_val, x_test, y_train, columns):

    # Target Encoding
    target_encoder = TargetEncoder()

    for col in columns:
        x_train[col] = target_encoder.fit_transform(
            x_train[[col]], y_train
        )
        x_val[col] = target_encoder.transform(x_val[[col]])
        x_test[col] = target_encoder.transform(x_test[[col]])


    return x_train, x_val, x_test, y_train


def apply_smote_techniques(x_train, y_train):

    print(f"\nBefore oversampling {y_train.value_counts()}\n")
    smote = SMOTE(random_state=42)
    #smote = SMOTEENN(random_state=42)
    x_train, y_train = smote.fit_resample(x_train, y_train)

    print(f"\nAfter oversampling {y_train.value_counts()}\n")

    return x_train, y_train



def split_data_classification(df, target, numerical_columns):

    x = df.drop(columns=[target])
    y = df[target]

    # Splitting data into train, validation and test data
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )


    # Standardizing numerical columns
    scaler = StandardScaler()
    x_train[numerical_columns] = scaler.fit_transform(x_train[numerical_columns])
    x_test[numerical_columns] = scaler.transform(x_test[numerical_columns])

    return x_train, x_test, y_train, y_test


def split_data_regression(df, numerical_columns):

    x = df.drop(columns=["Attrition", "MonthlyIncome"])
    y = df["MonthlyIncome"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    # Standardizing numerical columns
    scaler = StandardScaler()
    x_train[numerical_columns] = scaler.fit_transform(x_train[numerical_columns])
    x_test[numerical_columns] = scaler.transform(x_test[numerical_columns])

    return x_train, x_test, y_train, y_test



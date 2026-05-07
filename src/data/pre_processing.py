from src.visualisation.visualisation import plot_box_plots


def clean_data(df):
    # Colonnes inutiles
    columns_inutiles = [
        "EmployeeNumber",
        "StandardHours",
        "EmployeeCount",
        "Over18",
        "MonthlyRate",
        "DailyRate",
        "HourlyRate",
        "PerformanceRating",
    ]

    df = df.drop(columns=columns_inutiles)

    # Suppression des doublons
    df = df.drop_duplicates()


    # Elimination of outliers in numerical columns using the IQR method
    # Columns with outliers values
    columns_with_outliers = [
        "MonthlyIncome",
        "NumCompaniesWorked",
        "TotalWorkingYears",
        "YearsAtCompany",
        "YearsInCurrentRole",
        "YearsSinceLastPromotion",
        "YearsWithCurrManager"
    ]

    plot_box_plots(df, columns_with_outliers)

    return df, columns_with_outliers



def eliminate_outliers(df, columns):

    for column in columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        MAX_LIMIT = Q3 + 1.5 * IQR
        MIN_LIMIT = Q1 - 1.5 * IQR

        df[column] = df[column].clip(upper=MAX_LIMIT, lower=MIN_LIMIT)

    return df


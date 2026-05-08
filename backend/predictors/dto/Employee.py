from dataclasses import dataclass
from typing import Optional


@dataclass
class AttritionEmployee:
    Age: int
    BusinessTravel: str
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: float
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int



@dataclass
class SalaryEmployee:

    Age: int
    BusinessTravel: str
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int








@dataclass
class AttritionPredictionResponse:

    prediction: int
    prediction_label: str



@dataclass
class SalaryPredictionResponse:
    predicted_salary: float

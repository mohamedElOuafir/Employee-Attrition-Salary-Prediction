from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from predictors.dto.Employee import SalaryEmployee
from predictors.predictors_funcs import predict_salary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/salary/predict")
async def salary_predict(employee: SalaryEmployee):
    return predict_salary(employee)





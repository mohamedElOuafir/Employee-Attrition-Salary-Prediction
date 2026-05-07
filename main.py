import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.regression_salary_api:app", host="localhost", port=8000)
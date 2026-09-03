from fastapi import FastAPI, Request, HTTPException
from reports.report import generate_report
import time
from datetime import datetime
import json

app = FastAPI()

@app.middleware("http")
async def request_logger(request:Request, call_next):
    now = datetime.now()
    start = time.time()
    response = await call_next(request)
    end = time.time()
    response_time = round((end - start) * 1000,2)

    if response.status_code >=400:
        level = "ERROR"
    else:
        level = "INFO"

    log = {
        "timestamp":now.strftime("%d/%m/%Y, %H:%M:%S"),
        "level":level,
        "user_id":request.query_params.get("user_id"),
        "method":request.method,
        "endpoint":request.url.path,
        "status_code":response.status_code,
        "response_time":response_time
    }

    with open("logs.jsonl","a") as file:
        json.dump(log, file)
        file.write("\n")

    return response

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.get("/report")
def report():
    return generate_report()

@app.get("/login")
def login(user_id, success:bool = True):
    if success:
        return {"message":"login successful"}
    else:
        raise HTTPException(
            status_code=401,
            detail="login failed"
        )

@app.get("/search")
def search(user_id):
    time.sleep(2)
    return {"message": "search completed"}

@app.get("/products")
def products(user_id):
    return {"message":"products working"}

@app.get("/checkout")
def checkout(user_id, success:bool=True):
    if success:
        return {"message":"checkout successful"}
    else:
        raise HTTPException(
            status_code=500,
            detail="checkout service failed"
        )
@app.get("/payment")
def payment(user_id, success: bool=True):
    if success:
        return {"message":"payment successful"}
    else:
        raise HTTPException(
            status_code=500,
            detail="payment service failed"
        )
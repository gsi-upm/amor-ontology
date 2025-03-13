from typing import Annotated
from fastapi import Depends, FastAPI, Query
from fastapi.responses import RedirectResponse
from model import *

app = FastAPI()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/run")
def run(model: Experiment = Query(Experiment)):
    return model

@app.post("/run")
def run_post(model: Experiment):
    return {"msg": "Your experiment has been successfully run"}


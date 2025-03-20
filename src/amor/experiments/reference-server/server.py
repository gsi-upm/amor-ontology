from typing import Annotated
from fastapi import Depends, FastAPI, Query, Form
from fastapi.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi
from model import *
from pydantic import BaseModel
from pathlib import Path

import os
import json

db_path = Path("db")


os.makedirs(db_path, exist_ok=True)

def type_path(objtype: type):
    dirpath = db_path / objtype.__name__
    return dirpath

def obj_path(objtype: type, id: str):
    dirpath = type_path(objtype)
    return dirpath / id + ".json"

def load_object(objtype: type, id: str):
    fpath = obj_path(objtype, id)
    if not fpath.exists():
        return None
    with open(fpath) as f:
        return json.load(f)

def save_object(obj, id: str = None):
    id = id or new_id()
    fpath = obj_path(type(obj), id)
    with open(fpath, 'w') as f:
        json.dump(obj, f)


def list_objects(objtype: type):
    folder = type_path(objtype)
    objs = []
    if folder.exists():
        for fpath in folder.glob("*.json"):
            with open(fpath) as f:
                obj = json.load(f)
                objs.append(obj)
    return objs


app = FastAPI(
        description="This is a barebones service that shows how the Pydantic model of the experiments can be turned into a REST API that can be used to comfortably launch experiments in remote executors.",
        title="AMOR Experiments Reference Implementation"
              )


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/subjects/", tags=["subjects"])
def list_subjects() -> List[ExperimentationSubject]:
    """Get a list of available experiment subjects"""
    return list_objects(ExperimentationSubject)

@app.get("/subjects/form", include_in_schema=False, tags=["subjects"])
def new_subject():
    return ""

@app.post("/subjects/{id}", tags=["subjects"])
def subjects_post(id: str, subject: ExperimentationSubject = Form(ExperimentationSubject)):
    """
    Modify an existing subject
    """
    save_obj(subject, id)

@app.post("/subjects/", tags=["subjects"])
def post_subject(subject: ExperimentationSubject = Form(ExperimentationSubject)):
    save_obj(subject, id=None)

@app.put("/subjects/", tags=["subjects"])
def put_subject(subject: ExperimentationSubject):
    return ""

@app.get("/experiments/run", tags=["experiments"])
def experiments_query(config: Experiment = Query(Experiment)):
    """
    Run an experiment from an experiment configuration (GET)
    """
    return experiments_post(config)

@app.get("/evaluation/", tags=["evaluation"])
def evaluation_list():
    """
    Run an experiment from an experiment configuration (GET)
    """
    return []

@app.post("/evaluation/", tags=["evaluation"])
def evaluation_list(config: ExperimentEvaluation = Query(ExperimentEvaluation)):
    return "evaluation added"

@app.post("/experiments/form", tags=["experiments"])
def experiments_post(config: Experiment = Form(Experiment)):
    """
    Run an experiment from an experiment configuration (POST Form)
    """
    thisid = new_id()
    print("New id is:", thisid)
    exp = Experiment(id=thisid,**config.dict())
    return exp

@app.post("/experiments/run",
          tags=["experiments"])
def run_post(config: Experiment):
    """
    Run an experiment sent as a complete JSON object
    """
    thisid = new_id()
    print("New id is:", thisid)
    exp = Experiment(id=thisid,**config.dict())
    return exp


#def custom_openapi():
#    if app.openapi_schema:
#        return app.openapi_schema
#    openapi_schema = get_openapi(
#        title="Custom title",
#        version="2.5.0",
#        summary="This is a very custom OpenAPI schema",
#        description="Here's a longer description of the custom **OpenAPI** schema",
#        routes=app.routes,
#    )
#    openapi_schema["info"]["x-logo"] = {
#        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
#    }
#    app.openapi_schema = openapi_schema
#    return app.openapi_schema
#

#app.openapi = custom_openapi

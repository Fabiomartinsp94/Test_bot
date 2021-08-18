from fastapi import FastAPI
from services.rpa import rpa
import json
from fastapi import APIRouter



router = APIRouter()

@router.get("/results")
def results():

    with open(r'files/lenovo.json', 'r') as f:
        response = json.load(f)

    return response

@router.get("/")
def run_bot():

    rpa()

    return "bot succesfully started. visit /results to see the results"
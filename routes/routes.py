from services.rpa import rpa
from fastapi import APIRouter

import json


#atribuir o router
router = APIRouter()

#criar as rotas e definir as funções
@router.get("/results")
def results():

    with open(r'files/lenovo.json', 'r') as f:
        response = json.load(f)

    return response

@router.get("/")
def run_bot():

    rpa()

    return "bot succesfully started. visit /results to see the results"
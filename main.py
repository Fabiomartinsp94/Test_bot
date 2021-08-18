from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.routes import router as api_router

#Definir a função, configurar o CORS, atribuir a classe a app
def get_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins= ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix="/api")
    return application

#uvicorn main:app
app = get_application()
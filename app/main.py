from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from routes import user_routes,project_routes  # type: ignore
from db import init_db

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(project_routes.router)
init_db()

@app.get('/',tags=['root'])
def root():
  # return RedirectResponse(url='/docs')
  return JSONResponse(
        content={'message': 'Welcome to the Library Management System APIs'},
        status_code=200
    )

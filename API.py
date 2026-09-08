from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="test.html"
       )

@app.get("/test")
def test(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="test.html"
       )

@app.get("/program")
def program(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="program.html"
    )

@app.get("/tutor")
def tutor(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="tutor.html"
    )


#python -m uvicorn API:app --reload

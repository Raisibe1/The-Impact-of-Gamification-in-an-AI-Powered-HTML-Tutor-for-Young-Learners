"""Refactored from the supplied CodeVerse API.py; route contracts are preserved."""
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from core.web import templates
from core.security import get_current_student
router = APIRouter(tags=['Legacy HTML Pages'])

@router.get('/')
def root(request: Request):
     # Check if the user has a valid session
    student = get_current_student(request)
    if student is None:
        # Not logged in -> redirect to the React login page
        return RedirectResponse("http://localhost:5173/", status_code=303)
    
    return templates.TemplateResponse(
        request=request,
        name="tutor.html",
        context={"student": dict(student)} # Optionally pass student data to the game

       )


@router.get('/javascript')
def javascript(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="javascript.html")


@router.get('/test')
def test(request: Request):
    student = get_current_student(request)
    if student is None:
        return RedirectResponse("http://localhost:5173/", status_code=303)
        
    return templates.TemplateResponse(
        request=request,
        name="test.html"
       )


@router.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html")


@router.get('/program')
def program(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="program.html"
    )


@router.get('/tutor')
def tutor(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="tutor.html"
    )


@router.get('/registration')
def registration(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="registration.html")

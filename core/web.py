"""Legacy Jinja2 template rendering, retained for the existing HTML UI."""
from fastapi.templating import Jinja2Templates
from core.config import ROOT
templates = Jinja2Templates(directory=str(ROOT / 'templates'))

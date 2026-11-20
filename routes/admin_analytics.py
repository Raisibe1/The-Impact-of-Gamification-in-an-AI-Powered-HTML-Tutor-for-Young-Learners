from pathlib import Path
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
GRAPH_DIR = BASE_DIR / "reports" / "graphs"
HTML_FILE = BASE_DIR / "templates" / "admin_analytics.html"

ALLOWED_GRAPHS = {
	"class_distribution.png",
	"confusion_matrices.png",
	"roc_curves.png",
	"model_comparisons.png",
}

def verify_admin(request:Request):
	print("create an admin table")
	
@router.get("/admin/analytics")
def analytics_dashboard(request: Request):
	verify_admin(request)

	return FileResponse(
		HTML_FILE,
		media_type="text/html"
	)

@router.get("/api/admin/graphs/{filename}")
def get_graph(filename: str, request:Request):
	verify_admin(request)

	if filename not in ALLOWED_GRAPHS:
		raise HTTPException(
			status_code=404,
			detail="Graph not found"
		)

	graph_path = GRAPH_DIR / filename

	if not graph_path.is_file():
		raise HTTPException(
			status_code=404,
			detail="Graph not yet generated"
		)

	return FileResponse(
		graph_path,
		media_type="image/png"
	)
# main.py

from fastapi import FastAPI
from src.api import routes
from fastapi.responses import RedirectResponse # 1. Import RedirectResponse

app = FastAPI(
    title="AI-Powered Health Risk Profiler",
    description="An API to analyze lifestyle surveys and generate health risk profiles.",
    version="1.0.0"
)

# Include the API routes
app.include_router(routes.router)

# 2. Change the root endpoint to redirect to /docs
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirects the root URL to the /docs endpoint."""
    return RedirectResponse(url="/docs")
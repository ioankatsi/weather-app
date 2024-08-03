from fastapi import APIRouter
import os


router = APIRouter()


@router.get("/health", summary="Health Check", description="Check the health status of the application.")
def health_check():
    """
    Health check endpoint to ensure the application is running properly.
    """
    return {"status": "healthy"}

# Version Endpoint


@router.get("/version", summary="API Version", description="Get the version of the API.")
def get_version():
    """
    Version endpoint to retrieve the current version of the API.
    """
    BACKEND_VERSION = os.getenv("BACKEND_VERSION", "")
    return {"version": BACKEND_VERSION}

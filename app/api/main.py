from fastapi import FastAPI, Depends, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.deps import get_api_key, get_db
from app.models import receivables as models
from app.core.database import engine
# Importing routers
from app.api.routers import receivables
from app.core.config import config_instance as config

# Database configurations and session
from app.core import database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,  # Extracted from config
    allow_credentials=True,
    allow_methods=["POST, GET"],
    allow_headers=["*"],
)


# Middleware to manage DB sessions, ensuring they are opened and closed for each request.
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        request.state.db = database.SessionLocal()  # creating a new session
        response = await call_next(request)  # processing the request and response
    finally:
        request.state.db.close()  # closing the db session
    return response


# Including routers with API key dependency for certain routes
app.include_router(
    receivables.router,
    tags=["receivables"],
    prefix=config.api_prefix,
    dependencies=[Depends(get_api_key)]
    # Including dependencies to be used across all routes in the router
)


@app.on_event("startup")
async def startup_event():
    """
    Create tables in database at startup
    """
    models.Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Dispose of the database engine on application shutdown
    """
    if engine:
        await engine.dispose()


# Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "TP24 Receivables API"}

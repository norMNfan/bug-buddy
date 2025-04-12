from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import repos

app = FastAPI()


# Initialize database tables and mock data
@app.on_event("startup")
async def startup_event():
    init_db()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Include routers
app.include_router(repos.router, prefix="/repos", tags=["repos"])

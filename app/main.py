from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import stocks  # This is where your scoring logic lives

# 1. Lifespan: Logic that runs once when the API starts/stops
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to Snowflake...")
    # Setup global resources here
    yield
    print("Closing connections...")
    # Clean up here

# 2. Initialize the App
app = FastAPI(
    title="Artisanal Investment API",
    version="1.0.0",
    lifespan=lifespan
)

# 3. Security: Allow your frontend (Desktop/Mobile) to access this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Include Routers (The "Departments")
#app.include_router(stocks.router, prefix="/v1/stocks", tags=["Investment Logic"])

# 5. Basic Health Check
@app.get("/")
async def root():
    return {"status": "Online", "message": "Investment Intelligence Active"}
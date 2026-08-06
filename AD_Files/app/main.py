from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from common.rate_limiting import limiter, custom_rate_limit_handler
from common.logger import setup_logging
from common.logging_middleware import StructlogMiddleware
from app.core.config import settings
from app.api.files import router as files_router
from app.api.pools import router as pools_router

setup_logging(json_logs=False, log_level="INFO")


app = FastAPI(title=settings.APP_NAME, root_path="/files")

app.add_middleware(StructlogMiddleware)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(files_router)
app.include_router(pools_router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8003",
    "http://127.0.0.1:8003",
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

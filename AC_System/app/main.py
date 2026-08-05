from fastapi import FastAPI
from app.services.docker_monitor import docker_event_listener
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from contextlib import asynccontextmanager
import asyncio
from common.rate_limiting import limiter, custom_rate_limit_handler
from common.logger import setup_logging
from common.logging_middleware import StructlogMiddleware
from app.core.config import settings
from app.api.containers import router as containers_router
from app.api.dashboard import router as dashboard_router
from app.api.containers import router as containers_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Akcje przy starcie aplikacji (uruchomienie demona dockera w tle)
    docker_task = asyncio.create_task(docker_event_listener())
    yield
    
    # Akcje przy zamykaniu (Clean-up)
    docker_task.cancel()
    await docker_task

setup_logging(json_logs=False, log_level="INFO")


app = FastAPI(title=settings.APP_NAME, root_path="/system", lifespan=lifespan)

app.add_middleware(StructlogMiddleware)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(containers_router)
app.include_router(dashboard_router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8002",
    "http://127.0.0.1:8002",
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

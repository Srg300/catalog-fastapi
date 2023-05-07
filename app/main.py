import uvicorn
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import api
from config import settings
from db import engine

log_fmt = r"%(asctime)-15s %(levelname)s %(name)s %(funcName)s:%(lineno)d %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger("uvicorn.error")
logger.propagate = False
logging.basicConfig(format=log_fmt, level=logging.ERROR, datefmt=datefmt)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.on_event("startup")
async def startup():
   engine.connect()


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
        host=settings.HOST,
        port=settings.PORT,
        proxy_headers=True,
        reload=True,
        log_level=settings.LOG_LEVEL
    )

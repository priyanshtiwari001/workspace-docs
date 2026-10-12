from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, status,APIRouter
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from .core.base import Base
from .core.databases import engine, get_db
from .core.exception import AppException
from .models.user import User
from .routes import router
from .schemas.schemas import ErrorResponse, SuccessResponse, UserCreate, UserResponse
from .services.user_services import UserService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any setup tasks here (e.g., database connection, etc.)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()  # Dispose of the engine to close the connection
    # Perform any cleanup tasks here (e.g., closing database connection, etc.)



app = FastAPI(lifespan=lifespan,title="Workspace Docs",version="1.0.0",)

app.include_router(router)





@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    response = ErrorResponse(
        message=exc.message,
        error={"explanation": exc.explanation, "type": type(exc).__name__, "status_code": exc.status_code}
    )
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
        response = ErrorResponse(
            message="Validation error",
            error={"explanation": exc.errors(),"status_code":status.HTTP_422_UNPROCESSABLE_ENTITY} 
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response.model_dump())


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc: Exception):
    response = ErrorResponse(
        message="Internal Server Error",
        error={"explanation": str(exc)}
    )
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.model_dump())

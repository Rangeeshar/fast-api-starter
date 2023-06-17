"""
Main module which starts the application
"""
# Third party package
from fastapi import FastAPI

# User imports
from app.api.v1.user import router
from app.api.v1.claim import claim_router
from app.common.api_exceptions import RequestErrorHandler, RequestError
from app.middleware.request_middleware import RequestContextLogMiddleware
from app.core.db.db_session import engine
from app.database.postgres.model import common_fields

# initialize fastapi module
app = FastAPI(debug=True)
common_fields.metadata.create_all(bind=engine)
app.include_router(router.api_router, prefix="/api/v1")
app.include_router(claim_router.api_router, prefix="/api/v1")
app.add_middleware(RequestContextLogMiddleware)


@app.exception_handler(RequestError)
async def request_error_internal(request, exc):
    reh = RequestErrorHandler(exc=exc)
    return reh.process_message()


@app.get("/health")
async def root():
    return {"message": "Health check passed."}

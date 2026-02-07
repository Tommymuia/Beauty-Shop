from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
import os
from app.api.v1 import auth, products, orders, admin, mpesa, categories
from app.db.session import engine
from app.db.base import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Beauty Shop API",
    version="1.0.0",
    redirect_slashes=False
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    debug = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")  # FIXED
    errors = exc.errors()
    if not debug:
        sanitized = []
        for e in errors:
            sanitized.append({
                "loc": e.get("loc"),  # FIXED
                "msg": e.get("msg"),
                "type": e.get("type"),
            })
        errors_by_field = {}
        for e in errors:
            loc = e.get("loc", [])
            if len(loc) >= 2 and loc[0] == "body":
                field = ".".join(str(x) for x in loc[1:])  # FIXED
            else:
                field = ".".join(str(x) for x in loc)
            errors_by_field.setdefault(field, []).append(e.get("msg"))
        return JSONResponse(status_code=422, content={"detail": sanitized, "errors": errors_by_field})
    return JSONResponse(status_code=422, content={"detail": errors})

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_origin_regex=r"^https?://(localhost|127.0.0.1)(:\d+)?$",  # FIXED
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(mpesa.router)
app.include_router(categories.router)

@app.get("/")
def home():
    return {"Status": "Success", "message": "Beauty Shop API is running!"}
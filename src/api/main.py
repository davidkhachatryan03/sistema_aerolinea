from fastapi import FastAPI
from api.routers import create_booking_router

app = FastAPI(
    title=" Booking API",
    description="API for booking's system",
    version="1.0.0"
)

app.include_router(create_booking_router.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "The server is working."}
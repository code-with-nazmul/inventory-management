
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db


app = FastAPI(
  title = "Inventory Management API",
  description = "Backend API for inventory and order management",
  version = "1.0.0",
)


@app.get("/")
def root():
  return {"message": "Inventory Management API is running"}


@app.get("/health")
def health_check():
  return {"status": "healthy"}


@app.get("/health/db")
def database_health_check(db: Session = Depends(get_db)):
  result = db.execute(text("SELECT 1")).scalar_one()

  return {
    "database": "connected",
    "test_query_result": result,
  }

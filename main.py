from fastapi import FastAPI
from app.routes import cars  # Import your routers or API endpoints
from app.database import database  # Import your database setup if any
from app.schemas import Car
import uvicorn

app = FastAPI()

# Include your routers or API endpoints
app.include_router(cars.router)


database.connect()


if __name__ == '__main__':
    uvicorn.run("app.app:app", log_level="info", port=8000)

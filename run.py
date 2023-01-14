import uvicorn

from app import rocket
from app.routers import user, case
from app.models import Base, engine

Base.metadata.create_all(engine)

rocket.include_router(user.router)
rocket.include_router(case.router)

if __name__ == '__main__':
    uvicorn.run("main:rocket", host="0.0.0.0", port=5000, reload=True)

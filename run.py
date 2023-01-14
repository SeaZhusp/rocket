import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app import rocket
from app.routers import user, case
from app.models import Base, engine

Base.metadata.create_all(engine)

rocket.include_router(user.router)
rocket.include_router(case.router)

rocket.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == '__main__':
    uvicorn.run("app:rocket", host="0.0.0.0", port=5000, reload=True)

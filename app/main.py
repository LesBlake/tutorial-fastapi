from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import models
# from database import engine
from app.routers import authn, post, user, vote

# Used this initially to create the tables in the database, now we transitioned to Alembic,
# models.Base.metadata.create_all(bind=engine)

# *********************** FastAPI instance recteated ***********************
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authn.router)
app.include_router(vote.router)


# *********************** ROOT ***********************
@app.get("/")
def root():
    return {"message": "Welcome to my API."}

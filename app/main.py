from fastapi import FastAPI

import models
from database import engine
from routers import authn, post, user, vote

# Used this initially to create the tables in the database, now we transitioned to Alembic,
# models.Base.metadata.create_all(bind=engine)

# *********************** FastAPI instance recteated ***********************
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(authn.router)
app.include_router(vote.router)


# *********************** ROOT ***********************
@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}

from fastapi import FastAPI

import models

# from config import settings
from database import engine
from routers import authn, post, user

models.Base.metadata.create_all(bind=engine)

# *********************** FastAPI instance recteated ***********************
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(authn.router)


# *********************** ROOT ***********************
@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}

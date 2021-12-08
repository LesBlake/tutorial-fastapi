from fastapi import FastAPI



from . import models
from .database import engine
from .routers import post, user, authn

models.Base.metadata.create_all(bind=engine)

# *********************** FastAPI instance recteated ***********************
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(authn.router)

# *********************** ROOT ***********************
@app.get('/')
def root():
    return{"message": "Welcome to my API!!"}

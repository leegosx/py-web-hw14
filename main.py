import time
import redis.asyncio as redis

from sqlalchemy.orm import Session
from sqlalchemy import text

from fastapi import FastAPI, Request, Depends, HTTPException, status, BackgroundTasks
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig, MessageType
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter.depends import RateLimiter

from src.routes import contacts, auth, users
from src.database.db import get_db
from src.schemas import EmailSchema
from src.services.email import conf

app = FastAPI()

origins = [ 
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    The add_process_time_header function adds a header to the response called My-Process-Time.
    The value of this header is the time it took for the request to be processed by all middleware and routes.
    
    :param request: Request: Access the request object
    :param call_next: Call the next function in the pipeline
    :return: A response object
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response

@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app, like database connections or caches.
    
    :return: A list of coroutines
    """
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/", name='Корінь проекту')
def read_root():
    """
    The read_root function is a view function that returns the root of the API.
    It's purpose is to provide a simple way for users to test if their connection
    to the API is working properly.
    
    :return: A dictionary
    """
    return {"message": "Rest APIContacts v.1"}

@app.get("/api/healthchecker")
def healthchecher(db: Session = Depends(get_db)):
    """
    The healthchecher function is used to check the health of the application.
    It returns a message if everything is ok, or an error otherwise.
    
    :param db: Session: Pass the database connection to the function
    :return: A dict with a message
    """
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcom to FastApi"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")
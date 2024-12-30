from dotenv import load_dotenv
from fastapi import HTTPException
from mongoengine import connect,connection
import os

load_dotenv()

MONGO_URL=os.getenv("MONGODB_URL")

def init_db():
    try:
        if not MONGO_URL:
              raise HTTPException(status_code=400, detail="MongoDB URL not found")
        connect(host=MONGO_URL)
        client = connection.get_connection()
        client.admin.command('ping')
    except ConnectionError as ce:
         raise HTTPException(status_code=500,detail="Failed To Connect to DataBase "+str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


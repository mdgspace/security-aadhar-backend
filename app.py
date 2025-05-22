from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from views import add_person, remove_person, get_people_in, get_logs, get_people_out
from utils import save_image
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AddPersonRequest(BaseModel):
    aadhar: int
    name: str

class RemovePersonRequest(BaseModel):
    aadhar: int
        

@app.post("/removePerson")
def remove_person_endpoint(data: RemovePersonRequest):
    success = remove_person(data.aadhar)
    if not success:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"message": "Person removed successfully"}

@app.get("/getPeopleIn")
def get_people_in_endpoint():
    return get_people_in()

@app.get("/getLogs")
def get_logs_endpoint():
    return get_logs()

@app.get("/getRecentExits")
def get_recent_exits():
    return get_people_out()

@app.post("/registerUser")
async def register_user(
    file: UploadFile = File(...),
    isDigital: bool = Form(...)
):
    print("Received file:", file.filename)
    try:
        file_path = save_image(file=file, upload_dir=UPLOAD_DIR)
        # print("File saved at:", file_path) #Uncomment for debugging
        # print("isdigital:", isDigital) #Uncomment for debugging
        aadhar, name = add_person(path=file_path, isDigital=isDigital)
        # print("User registered:", aadhar, name) #Uncomment for debugging
        return aadhar
    except Exception as e:
        # print("Error:", e) #Uncomment for debugging
        raise HTTPException(status_code=500, detail="Failed to register user")


    

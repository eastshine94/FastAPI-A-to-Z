from fastapi import FastAPI
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"



app = FastAPI()

@app.get("/")
async def root():
    return {
        "message":"Hello World"
    }

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {
        "item_id":item_id
    }

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    print(model_name, model_name.value, model_name == 'alexnet')
    if model_name is model_name.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return  {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
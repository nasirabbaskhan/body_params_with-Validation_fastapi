from fastapi import FastAPI,Query,Path, Body # type: ignore
import uvicorn # type: ignore
from pydantic import BaseModel , Field
from typing import Annotated

app= FastAPI()
# if any varible that heve pydantic type fastapi consider it is body parameter
class Item(BaseModel):
    id: int
    price :int
    description: str | None= None
    tex: int | None = None
    
class User(BaseModel):
    userName: str
    
    
#validation on pydantic type
class Users(BaseModel):
    userName: str = Field(max_digits=10, title="this is title ")

@app.get("/bodyParams")
def student(item:Item):
    return item

@app.get("/bodyParamswithTex")
def student1(item:Item): # body params
    item_dect= item.dict() #  convert item into dictionary
    if item.tex:
        price_with_tex= item.tex + item.price
        item_dect.update({"price_with_tex":price_with_tex}) # adding price_with_tex in dictionary 
    return item_dect


@app.get("/pathquerybodyparams/{id}")
def student3(id, studenName:str, item:Item): # body params
    return {
        "id":id,
        "studenName":studenName,
        "item":item
          }
    
 # Annotated used for validation   
# Declare additional validation and matadata for parameter
@app.get("/getAnnotated")
def annotated(item:Annotated[str, Query(max_length=10, min_length=4 , pattern="^nas[a-zA-Z0-9]")]): #query params with validation
    return item

# 
# path parameter and Numaric validation
@app.get("/AnnotatedValidation/{id}") # Path parameter
def AnnotatedValidation(id:Annotated[int, Path(le=5,ge=3)]): #le=less then and equal to, ge= greater than and equal to
    return {"id":id}

#  body multiple parameter
@app.get("/bodyMultiParams")
def bpdyMultiParams(item:Item,user:User, count: Annotated[int, Body()]):
    result= {"item":item,"user": user,"count":count }
    return result

##  passing the multy body params

# {
#     "count":55,
#     "item":{
#      "id": 2,
#     "price":400
#     },
#     "user":{
#         "userName":"vhghgh"
#         }
# }


def start():
    uvicorn.run("todo.main:app", host="127.0.0.1", port= 8080, reload=True)
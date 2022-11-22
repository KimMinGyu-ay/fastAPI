from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
app = FastAPI()

db = []

#--------------------------------------------------------------------------
# data models

#--------------------------------------------------------------------------
class City(BaseModel):
    name: str
    timezone: str


templates = Jinja2Templates(directory="templates")

@app.get("/") # url 만들기

def root():
    return {"Hello":"World"}



@app.get("/cities",response_class=HTMLResponse)
def get_cities(request: Request):
    context = {}
    rsCity = []
    cnt = 0
    for city in db:
        strs = f"https://worldtimeapi.org/api/timezone/{city['timezone']}"
        r = requests.get(strs)
        cur_time = r.json()["datetime"]
        cnt +=1
        rsCity.append(
            {   "id" : cnt,
                "name":city["name"],
                "timezone":city["timezone"],
                "current_time":cur_time
            }
            )
    context["request"] = request
    context["rsCity"] = rsCity
    return templates.TemplateResponse("city_list.html",context=context)


@app.get("/cities/{city_id}")
def det_city(city_id:int):
    city = db[city_id-1]
    strs = f"https://worldtimeapi.org/api/timezone/{city['timezone']}"
 
    r = requests.get(strs)
    cur_time = r.json()["datetime"]
    return {
        "name":city["name"],"timezone":city["timezone"],"current_time":cur_time}
        

@app.post("/cities")
def create_city(city:City):
    db.append(city.dict())
    print(db)
    return db[-1]

@app.delete("/cities/{city_id}")
def delet_city(city_id:int):
    db.pop(city_id-1)

    return {}
# Restfull을 FastAPI로 구현
# locall / url / docs (Swagger) --> RestAPI를 Json으로 표현하는 방식
# locall / url / redoc
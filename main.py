from fastapi import FastAPI
from pydantic import BaseModel
import requests
app = FastAPI()

db = []

class City(BaseModel):
    name: str
    timezone: str
@app.get("/") # url 만들기

def root():
    return {"Hello":"World"}



@app.get("/cities")
def get_cities():
    results = []
    
    for city in db:
        strs = f"https://worldtimeapi.org/api/timezone/{city['timezone']}"
        
        r = requests.get(strs)

        cur_time = r.json()["datetime"]
        results.append(
            {
                "name":city["name"],
                "timezone":city["timezone"],
                "currenct_time":cur_time
            }
            )
    
    return results


@app.get("/cities/{city_id}")
def get_city(city_id:int):
    city = db[city_id-1]
    strs = f"https://worldtimeapi.org/api/timezone/{city['timezone']}"
 
    r = requests.get(strs)
    cur_time = r.json()["datetime"]
    return {
        "name":city["name"],"timezone":city["timezone"],"currenct_time":cur_time}
        

@app.post("/cities")
def create_city(city:City):
    db.append(city.dict())
    return db[-1]

@app.delete("/cities/{city_id}")
def delet_city(city_id:int):
    db.pop(city_id-1)

    return {}
# Restfull을 FastAPI로 구현
# locall / url / docs (Swagger) --> RestAPI를 Json으로 표현하는 방식
# locall / url / redoc
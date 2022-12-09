import uvicorn

import uvicorn
from fastapi import FastAPI,Query

import joblib # 기계학습 모델을 저장하고 다시 불러오는 라이브러리

# Vectorizer
gender_vectorizer = open("model/gender_vectorizer.pkl","rb")
gender_cv = joblib.load(gender_vectorizer)

# Models
gender_nv_model = open("model/gender_nv_model.pkl","rb")
gender_clf =  joblib.load(gender_nv_model)

app = FastAPI()

@app.get("/")
async def index():
    return {"message" : "ML전문가님 안녕하세요"}


@app.get("/item/{name}")
async def get_item(name):
    return {"name": name}

@app.get("/predict")
async def predict(name):
    vactorized_name = gender_cv.transform([name]).toarray()
    prediction = gender_clf.predict(vactorized_name)
    result = ""

    if prediction[0] == 0:
        result = "여성"
    else:
        result = "남성"

    return {"origin name" : name, "예측" : result}

@app.post("/predict")
async def predict(name):
    vactorized_name = gender_cv.transform([name]).toarray()
    prediction = gender_clf.predict(vactorized_name)
    result = ""

    if prediction[0] == 0:
        result = "여성"
    else:
        result = "남성"

    return {"origin name" : name, "예측" : result}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
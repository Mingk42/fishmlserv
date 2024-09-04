from typing import Union
from fastapi import FastAPI
import pickle

from fishmlserv.model.manager import get_model_path

with open(get_model_path(), "rb") as f:
    fish_model=pickle.load(f)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/")
def post_root():
    return {"method":"post"}

@app.get("/fish")
def fish(length:float, weight:float):
    """
    어종 판별기

    Args:
     - length(int): 물고기 길이(cm)
     - weight(int): 물고기 무게(g)

    Return
     - dict, 물고기의 종류를 담은 딕셔너리
    """
    
#    if length>=30:
#        prediction="도미"
#    else:
#        prediction="빙어"

#    from fishmlserv.model.manager import get_model_path 

#   with open(get_model_path(), "rb") as f:
#       fish_model=pickle.load(f)
        
    pred=fish_model.predict([[length, weight]])[0]

    CLASSES={
                0:"빙어",
                1:"도미"
            }

    return {
            "prediction":CLASSES[pred],
            # "prediction":get_model_path(),
            "length":length,
            "weight":weight
            }


import typer

app = typer.Typer()


def prediction(l:float=typer.Option(...,"-l"), w:float=typer.Option(...,"-w")):

    from fishmlserv.model.manager import get_model_path
    from sklearn.neighbors import KNeighborsClassifier
    import pickle

    with open(get_model_path(),"rb") as f:
        model=pickle.load(f)

    pred=model.predict([[l,w]])
    
    CLASSES={
        0:"빙어",
        1:"도미"
    }

    print(CLASSES[pred[0]])


def run():
    typer.run(prediction)


def run_pred(length:float=typer.Option(...,"-l","--length"),weight:float=typer.Option(...,"-w","--weight")):

    typer.run(fish(length,weight))


def fish(length:float, weight:float):
    """
    어종 판별기

    Args:
     - length(int): 물고기 길이(cm)
     - weight(int): 물고기 무게(g)

    Return
     - dict, 물고기의 종류를 담은 딕셔너리
    """
    from fishmlserv.model.manager import get_model_path
    from sklearn.neighbors import KNeighborsClassifier
    import pickle
    
#    if length>=30:
#        prediction="도미"
#    else:
#        prediction="빙어"


    with open(get_model_path(), "rb") as f:
        fish_model=pickle.load(f)
        
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
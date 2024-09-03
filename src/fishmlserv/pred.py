import typer

app = typer.Typer()


def prediction(l:float=typer.Option(...,"-l","--length"), w:float=typer.Option(...,"-w","--weight")):
    """
    어종 판별기

    Args:
     - length(int): 물고기 길이(cm)
     - weight(int): 물고기 무게(g)

    Returns:
     - str, 물고기의 종류를 반환 (도미/빙어)
    """

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

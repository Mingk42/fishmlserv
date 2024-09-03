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

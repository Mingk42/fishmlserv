import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

@app.command()
def prediction(l:float=typer.Option(), w:float=typer.Option()):
    from fishmlserv.model.manager import get_model_path
    import pickle

    with open(get_model_path(),"rb") as f:
        model=pickle.load(f)

    pred=model.predict(l,w)

    print(pred)


if __name__ == "__main__":
    app()

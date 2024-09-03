
def get_model_path():
    ## 이 함수 파일의 절대 경로를 받아온다.
    import os
    abspath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(abspath, "model.pkl")


# print(get_model_path())
